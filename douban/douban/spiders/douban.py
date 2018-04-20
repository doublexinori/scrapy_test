import scrapy,json,re,time
from bs4 import BeautifulSoup
from douban.items import DoubanItem

class doubanSpider(scrapy.Spider):
	name = 'douban'
	allowed_domains = ['movie.douban.com']
	start_urls = ['https://movie.douban.com/']
	
	def parse(self, response):
		main_url="https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=动画,日本&start=0"
		yield scrapy.Request(url = main_url, callback = self.parse_getid)
	
	def parse_getid(self,response):
		data = json.loads(response.body.decode("utf-8"))["data"][0]
		page_num = str(response.url)[str(response.url).rfind('=') +1:len(str(response.url))]
		item = DoubanItem()
		item['title'] = data['title']
		item['directors'] = str(data['directors']).replace("['","").replace("']","")
		item['rate'] = data['rate']
		item['star'] = data['star']
		item['id'] = data['id']
		#print(item)
		yield item
		if int(page_num) < 10:
			start = int(page_num) + 1
			new_main_url = str(response.url).replace('start='+page_num,'start='+str(start))
			time.sleep(15)
			yield scrapy.Request(url=new_main_url, callback=self.parse_getid)