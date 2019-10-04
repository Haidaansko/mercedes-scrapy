# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import urllib

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

from mercedes_scrapper.items import CarItem, MercedesScrapperItem

KEYS = ('url', 'name', 'engine', 'inner', 'price')


class PanavtoSpider(scrapy.Spider):
    name = 'panavto'

    start_url = "https://sales.mercedes-panavto.ru"
    

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_main_page, errback=self.errback, priority=0)


    def parse_main_page(self, response):
        hrefs = response.xpath('//div[@class="classBlocks_list"]/a/@href').getall()
        names = response.xpath('//div[@class="classBlocks_item_title"]/text()').getall()
        prices = response.xpath('//div[@class="classBlocks_item_caption"]/text()').getall()

        for href, price, name in zip(hrefs, prices, names):
            url = urllib.parse.urljoin(self.start_url, href)
            model_item = MercedesScrapperItem(**{'url' : url, 'name': name, 'price': price, 'cars': []})
            yield scrapy.Request(url, callback=self.parse_models, errback=self.errback, meta={'model_item': model_item.copy(), 'name': name})


    def parse_models(self, response):
        model_item = response.meta['model_item']
        name = response.meta['name']
        hrefs = response.xpath('//div[@class="paging_all"]/a/@href').getall()
        for href in hrefs:
            url = urllib.parse.urljoin(self.start_url, href)
            yield scrapy.Request(url, callback=self.parse_model_page, errback=self.errback, meta={'model_item': model_item.copy(), 'name': name})
        for elem in self.parse_model_page(response):
            yield elem


    
    def parse_model_page(self, response):
        model_item = response.meta['model_item'] 
        try:
            model_urls = list(map(lambda x: urllib.parse.urljoin(self.start_url, x), response.xpath('//div[@class="offersList_model_title"]/a/@href').getall()))
            model_names = list(map(lambda x: x.strip(), response.xpath('//div[@class="offersList_model_title"]/a/text()').getall()))
            model_engines = list(map(
                lambda x: ''.join(x.xpath('./text()').getall()), 
                response.xpath('//div[@class="offersList_item"]/div[@class="offerslist_engine"]')))
            model_inner = response.xpath('//div[@class="offersList_item"]/div[@class="offerslist_salon"]/text()').getall()
            model_price = list(map(lambda x: x.xpath('./noindex/div/text()').getall(), response.xpath('//div[@class="offersList_item"]/div[@class="offerslist_cost"]')))
            cars = list(map(lambda x: CarItem(**dict(zip(KEYS, x))), zip(model_urls, model_names, model_engines, model_inner, model_price)))
            if len(cars):
                for car in cars:
                    yield scrapy.Request(car['url'], callback=self.parse_car_page, errback=self.errback, meta={'car_item': car, 'model_item': model_item.copy()}, priority=900)
            else:
                model_item['cars'] = []
                yield model_item
            
        except Exception as e:
            print(e)

    
        

    def parse_car_page(self, response):
        car_item = response.meta['car_item']
        model_item = response.meta['model_item']
        car_item['start'], car_item['monthly'] = response.xpath('//div[@class="offerCard_special_credit"]/*/li/text()').getall()
        car_item['special'] = response.xpath('//div[@class="offerCard_special_also"]/*/li/text()').getall()
        model_item['cars'] = dict(car_item)
        yield model_item


    def errback(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


