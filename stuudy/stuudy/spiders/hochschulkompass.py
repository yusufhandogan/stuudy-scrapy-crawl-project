import scrapy
import requests
from pprint import pprint

class OxylabsSpider(scrapy.Spider):
    name = 'oxylabs_spider'
    
    def start_requests(self):
        # Oxylabs API'ye istek göndermek için payload oluşturuyoruz
        payload = {
            'source': 'universal',
            'url': 'https://www.hochschulkompass.de/studium/studiengangsuche/erweiterte-studiengangsuche/search/1/studtyp/3.html',
            'user_agent_type': 'desktop_firefox',
            'context': [
                {'key': 'http_method', 'value': 'get'}
            ],
            'render': 'html',
            "Content-Type": "text/html;charset=utf-8"
        }
        
        # POST isteğini Oxylabs API'ye atıyoruz
        response = requests.post(
            'https://realtime.oxylabs.io/v1/queries',
            auth=('stuudy_zWPLe', 'u5AHbsI2M=A78'),
            json=payload
        )
        
        # Yanıtı JSON formatında alıyoruz
        data = response.text
        
        # Yanıtı Scrapy ile işlemek için parse metoduna gönderiyoruz
        pprint(data)  # Yanıtı yazdırıyoruz
    
    def parse(self, response):
        pass
