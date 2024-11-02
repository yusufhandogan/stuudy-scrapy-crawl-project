import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'universal',
   'parse': True,
   'user_agent_type': 'desktop_chrome',
   'url': 'https://www.educations.com/institutions/university-of-law-online-undergraduate/online-llb-hons-law',
   'render': 'html'
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('EMAIL', 'YOUR_PASSWORD'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())