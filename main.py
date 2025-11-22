import time
import pandas as pd
import yfinance as yf
import requests

TOKEN = "PUT_YOUR_TELEGRAM_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"

MARKETS = {
    "S&P 500 🇺🇸": "^GSPC",
    "DAX 🇩🇪": "^GDAXI",
}

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_ma_cross(symbol):
    data = yf.download(symbol, period="6mo", interval="30m")
    data["MA9"] = data["Close"].rolling(9).mean()
    data["MA26"] = data["Close"].rolling(26).mean()

    fast_prev = data["MA9"].iloc[-2]
    slow_prev = data["MA26"].iloc[-2]
    fast_now = data["MA9"].iloc[-1]
    slow_now = data["MA26"].iloc[-1]

    if fast_prev < slow_prev and fast_now > slow_now:
        send_msg(f"📈 BUY SIGNAL – {symbol}  (MA9 crossed ABOVE MA26)")
    elif fast_prev > slow_prev and fast_now < slow_now:
        send_msg(f"📉 SELL SIGNAL – {symbol} (MA9 crossed BELOW MA26)")

def main():
    while True:
        for name, symbol in MARKETS.items():
            check_ma_cross(symbol)
        time.sleep(60)

if __name__ == "__main__":
    main()
