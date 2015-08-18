import sys
#from scrapy.spider import BaseSpider
#from scrapy.spider import CrawlSpider
#
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse

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

#   for u in range(3, 38):
#       print "scanning gameweek: %d ..." % (u)
       #http_user = 'trashcan_x@yahoo.com'
       ##http_pass = 'sanfran1'
name = "dmoz"
#allowed_domains = ["premierleague.com"]
#start_urls = ['http://fantasy.premierleague.com/fixtures/31/']
#v = str(u)
#start_urls = []
##start_urls.append(q+v)
#print "START_URLS: %s" % start_urls
       #myreq = HtmlResponse(url="XXXXXXXXXX")
       #sel0 = Selector(myreq)
       #getfixdata(sel0)

for u in range(3, 38):
       def parse(self, response):
          print "scanning gameweek: %d ..." % (u)
          myreq = HtmlResponse(url="XXXXXXXXXX")
          sel0 = Selector(response)
          getfixdata(sel0)
          #return

# set xpath point to extract dates & times within the "ism" TR block
# getting the list of dates tells us...
# 1. A count of games that will be played in this weeks gameweek
# 2. the date and time of each game is

def getfixdata(selector):
    sel0 = selector
    fixchunk = sel0.xpath('//*[@id="ism"]//tr[@class="ismFixture"]//td[1]/text()')
    fixtures = []
    for j, k in enumerate(fixchunk.extract()):
        item = DmozItem()
        a = gethometeam(sel0, j)
        b = getawayteam(sel0, j)
        item['fixdatetime'] = k
        item['fixhometeam'] = a
        item['fixawayteam'] = b
        print "Game: %d starts at: %s - (Home) %s v %s (Away)" % (j+1, k, a, b)
        fixtures.append(item)
    return fixtures

def gethometeam(selector, fixnum):
    homechunk = selector.xpath('//*[@id="ism"]//tbody//tr[@class="ismFixture"]//td[@class="ismHomeTeam"]/text()')
    for x, y in enumerate(homechunk.extract()):
        if x == fixnum:
            return y
    return "NOT_FOUND"

def getawayteam(selector, fixnum):
    awaychunk = selector.xpath('//*[@id="ism"]//tbody//tr[@class="ismFixture"]//td[@class="ismAwayTeam"]/text()')
    for n, m in enumerate(awaychunk.extract()):
        if n == fixnum:
            return m
    return "NOT_FOUND"
