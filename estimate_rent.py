import requests

url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=7318+MIDDLEBURY+PL+CHARLOTTE+NC+28212'

resp = requests.get(url, stream=True)
print(resp.text)