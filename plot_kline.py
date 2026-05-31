import akshare as ak
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# 1. 获取贵州茅台历史日线数据
print("正在获取贵州茅台历史数据...")
df = ak.stock_zh_a_daily(symbol="sh600519", adjust="qfq")

# 2. 数据预处理：兼容性升级
if isinstance(df.index, pd.DatetimeIndex):
    df = df.reset_index()

df.rename(columns={
    '日期': 'Date', 'date': 'Date', 'trade_date': 'Date',
    '开盘': 'Open', 'open': 'Open', 
    '最高': 'High', 'high': 'High', 
    '最低': 'Low', 'low': 'Low', 
    '收盘': 'Close', 'close': 'Close', 
    '成交量': 'Volume', 'volume': 'Volume'
}, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# 3. 先截取最近120个交易日的数据
df = df.tail(120)

# 4. 计算均线与识别金叉点
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()

# 识别金叉：5日均线上穿20日均线
df['Signal'] = 0
df.loc[(df['MA5'] > df['MA20']) & (df['MA5'].shift(1) <= df['MA20'].shift(1)), 'Signal'] = 1

# 【核心修复】提取金叉发生时的收盘价。
# 注意：这里保留完整的 df['Close'] 序列，只是把非金叉日的值设为 NaN。
# 这样它的长度就永远是 120，和 X 轴完美对应！
buy_points = df['Close'].where(df['Signal'] == 1)

# 5. 准备绘图配置
custom_style = mpf.make_mpf_style(
    mavcolors=['dodgerblue', 'goldenrod'], 
    rc={'font.family': 'SimHei'}
)

# 【核心修复】明确指定 panel=0，告诉 mplfinance 这是主图上的散点
ap = [
    mpf.make_addplot(df['MA5'], color='dodgerblue', width=1),
    mpf.make_addplot(df['MA20'], color='goldenrod', width=1),
    mpf.make_addplot(buy_points, type='scatter', markersize=100, marker='^', color='red', panel=0)
]

# 6. 绘制并保存K线图
print("正在生成K线图...")
mpf.plot(
    df,
    type='candle',
    style=custom_style,
    title='贵州茅台(600519) 日线K线与均线金叉',
    ylabel='价格（元）',
    volume=True,
    mav=(),
    addplot=ap,
    savefig='maotai_kline.png',
    figratio=(14, 8)
)
print("成功！K线图已保存为 maotai_kline.png，请在文件夹中查看。")