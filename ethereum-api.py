import requests
import json

base = "http://api.ethplorer.io"
request_url = base + "/getAddressInfo/0x734DFD7d5702634cF1C87f4A6Bc8557C1599150A?apiKey=freekey"
result = requests.get(request_url).json()

tokens = [[token['rawBalance'], token['tokenInfo']['decimals'], token['tokenInfo']['price']['rate'], token['tokenInfo']['address'], token['tokenInfo']['symbol']] for token in result["tokens"]]
tokens_values = []
for token in tokens:
	divider = len(token[0]) - int(token[1])
	integer = int(token[0][:divider]) if token[0][:divider] else 0
	decimals = int(token[0][divider : divider + 3]) / 1000
	value = integer + decimals
	tokens_values.append([token[4], value, value * token[2]])

print(tokens_values)
print(sum(map(lambda t: t[2], tokens_values)))

# GET PRICES EVERYDAY AT MIDNIGHT
#request_url = "http://api.ethplorer.io/getTokenPriceHistoryGrouped/0x8762db106b2c2a0bccb3a80d1ed41273552616e8?apiKey=freekey&period=7"
#result = requests.get(request_url).json()
#print(json.dumps(result, indent=5))













