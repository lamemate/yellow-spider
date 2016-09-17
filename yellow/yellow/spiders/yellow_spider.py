# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector

from yellow.items import YellowItem


class YellowSpider(Spider):
	name = "yellow"
	allowed_domains = ["gelbeseiten.de"]
	start_urls = [
		"http://www.gelbeseiten.de/wohnungsverwaltung/berlin",
		"http://www.gelbeseiten.de/wohnungsgenossenschaften/berlin",
		"http://www.gelbeseiten.de/wohnungsgesellschaften/berlin",
		"http://www.gelbeseiten.de/wohnungsunternehmen/berlin"
	]

	def parse(self, response):
		for box in response.xpath('//div[@class="box"]'):
			item = YellowItem()
			item['name'] = box.xpath('div//span[@itemprop="name"]/text()').extract()
			item['streetAddress'] = box.xpath('div//span[@itemprop="streetAddress"]/text()').extract()
			item['postalCode'] = box.xpath('div//span[@itemprop="postalCode"]/text()').extract()
			item['addressLocality'] = box.xpath('div//span[@itemprop="addressLocality"]/text()').extract()
			item['mail'] = box.xpath('div//span[@itemprop="email"]/text()').extract()
			item['website'] = box.xpath('div//div[contains(@class, "B")]//li[contains(@class, "website")]/a/span/text()').extract()
			item['subscriberId'] = box.xpath('div//a[contains(@class, "teilnehmername")]/@href').extract()[0][30:40]
			yield item
