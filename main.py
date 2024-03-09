from binanceapi import BinanceAPI
import time
import threading
if __name__ == "__main__":
    symbols = BinanceAPI.get_trading_pairs()[:5]
    print(symbols)

    ws = BinanceAPI(symbols=symbols)
    t = threading.Thread(target=ws.run_forever)

    t.start()

    cnt = 0
    while cnt < 10:
        for k, v in ws.data.items():
            print(k, v)
        time.sleep(1)
        cnt += 1

    ws.close()

    t.join()

    print("Done!")





