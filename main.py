from binanceapi import BinanceAPI
import time
import threading

def demo1():
    symbols = BinanceAPI.get_trading_pairs()
    filter = list(symbols.keys())[:10]
    filtered_symbols = {k: symbols[k] for k in filter}

    # symbols = ["btcusdt", "ethusdt", "usdttry", "btctry", "ethbtc", "btceur"]

    ws = BinanceAPI(symbols=filtered_symbols)
    t = threading.Thread(target=ws.run_forever)

    t.start()

    cnt = 0
    while cnt < 1000:
        print(f'{"":<5}', end=" ")
        for u in ws.adj:
            print(f'{u:<5}', end=" ")
        print()

        for v in ws.adj:
            print(f'{v:<5}', end=" ")
            for u in ws.adj:
                if v in ws.adj[u]:
                    print(f'{ws.adj[u][v]:<5.2f}', end=" ")
                else:
                    print(f'{"":<5}', end=" ")
            print()
        time.sleep(1)
        cnt += 1

    ws.close()

    t.join()

    print("Done!")

if __name__ == "__main__":
    demo1()
