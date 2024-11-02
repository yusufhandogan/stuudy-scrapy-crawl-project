import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'universal',
   'user_agent_type': 'desktop_chrome',
   'url': 'https://www.hochschulkompass.de/studium/studiengangsuche/erweiterte-studiengangsuche/detail/all/search/1/studtyp/3.html?tx_szhrksearch_pi1%5BQUICK%5D=1&tx_szhrksearch_pi1%5Bfach%5D='
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('YOUR_USERNAME', 'YOUR_PASSWORD'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())