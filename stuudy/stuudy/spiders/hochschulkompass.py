import scrapy
from urllib.parse import urljoin
import pandas as pd
from dotenv import load_dotenv
import os


class HochschulkompassSpider(scrapy.Spider):
    name = "hochschulkompass"

    # Proxy bilgilerini ayarlayalım
    proxy = os.getenv("PROXY_URL")
    allowed_domains = ["hochschulkompass.de"]

    custom_settings = {
        "CONCURRENT_REQUESTS": 5000,            # Aynı anda gönderebileceği istek sayısını artır
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1000, # Aynı domaine gönderebileceği maksimum istek sayısı
        # "DOWNLOAD_DELAY": 0.1,                # İstekler arasında çok kısa bir gecikme (daha fazla yüklenmeyi önlemek için)
        "AUTOTHROTTLE_ENABLED": False,         # Trafik sıkışıklığını önlemek için otomatik hız ayarı
        # "AUTOTHROTTLE_START_DELAY": 0.5,      # İlk isteklerde bekleme süresi
        # "AUTOTHROTTLE_MAX_DELAY": 3,          # Yoğun trafiğe karşı bekleme süresini artır
        # "AUTOTHROTTLE_TARGET_CONCURRENCY": 10, # Paralel istek sayısını dengeleme
        "RETRY_ENABLED": True,                # Hatalı isteklerde yeniden deneme ayarı
        "RETRY_TIMES": 20,                     # Hatalı isteklerde yeniden deneme sayısı
        "DOWNLOAD_TIMEOUT": 60,               # Bir isteğin maksimum bekleme süresi (saniye)
        "REACTOR_THREADPOOL_MAXSIZE" : 20
        
    }

    start_urls = [
        "https://www.hochschulkompass.de/studium/studiengangsuche/erweiterte-studiengangsuche/search/1/studtyp/3.html"
    ]

    # Linkleri saklamak için liste
    program_links_list = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_program_list,
                method="GET",
                meta={"proxy": self.proxy},
            )

    def parse_program_list(self, response):
        content = response.body.decode("utf-8", errors="ignore")

        from scrapy import Selector

        response = Selector(text=content)

        # Tüm program linklerini çekiyoruz (section etiketleri içerisinde)
        sections = response.xpath('//div[@class="clearfix result-section"]/section')
        
        for section in sections:
            # Her bir section içinde 'Mehr Erfahren' linkini çekiyoruz
            link = section.xpath('.//a[@class="btn-info btn"]/@href').get()
            if link:
                full_link = urljoin("https://www.hochschulkompass.de/", link)
                self.program_links_list.append(full_link)
                print("link çekildi:\n", full_link)

        # Sonraki sayfaya geçiş
        next_page = response.xpath(
            '//*[@id="c9905"]/div/section/footer/div[2]/ul/li[9]/a/@href'
        ).get()

        if next_page:
            next_page_url = urljoin("https://www.hochschulkompass.de/", next_page)
            yield scrapy.Request(
                url=next_page_url,
                method="GET",
                callback=self.parse_program_list,
                meta={"proxy": self.proxy},
            )
        else:
            # Son sayfadaysak veriyi CSV dosyasına kaydet
            self.save_to_csv()

    def save_to_csv(self):
        """Program linklerini CSV formatında kaydet."""
        df = pd.DataFrame(self.program_links_list, columns=["Program Links"])
        df.to_csv(
            "hochschulkompass_program_link.csv", index=False, encoding="utf-8-sig"
        )
        self.log("Links saved to hochschulkompass_program_link.csv")
