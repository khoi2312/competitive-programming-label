import requests
import json

address = 'https://codeforces.com/api/{methodName}'
response = requests.get(address.format(methodName='problemset.problems'))
status = response.json()['status']
result = response.json()['result']

print(status)
with open("data/problems.json", "w") as outfile:
    json.dump(result, outfile)