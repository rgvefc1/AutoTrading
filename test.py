import Function

ACCESS_TOKEN = Function.get_access_token()

stock_dict = Function.get_stock_balance(ACCESS_TOKEN) # 보유 주식 조회
for key in stock_dict.keys():
    buy_price = float(stock_dict[key][1])
    buy_price = int(buy_price + (buy_price * 0.1))
    print(f"{key},{stock_dict[key][0]},{buy_price}")
    result = Function.order_resv(ACCESS_TOKEN,key,stock_dict[key][0],buy_price)