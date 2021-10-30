import time
import os
import requests
import json

from datetime import datetime

import urllib.parse
import hashlib
import hmac
import base64
import copy

api_url = "https://api.kraken.com"
api_key = "ZEsiQqdtFTqA9a6eyFAq/Sp9Q9eOfwLLwuaAdn3jx09lC4z7Vu3jMaqF"
api_sec = "skHdho3TrnWCOeWArrJNXGlFOkweXdQTFwU2+NPxeDEiPEW7fVy6AE8Bnq3Ua9pokEhDFClLxGh1DUVSMKVfyA=="

TIME_INTERVAL = '15'
BASE_CURRENCY = 'USD' # USE EITHER 'USD' OR '/EUR


def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


def get_current_balance():
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)

    portfolio = resp.json()["result"]
    portfolio_tickers = {}
    for asset in portfolio.keys():
        if asset == "ZUSD" or asset == "ZEUR":
            continue
        quantity = float(portfolio[asset])
        if quantity > 0.001:
            ticker = asset
            if '.' in asset:
                ticker = asset.split('.')[0]
            portfolio_tickers[ticker] = quantity
    return portfolio_tickers


def get_raw_portfolio_time():
    portfolio_tickers = get_current_balance()
    ticker = list(portfolio_tickers.keys())[-1]
    raw_portfolio_time = []

    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair='+ticker+BASE_CURRENCY+'&interval='+TIME_INTERVAL+'&since='+str(TIME_FRAME))
    length_resp = len(resp.json()['result'][ticker+BASE_CURRENCY])-1
    for t in range(0, length_resp):
        tim = int(json.dumps(resp.json()['result'][ticker+BASE_CURRENCY][t][0]))
        raw_portfolio_time.append(tim)

    portfolio_timeline = [copy.deepcopy(portfolio_tickers) for i in range(int(length_resp))]
    return raw_portfolio_time, portfolio_timeline


def update_portfolio(time, asset, tx_type, cost, price):
    raw_portfolio_time, portfolio_timeline = get_raw_portfolio_time()
    for i in range(len(raw_portfolio_time)):
        if time < raw_portfolio_time[i]:
            tstart = i+1
            break
    if tx_type == "buy":
        cost *= (-1)
    for i in range(tstart, 0, -1):
        if asset not in list(portfolio_timeline[i].keys()):
            portfolio_timeline[i][asset] = cost/price
        else:
            portfolio_timeline[i][asset] = portfolio_timeline[i][asset] + cost/price


def get_all_trades():
    raw_portfolio_time, portfolio_timeline = get_raw_portfolio_time()

    resp = kraken_request('/0/private/TradesHistory', {
        "nonce": str(int(1000*time.time())),
        "trades": True
    }, api_key, api_sec)

    asset_prices = {}

    for i in resp.json()["result"]["trades"].values():
        asset_name = i['pair'][:-3]
        asset_prices[asset_name] = requests.get('https://api.kraken.com/0/public/OHLC?pair='+asset_name+'USD&since='+str(raw_portfolio_time[0])+'&interval='+TIME_INTERVAL+'&since='+str(TIME_FRAME))
        if (i['time'] > raw_portfolio_time[0]):
            update_portfolio(i['time'], i['pair'][:-3], i['type'], float(i['cost']), float(i['price']))

    return asset_prices


def assemble_timed_data():
    raw_portfolio_time, portfolio_timeline = get_raw_portfolio_time()
    asset_prices = get_all_trades()
    traded_values = [0] * len(raw_portfolio_time)
    updated_times = ''
    for time in range(len(raw_portfolio_time)):
        for asset in portfolio_timeline[time]:
            quantity = portfolio_timeline[time][asset]
            price = float(asset_prices[asset].json()['result'][asset+'USD'][time][1])
            traded_values[time] = str( float(traded_values[time]) + price * quantity )
        tim = int(asset_prices['DOT'].json()['result']['DOTUSD'][time][0])
        updated_times += (datetime.utcfromtimestamp(tim).strftime('%Y-%m-%d_%H:%M') + ' ')
    traded_values = ' '.join(traded_values)
    return traded_values, updated_times


TIME_FRAME = time.time() - 86400  # DAY IS 86400; WEEK IS 604800
daily_values, daily_times = assemble_timed_data()

TIME_FRAME = time.time() - 604800  # DAY IS 86400; WEEK IS 604800
weekly_values, weekly_times = assemble_timed_data()

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def output():
    return render_template("index.html", weeklyValues=weekly_values, weeklyTimes=weekly_times, dailyValues=daily_values, dailyTimes=daily_times)

if __name__ == "__main__":
	app.run()












