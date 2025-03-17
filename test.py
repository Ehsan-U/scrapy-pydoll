import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_pydoll.page import PageMethod
from pydoll.constants import By



class TestSpider(scrapy.Spider):
    name = "test"


    def start_requests(self):
        url = "http://quotes.toscrape.com/js/"
        yield scrapy.Request(url, callback=self.parse, meta={
            "pydoll": True,
            "pydoll_page_methods": [
                PageMethod("wait_element", By.XPATH, "//div[@class='quote']"),
            ]
        })

    def parse(self, response):
        for author in response.xpath("//small/text()").getall():
            yield {
                "author": author
            }


process = CrawlerProcess(settings={
    "DOWNLOAD_HANDLERS": {
        "http": "scrapy_pydoll.handler.PydollDownloadHandler",
        "https": "scrapy_pydoll.handler.PydollDownloadHandler",
    },
    "PYDOLL_HEADLESS": True,
    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
})
process.crawl(TestSpider)
process.start()