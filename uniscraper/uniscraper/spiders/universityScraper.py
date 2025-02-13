import scrapy
from scrapy.crawler import CrawlerProcess

class UniversityscraperSpider(scrapy.Spider):
    name = "universityScraper"
    allowed_domains = ["yokatlas.yok.gov.tr"]

    def __init__(self, arananUni="KOÇ ÜNİVERSİTESİ", bolumKodu="10206", *args, **kwargs):
        super(UniversityscraperSpider, self).__init__(*args, **kwargs)
        self.arananUni = arananUni
        self.bolumKodu = bolumKodu
        self.start_urls = [f"https://yokatlas.yok.gov.tr/netler-tablo.php?b={bolumKodu}"]

    def parse(self, response):
        uniler = response.css('tr')
        for uni in uniler:
            try:
                uniName = uni.css("td small a::text").get()
                uniType = uni.css("td::text").getall()[1]
                tytTurkceNet = uni.css("td::text").getall()[6]
                tytSosyalNet = uni.css("td::text").getall()[7]
                tytMatNet = uni.css("td::text").getall()[8]
                tytFenNet = uni.css("td::text").getall()[9]
                aytMatNet = uni.css("td::text").getall()[10]
                aytFizikNet = uni.css("td::text").getall()[11]
                aytKimyaNet = uni.css("td::text").getall()[12]
                aytBiyoNet = uni.css("td::text").getall()[13]
                if self.arananUni in uniName:
                    yield {
                        "Üniversite adı": uniName, "Üniversite tipi": uniType, "TYT Türkçe Net": tytTurkceNet,
                        "TYT Sosyal": tytSosyalNet, "TYT Mat": tytMatNet, "TYT Fen": tytFenNet,
                        "AYT Mat": aytMatNet, "AYT Fizik": aytFizikNet, "AYT Kimya": aytKimyaNet,
                        "AYT Biyoloji": aytBiyoNet}
                    return
            except:
                pass


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEEDS': {
            "yks.json": {
                "format": "json",
                "encoding": "utf-8",
                "overwrite": True,
            }
        }
    })
    process.crawl(UniversityscraperSpider)
    process.start()
