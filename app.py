from flask import Flask, render_template
import requests
import redis


app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)

bitcoinPrice = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
bitcoinAvrPrice = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=9'

def getbitcoinPrice():
    try:
        response = requests.get(bitcoinPrice)
        data = response.json()['price']
        redis.set('btcoinPrice', data)
    except Exception as e:
        print(e)

    return data

def getbitcoinAvgPrice():
    try:
        response = requests.get(bitcoinAvrPrice)
        data = response.json()['Data']['Data']
        avg = 0;

        for price in data:
            avg += price['open']

        avg /= 10
        redis.set('btcoinAvgPrice', avg)
    except Exception as e:
        print(e)

    return avg



@app.route("/")
def home():
    return render_template("home.html", price=getbitcoinPrice(), avgPrice=getbitcoinAvgPrice()) 



if __name__ == "__main__":
    app.run(debug = True)