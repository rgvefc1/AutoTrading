# -*- coding: utf-8 -*-
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import os
import psutil

# Excel 프로세스 종료
for proc in psutil.process_iter():
    if "EXCEL.EXE" in proc.name():
        proc.kill()
file_path = 'data.xlsx'
# 기준일 설정 (오늘 날짜로부터 90일 전)
end_date = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")

if os.path.exists(file_path):
    os.remove(file_path)

tickers = stock.get_market_ticker_list(start_date)
result_dict = {}
for ticker in tickers:
    # 종목의 1년치 데이터 가져오기
    df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)

    # 가장 높았던 가격과 가장 낮았던 가격 뽑아내기
    highest_price = df['고가'].max()
    lowest_price = df['저가'].min()
    difference = highest_price - lowest_price
    if(lowest_price != 0):
        result_dict[ticker] = (highest_price, lowest_price,difference)

# 데이터프레임 생성
df = pd.DataFrame(result_dict).T.reset_index()
df.columns = ['Code', 'highest_price', 'lowest_price','difference']
df_sorted = df.sort_values('difference', ascending=False)
# 엑셀 파일로 저장
df_sorted.to_excel(file_path, index=False)