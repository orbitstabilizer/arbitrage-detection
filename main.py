from binanceapi import BinanceAPI
import time
import threading

def demo1():
    symbols = BinanceAPI.get_trading_pairs()
    # filter = list(symbols.keys())[:10]
    filter = ["btcusdt", "ethusdt", "usdttry", "btctry", "ethbtc", "btceur"]
    filtered_symbols = {k: symbols[k] for k in filter}


    ws = BinanceAPI(symbols=filtered_symbols)
    t = threading.Thread(target=ws.run_forever)

    t.start()

    cnt = 0
    while cnt < 1000:
        print(f'{"":<10}', end=" ")
        for u in ws.adj:
            print(f'{u:<10}', end=" ")
        print()

        for v in ws.adj:
            print(f'{v:<10}', end=" ")
            for u in ws.adj:
                if v in ws.adj[u]:
                    print(f'{ws.adj[v][u]:<10.6f}', end=" ")
                else:
                    print(f'{" ":<10}', end=" ")
            print()
        time.sleep(1)
        cnt += 1

    ws.close()

    t.join()

    print("Done!")

def demo2():
    symbols = BinanceAPI.get_trading_pairs()
    filter = list(symbols.keys())[:150]
    # filter = ["btcusdt", "ethusdt", "usdttry", "btctry", "ethbtc", "btceur"]
    filtered_symbols = {k: symbols[k] for k in filter}
    N = sum([len(v) for v in filtered_symbols.values()])
    print(N)
    assert N <= 500 , f"Too many symbols: {N} > 500"


    ws = BinanceAPI(symbols=filtered_symbols)
    t = threading.Thread(target=ws.run_forever)

    t.start()

    while True:
        time.sleep(0.1)
        # print(ws.adj)
        it = list(ws.arbitrage.items())
        it.sort(key=lambda x: x[1])
        if len(it) > 0:
            print(*it, sep="\n")
            print('--'*10)

    ws.close()

    t.join()

    print("Done!")
    

if __name__ == "__main__":
    demo2()
