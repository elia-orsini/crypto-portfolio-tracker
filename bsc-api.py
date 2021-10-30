import requests
import json

base = "https://api.covalenthq.com"
key = "ckey_c9ff6042010f4c8e923c9e21615"
address = "0x734DFD7d5702634cF1C87f4A6Bc8557C1599150A"

url = base + "/v1/56/address/" + address + "/balances_v2/?key=" + key
result = requests.get(url).json()

#print(json.dumps(result, indent=6))

tokens = [[token['balance'], token['contract_decimals'], token['quote_rate'], token['contract_address'], token['contract_ticker_symbol']] for token in result['data']["items"]]
tokens_values = []
for token in tokens:
	if token[4] == 'ETH':
		continue
	divider = len(token[0]) - int(token[1])
	integer = int(token[0][:divider]) if token[0][:divider] else 0
	decimals = int(token[0][divider : divider + 3]) / 1000 if token[0][divider : divider + 3] else 0
	value = integer + decimals
	
	if token[2]:
		tokens_values.append([token[4], value, value * token[2]])

print(tokens_values)
print(sum(map(lambda t: t[2], tokens_values)))












