from scrapy import Spider, Request
from yelp.items import YelpItem
import re

class YelpSpider(Spider):
	name = 'yelp_spider'
	allowed_urls = ['https://www.yelp.com/']
	start_urls = ['https://www.yelp.com/search?find_desc=&find_loc=Houston%2C+TX&ns=1']

	def parse(self, response):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		text = response.xpath('//span[@class = " css-1e4fdj9"]/text()').extract()
		total = 24
		#_, _, total = map(lambda x: int(x), re.findall('\d+', text))
		
		# list comprehension to construct all the urls
		result_urls = ['https://www.yelp.com/search?find_desc=&find_loc=Houston%2C+TX&ns=' + str(x) for x in range(0, total, 1)]

		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):
		# This function parses the search result page

		# We are looking for the url of the detail page
		restaurant_urls_ending = response.xpath('//a[@class="css-1422juy"]/@href').extract()[1:]
		
		# Manually concatenate all the urls
		restaurant_urls = ['https://www.yelp.com' + url for url in restaurant_urls_ending]

		#print(restaurant_urls)
		# Yield the requests to the restaurant pages,
		# using parse_restaurant_page function to parse the response
		for url in restaurant_urls:
			#print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\",url)
			yield Request(url=url, callback=self.parse_restaurant_page, meta = {
				'current_url':url
				})

	def parse_restaurant_page(self, response):
		current_url = response.meta['current_url']
		# so we can append
		truncated_url = re.search('^[^?]+', current_url)[0]
		# Find the total number of reviews so that we can decide how many urls to scrape next
		text = response.xpath('//span[@class = " css-1e4fdj9"]/text()').extract()
		total = int(text[-1].split(' ')[-1])
		print(total)
		#total = map(lambda x: int(x), re.findall('\d+', text))
		#total = int(re.findall('\d+', text)[0])
		restaurant_review_urls = [truncated_url + '?start=' + str(x) for x in range(0, total, 10)]
		print(restaurant_review_urls)
		# Yield the requests to the restaurant reviews pages,
		# using parse_restaurant_reviews_page function to parse the response
		for url in restaurant_review_urls:
			yield Request(url=url, callback=self.parse_restaurant_reviews_page)

	def parse_restaurant_reviews_page(self, response):
		reviews_text = response.xpath('//span[@class = " raw__09f24__T4Ezm"]/text()').extract()
		print(reviews_text)
		restaurant = response.xpath('//h1[@class = "css-1x9iesk"]/text()').extract_first()
		print(restaurant)
		#address = response.xpath('//div[@class="mapbox"]//address/text()').extract_first().strip()
		#price = response.xpath('//span[@class="business-attribute price-range"]/text()').extract_first()
		for review in reviews_text:
		#	rating = review.xpath('.//div[@class="biz-rating biz-rating-large clearfix"]/div/div/@title').extract_first()[0]
		#	text = review.xpath('.//p[@lang="en"]/text()').extract()
		#	date = review.xpath('.//span[@class="rating-qualifier"]/text()').extract_first().strip()

			item = YelpItem()
			item['restaurant'] = restaurant
		#	item['rating'] = rating
			item['text'] = review
		#	item['date'] = date
		#	item['address'] = address
		#	item['price'] = price
			yield item

















