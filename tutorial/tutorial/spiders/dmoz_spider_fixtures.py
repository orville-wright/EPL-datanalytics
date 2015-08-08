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

   http_user = 'trashcan_x@yahoo.com'
   http_pass = 'sanfran1'

   name = "dmoz"
   allowed_domains = ["dmoz.org"]
#   start_urls = ["http://www.premierleague.com/en-gb.html"]
   start_urls = ["http://fantasy.premierleague.com/fixtures/"]

   def parse(self, response):
       sel = Selector(response)

# set xpath point to extract dates & times withint TR block
       fixchunk = sel.xpath('//*[@id="ism"]//tr[@class="ismFixture"]//td[1]/text()')
       fixtures = []
       for j, k in enumerate(fixchunk.extract()):
           print "Game: ", j, "starts at: ", k

           item = DmozItem()
           item['fixdatetime'] = k
           fixtures.append(item)

#   def parse(self, response):
       sel = Selector(response)
       fixchunk = sel.xpath('//*[@id="ism"]//tbody//td[@class="ismHomeTeam"]/text()')
       for j, k in enumerate(fixchunk.extract()):
           print "Home team: ", k
           item = DmozItem()
           item['fixhometeam'] = k
           fixtures.append(item)

#   def parse(self, response):
       sel = Selector(response)
       fixchunk = sel.xpath('//*[@id="ism"]//tbody//td[@class="ismAwayTeam"]/text()')
       for j, k in enumerate(fixchunk.extract()):
           print "Away team: ", k
           item = DmozItem()
           item['fixawayteam'] = k
           fixtures.append(item)
       return fixtures
