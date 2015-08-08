#from scrapy.spider import BaseSpider
#from scrapy.spider import CrawlSpider
#
from scrapy.spider import Spider
from scrapy.selector import Selector

from tutorial.items import DmozItem

#class DmozSpider(BaseSpider):
class DmozSpider(Spider):

###
# class LoginSpider(BaseSpider):
#    name = 'example.com'
#    start_urls = ['http://www.example.com/users/login.php']
#
#    def parse(self, response):
#        return [FormRequest.from_response(response,
#                    formdata={'username': 'john', 'password': 'secret'},
#                    callback=self.after_login)]
#
#    def after_login(self, response):
#        # check login succeed before going on
#        if "authentication failed" in response.body:
#            self.log("Login failed", level=log.ERROR)
#            return
#
# continue scraping with authenticated session...
###

   DOWNLOADER_MIDDLEWARES = {
       'myproject.middlewares.CustomDownloaderMiddleware': 300,
   }

   http_user = 'david@usakiwi.com'
   http_pass = 'Am3li@++'

   name = "dmoz"
   allowed_domains = ["dmoz.org"]
#   start_urls = ["http://www.premierleague.com/en-gb.html"]
   start_urls = ["http://fantasy.premierleague.com/fixtures/"]

   def parse(self, response):
       sel = Selector(response)
       #sites = sel.xpath('//*[@id="masthead"]/div[2]/div/div[2]/div[1]/ul')
       gameweek = sel.xpath('//*[@id="ismFixtureTable"]/caption')
#
#       clubs = []
#       for site in sites:
#           item = DmozItem()
#           item['clubname'] = site.xpath('a/@title').extract()
#           item['clublink'] = site.xpath('a/@href').extract()
#           item['clublogo'] = site.xpath('@class').extract()
#           clubs.append(item)
#       return clubs
#
       return gameweek
