import requests


USERNAME, PASSWORD = 'YOUR_USERNAME', 'YOUR_PASSWORD'


proxies = {
    'http':f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
    'https':f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000'
}

response = requests.request(
    "GET",
    'http://www.hochschulkompass.de/studium/studiengangsuche/erweiterte-studiengangsuche/search/1/studtyp/3.html',
    verify=False,
    proxies=proxies,
)



with open('result.html','w') as f:
    f.write(response.text)