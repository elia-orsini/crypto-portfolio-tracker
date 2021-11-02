import requests
import json

def get_chartdata(address, chain_id):
	base = "https://api.covalenthq.com"
	key = "ckey_c9ff6042010f4c8e923c9e21615"
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








