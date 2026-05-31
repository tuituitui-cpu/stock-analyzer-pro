import akshare as ak
import pandas as pd
import time

def get_a_stock_realtime(symbol):
    """
    获取A股实时行情数据
    :param symbol: 股票代码，例如 '600519' (贵州茅台)
    """
    try:
        # 使用 akshare 的 stock_zh_a_spot_em 接口
        # 这个接口获取的是东方财富网的实时行情，速度较快
        stock_df = ak.stock_zh_a_spot_em()

        # 筛选特定股票 (注意：akshare返回的代码通常是6位数字字符串)
        # 确保 symbol 是字符串格式
        target_stock = stock_df[stock_df['代码'] == str(symbol)]

        if target_stock.empty:
            return "未找到该股票数据，请检查代码是否正确。"

        # 提取关键信息
        current_price = target_stock.iloc[0]['最新价']
        change_pct = target_stock.iloc[0]['涨跌幅']
        volume = target_stock.iloc[0]['成交量']
        name = target_stock.iloc[0]['名称']

        print(f"--- {name} ({symbol}) 实时行情 ---")
        print(f"当前价格: {current_price}")
        print(f"涨跌幅: {change_pct}%")
        print(f"成交量: {volume}")
        print("-----------------------------")

        return target_stock

    except Exception as e:
        print(f"获取数据出错: {e}")
        return None

# --- 主程序入口 ---
if __name__ == "__main__":
    # 这里输入你想分析的 A 股代码，比如贵州茅台是 600519
    stock_code = "600519"

    # 获取一次数据
    get_a_stock_realtime(stock_code)

    # 如果你想做一个简单的实时监控（每3秒刷新一次）
    # while True:
    #     get_a_stock_realtime(stock_code)
    #     time.sleep(3)