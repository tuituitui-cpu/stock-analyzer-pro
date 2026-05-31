# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
import time
import random

def fetch_a_stock_data():
    print("正在从互联网获取A股最新数据，请稍候...")
    
    # 最多尝试获取 3 次
    for i in range(3):
        try:
            # 使用 akshare 获取A股实时行情列表
            stock_df = ak.stock_zh_a_spot_em()
            
            if not stock_df.empty:
                print(f" 成功获取到 {len(stock_df)} 只股票的数据！")
                
                # 1. 筛选贵州茅台 (600519)
                moutai = stock_df[stock_df['代码'] == '600519']
                if not moutai.empty:
                    print("\n--- 贵州茅台 (600519) 最新行情 ---")
                    print(f"名称: {moutai.iloc['名称']}")
                    print(f"最新价: {moutai.iloc['最新价']}")
                    print(f"涨跌幅: {moutai.iloc['涨跌幅']}%")
                
                # 2. 筛选涨停的股票 (涨跌幅 > 9.8%)
                limit_up = stock_df[stock_df['涨跌幅'] > 9.8]
                if not limit_up.empty:
                    print(f"\n--- 涨停板股票 ({len(limit_up)} 只) ---")
                    print(limit_up[['代码', '名称', '最新价', '涨跌幅']].head().to_string(index=False))
                
                # 3. 将数据保存到 CSV 文件
                stock_df.to_csv("a_share_realtime_data.csv", index=False, encoding="utf-8-sig")
                print("\n 数据已自动保存到 a_share_realtime_data.csv")
                return # 获取成功，直接退出函数
                
        except Exception as e:
            print(f" 第 {i+1} 次尝试获取数据失败: {e}")
            if i < 2: # 如果不是最后一次尝试，就等待一下再重试
                wait_time = random.uniform(3, 6) # 随机等待 3 到 6 秒
                print(f" 等待 {wait_time:.1f} 秒后自动重试...\n")
                time.sleep(wait_time)
    
    print(" 经过多次尝试仍无法获取数据，请稍后再运行程序。")

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    fetch_a_stock_data()