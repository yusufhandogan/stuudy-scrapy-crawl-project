import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'universal',
   'user_agent_type': 'desktop_chrome',
   'url': 'https://www.bachelorsportal.com/studies/455877/comic-and-concept-art.html?ref=search_card#content:fees_and_funding'
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