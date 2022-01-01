import ccxt
import pprint
import time

api_key=""
secret=""


binance=ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options':{
        'defaultType': 'future'
    }
})


symbols = {"ALGOUSDT" : 10,
           "FTMUSDT" : 10
          }

while True:
    for symbol, amount in symbols.items():
    
        T_stop_order=False
        T_limit_order=False
        P_Amt=0
        T_Amt=0
        T_no=""
        side = 'sell'
        amount = amount
        order_type = 'TRAILING_STOP_MARKET'
        rate = '0.5'
        price = None
        EP=0
        btc = binance.fetch_ticker(symbol)
        i = btc['last']
        balance=binance.fetch_balance()
        open_orders=binance.fetch_open_orders(symbol=symbol)
        positions=balance['info']['positions']
         
        for position in positions:
            if position["symbol"]==symbol:
                EP=float(position["entryPrice"])
                P_Amt=float(position["positionAmt"])

        #포지션 존재시 트레일링 주문 조회        
                if EP!=0.0:
                    for open_order in open_orders:
                        if open_order['info']['origType']=="TRAILING_STOP_MARKET":
                            T_Amt=float(open_order["amount"])
                            T_stop_order = True
                            T_no=(open_order["id"])

                    time.sleep(2) 

        #트레일링 주문없으면 신규 주문

                    if T_stop_order == False :
                        params = {
                        'activationPrice': EP*1.013,
                        'callbackRate': rate
                        }
                        order = binance.create_order(symbol, order_type, side, P_Amt, price, params)

        #트레일링 주문 있으면 취소하고 현재가 기준 다시주문
                    else :
                        if P_Amt == T_Amt :
                            pass

                        else :

                            binance.cancel_order(id=open_order['id'],symbol=symbol)  
                            
                            params = {
                            'activationPrice': EP*1.013,
                            'callbackRate': rate
                            }
                            order = binance.create_order(symbol, order_type, side, P_Amt, price, params)

        #현재 보유 포지션 없음

                else :
                    
                    for open_order in open_orders:
                        if open_order['info']['origType']=='LIMIT':
                            binance.cancel_order(id=open_order['id'],symbol=symbol)                    
                    
                    m_list = [0.999, 0.995, 0.99, 0.985, 0.95, 0.9, 0.85, 0.8]
                    
                    time.sleep(5)
                    for m in m_list:
                        order=binance.create_limit_buy_order(
                            symbol=symbol,
                            amount=amount,
                            price= i*m
                        )

    time.sleep(60)
