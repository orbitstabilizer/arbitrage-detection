import websocket
import requests
import json
from math import log10 as log



class BinanceAPI(websocket._app.WebSocketApp):
    BINANCE_API_URL = "wss://stream.binance.com:9443/ws"
    def __init__(self, symbols: dict = {})->None:
        """
        BinanceAPI class, inherits from websocket._app.WebSocketApp,
        - used to get real-time data from binance websocket api
        - calculates triangular arbitrage efficiency
        - gets trading pairs from binance api

        params:
            symbols: { trading_pair: (base_asset, quote_asset) }
        """
        self.symbols = symbols
        self.adj = self.setup_adj(symbols)
        self.eff = { u: 0 for u in self.adj}
        self.arbitrage = {}
        self.first_message = True
        super().__init__(self.BINANCE_API_URL,
                         on_message=self.on_message,
                         on_error=self.on_error,
                         on_close=self.on_close, on_open=self.on_open)


    def update_eff(self, u:str, v:str)->None:
        """
        Update triangular arbitrage efficiency, given the edge u -> v
        Checks if u -> v -> w -> u is an arbitrage opportunity for all w
        
        params:
        u: str
        v: str

        """
        # u -> v -> w -> u
        for w in self.adj[v]: # v -> w
            if w in self.adj[u]:
                self.eff[u] = self.adj[u][v] + self.adj[v][w] + self.adj[w][u]
                tri = [u,v,w]
                tri.sort()
                if (e:=self.eff[u]) > 0 and e != float('inf'):
                    self.arbitrage[tuple(tri)] = 10**self.eff[u]
                else:
                    self.arbitrage.pop(tuple(tri), None)

    def setup_adj(self, symbols: dict) -> dict:
        """
        Setup adjacency list for the graph of exchange rates
        initializes weights to infinity

        params:
            symbols: { trading_pair: (base_asset, quote_asset) }
        """
        adj = {}
        for u,v in self.symbols.values():
            if u not in adj:
                adj[u] = {}
            if v not in adj:
                adj[v] = {}
            adj[u][v] = float('inf')
            adj[v][u] = float('inf')
        return adj

    def on_message(self,_, message: str)->None:
        """
        Socket message handler 
        params:
            message: str
        """
        if self.first_message:
            print(message)
            self.first_message = False
        data = json.loads(message)
        update_id = data.get('u', -1)
        symbol = data.get('s', "none").lower()
        best_bid_price = float(data.get('b', float('inf')))
        best_ask_price = float(data.get('a', float('inf')))
        print(f"Symbol: {symbol}, Bid: {best_bid_price}, Ask: {best_ask_price}")
        if symbol != "none":
            u,v = self.symbols[symbol]
            self.adj[u][v] = log(best_bid_price)
            self.adj[v][u] = -log(best_ask_price)
            self.update_eff(u, v)
            self.update_eff(v, u)


    def on_error(self, _, error: Exception)->None:
        """
        Socket error handler
        """
        print(f"Error: {error}")

    def on_close(self, _, close_status_code: int , close_msg : str)->None:
        """
        Socket close handler
        """
        print("Closed WebSocket Connection...")

    def on_open(self, _):
        """
        Socket open handler
        Subscribes to the binance websocket api for the self.symbols trading pairs
        """
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
        """
        Get trading pairs from binance api
        """
        api_url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            symbols_and_tickers = { symbol['symbol'].lower():
                                    (symbol['baseAsset'].lower(),
                                    symbol['quoteAsset'].lower()) for symbol in data['symbols']}
            return symbols_and_tickers
        else:
            print(f"Error: {data}")
            return {}


