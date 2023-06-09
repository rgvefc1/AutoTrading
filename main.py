# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
import yaml
import Function


ACCESS_TOKEN = Function.get_access_token()

# 1. 데이터 수집일 3개월 경과시 재수집
Function.DataCheck()

# 2. 종목 리스트 불러오기
df = Function.GetData('data.xlsx')
# 3. 매수 조건 Setting
target_buy_count = 5 # 매수할 종목 수
buy_percent = 0.33 # 종목당 매수 금액 비율
win = 6  # 수익
lose = -5 # 손절

# 3-1. 오늘자 
try:
    Function.send_message("===국내 주식 자동매매 프로그램을 시작합니다===")
    # 4. 보유자산 가져오기
    total_cash = Function.get_balance(ACCESS_TOKEN) # 보유 현금 조회
    stock_dict = Function.get_stock_balance(ACCESS_TOKEN) # 보유 주식 조회
    buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
    soldout = len(stock_dict) >= target_buy_count

    while(True):
        t_now = datetime.datetime.now()
        t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
        t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
        t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
        t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
        today = datetime.datetime.today().weekday()
        if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
            Function.send_message("주말이므로 프로그램을 종료합니다.")
            break
        if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
            if(not soldout):
                for index, row in df.iterrows():
                    # 현재가격 가져오기
                    current_price = Function.get_current_price(row['Code'],ACCESS_TOKEN)
                    # 매수 여부 판단
                    buy_count = Function.get_target_price(row['lowest_price'],current_price,buy_amount)
                    if(buy_count > 0):
                        # 매수 진행
                        buy_success = Function.buy(ACCESS_TOKEN,row['Code'],buy_count)
                        if(buy_success):
                            stock_dict = Function.get_stock_balance(ACCESS_TOKEN) # 보유 주식 조회
                            soldout = len(stock_dict) >= target_buy_count
                    time.sleep(1)
                time.sleep(1)
            else:
                for key in stock_dict.keys():  # data = (종목코드,갯수,구매가격)
                    # 현재가격 가져오기
                    current_price = Function.get_current_price(key,ACCESS_TOKEN)
                    # 구매가격
                    buy_price = float(stock_dict[key][1])
                    # 수익률(%) = ((판매 가격 - 구매 가격) / 구매 가격) * 100
                    # 6% 수익률
                    win_price = buy_price + (buy_price * win / 100)

                    # -5% 수익률
                    Lose_price = buy_price + (buy_price * lose / 100)

                    # 6% 이상 또는 -5% 이하인지 확인하는 조건식
                    flag =  current_price >= win_price or current_price <= Lose_price
                    if(flag):
                        Function.send_message(f"지정가 확인 구매가 : {buy_price} 현재가: {current_price}")
                        Function.sell(ACCESS_TOKEN,key,stock_dict[key][0])
                        soldout = False
                    time.sleep(1)
                time.sleep(1)
        if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
            Function.send_message("프로그램을 종료합니다.")
            break
except Exception as e:
    Function.send_message(f"[오류 발생]{e}")
    time.sleep(1)
