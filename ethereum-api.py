import requests
import json

from flask import Flask, render_template, flash, redirect
from config import Config
from forms import LoginForm


base = "https://api.covalenthq.com"
key = "ckey_c9ff6042010f4c8e923c9e21615"
address = "0x734DFD7d5702634cF1C87f4A6Bc8557C1599150A"
address = "0x734269BF7aC3F3f644Bd4037EDcE162316117625"

def get_chartdata(address, chain_id, key):
	url = base + "/v1/"+ str(chain_id) +"/address/" + address + "/portfolio_v2/?key=" + key
	result = requests.get(url).json()

	times = []
	prices_range = []
	for token_price in result['items']:
		temp = []
		for price_point in token_price['holdings']:
			temp.append(price_point['close']['quote'])
		prices_range.append(temp)

	for time in result['items'][0]['holdings']:
		times.append(time['timestamp'])

	portfolio_value = []
	for i in range(31):
		temp = 0
		for p in prices_range:
			temp += p[i]
		portfolio_value.append(str(temp))

	portfolio_value.reverse()
	times.reverse()
	portfolio_value = ' '.join(portfolio_value)
	times = ' '.join(times)
	return (portfolio_value, times)

(portfolio_valu,time) = get_chartdata(address, 1, key)

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.address.data, form.chain.data))
		try:
			(portfolio_value,times) = get_chartdata(form.address.data, form.chain.data, key)
		except:
			return render_template('login.html', title='Sign In', form=form)
		return render_template("index.html", weeklyValues=portfolio_value, weeklyTimes=times)
	return render_template('login.html', title='Sign In', form=form)

@app.route("/chart")
def output():
	(portfolio_value,times) = get_chartdata(address, form.chain.data, key)
	return render_template("index.html", weeklyValues=portfolio_value, weeklyTimes=times)

if __name__ == "__main__":
	app.run()








