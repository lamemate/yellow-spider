# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector

from yellow.items import YellowItem


class YellowCrawlerSpider(CrawlSpider):
    name = 'yellow_crawler'
    allowed_domains = ['gelbeseiten.de']
    start_urls = [
        "http://www.gelbeseiten.de/wohnungsverwaltung/berlin",
        "http://www.gelbeseiten.de/wohnungsgenossenschaften/berlin",
        "http://www.gelbeseiten.de/wohnungsgesellschaften/berlin",
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="gs_seite_vor_wrapper"]/a')), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        for box in response.xpath('//div[@class="box"]'):
            item = YellowItem()
            item['name'] = box.xpath('div//span[@itemprop="name"]/text()').extract()
            item['streetAddress'] = box.xpath('div//span[@itemprop="streetAddress"]/text()').extract()
            item['postalCode'] = box.xpath('div//span[@itemprop="postalCode"]/text()').extract()
            item['addressLocality'] = box.xpath('div//span[@itemprop="addressLocality"]/text()').extract()
            item['mail'] = box.xpath('div//span[@itemprop="email"]/text()').extract()
            item['website'] = box.xpath('div//div[contains(@class, "B")]//li[contains(@class, "website")]/a/span/text()').extract()
            yield item
