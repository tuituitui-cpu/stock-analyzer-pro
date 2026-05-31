import akshare as ak
import mplfinance as mpf
import pandas as pd
import time
import os

# ==========================================
# 1. 配置股票池 (代码, 显示名称)
# ==========================================
stock_pool = [
    ("002185", "华天科技"),
    ("000338", "潍柴动力"),
    ("600396", "华电辽能"),  # 原金山股份，已更名
    ("603601", "再升科技"),
    ("600986", "浙文互联"),
    ("002340", "格林美"),
    ("159206", "卫星ETF富国")
]

def get_stock_data(symbol, name):
    """
    获取数据并处理特殊情况（如改名）
    """
    print(f"正在获取: {name} ({symbol}) ...")
    try:
        # 获取最近120个交易日的数据
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date="",
            end_date="",
            adjust="qfq" # 前复权，适合看均线趋势
        )

        if df.empty:
            print(f"  ⚠️ {name} 未获取到数据，跳过。")
            return None

        # --- 特殊处理：强制修正显示名称 ---
        # 因为接口返回的可能还是旧名字（如金山股份），这里强制改为我们要的名字
        df['Name'] = name

        # 重命名列以符合 mplfinance 格式
        df.rename(columns={
            "日期": "Date",
            "开盘": "Open",
            "收盘": "Close",
            "最高": "High",
            "最低": "Low",
            "成交量": "Volume"
        }, inplace=True)

        # 转换日期格式
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # 确保数据类型正确
        for col in ['Open', 'Close', 'High', 'Low', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        print(f"  ❌ 获取 {name} 失败: {e}")
        return None

def plot_and_save(df, name):
    """
    计算均线、生成金叉信号并画图保存
    """
    if df is None:
        return

    # 计算均线
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # 寻找金叉点 (MA5上穿MA20)
    # 逻辑：今天MA5>MA20 且 昨天MA5<=MA20
    buy_signals = (df['MA5'] > df['MA20']) & (df['MA5'].shift(1) <= df['MA20'].shift(1))

    # 准备绘图标记
    # 只在金叉的那天标记一个向上的红色三角形
    markers = []
    for date, signal in buy_signals.items():
        if signal:
            price = df.loc[date, 'Low'] # 标记在最低价下方一点，或者用Low值
            markers.append(dict(
                marker=dict(marker='^', color='r', size=10),
                date=date,
                y=price * 0.995 # 稍微往下一点点，避免遮挡K线
            ))

    # 设置绘图风格
    mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=True)

    # 绘图
    filename = f"{name}_kline.png"
    try:
        mpf.plot(
            df,
            type='candle',
            style=s,
            title=f"{name} 日线K线与均线金叉",
            ylabel='价格 (元)',
            volume=True,
            ylabel_lower='成交量',
            mav=(5, 20),          # 显示5日和20日均线
            addplot=mpf.make_addplot(markers) if markers else None, # 如果没有信号就不加标记
            savefig=dict(fname=filename, dpi=150, bbox_inches='tight'), # 保存图片
            show_nontrading=False
        )
        print(f"  ✅ 图片已保存: {filename}")
    except Exception as e:
        print(f"  ❌ 绘图失败: {e}")

# ==========================================
# 主程序入口
# ==========================================
if __name__ == "__main__":
    print("开始批量扫描...")
    for code, name in stock_pool:
        # 1. 获取数据
        data = get_stock_data(code, name)
        # 2. 画图并保存
        plot_and_save(data, name)
        # 3. 稍微暂停一下，避免请求太快被接口限制
        time.sleep(1)

    print("\n全部任务完成！请查看文件夹中的图片。")