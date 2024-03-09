import websocket
import requests
import json


class BinanceAPI(websocket._app.WebSocketApp): 
    BINANCE_API_URL = "wss://stream.binance.com:9443/ws"
    def __init__(self, symbols: list = []):
        self.symbols = symbols
        self.data = { symbol: {} for symbol in symbols}
        super().__init__(self.BINANCE_API_URL, 
                         on_message=self.on_message,
                         on_error=self.on_error,
                         on_close=self.on_close, on_open=self.on_open)

    def on_message(self,_, message):
        data = json.loads(message)
        update_id = data.get('u', -1)
        symbol = data.get('s', "N/A")
        best_bid_price = float(data.get('b', 0.0))
        best_ask_price = float(data.get('a', 0.0))
        if symbol == "N/A":
            return
        self.data[symbol.lower()] = {
            "update_id": update_id,
            "best_bid_price": best_bid_price,
            "best_ask_price": best_ask_price
        }

    def on_error(self, _, error):
        print(f"Error: {error}")
    
    def on_close(self, _, close_status_code, close_msg):
        print("Closed WebSocket Connection...")

    def on_open(self, _):
        subscription_message = {
            "method": "SUBSCRIBE",
            "params": [
                f"{symbol}@bookTicker" for symbol in self.symbols
            ],
            "id": 1
        }

        self.send(json.dumps(subscription_message))


    @staticmethod
    def get_trading_pairs():
        api_url = "https://api.binance.com/api/v3/exchangeInfo"

        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            symbols = [symbol['symbol'].lower() for symbol in data['symbols']]
            return symbols
        else:
            print(f"Error: {data}")
            return []


