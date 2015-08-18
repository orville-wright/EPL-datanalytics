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

gw = 20
class fixturesSpider(Spider):
   name = "fixtures"
   allowed_domains = ["premierleague.com"]

   def start_requests(self):
      for u in range(1, 7):
         gw = u
         print "SCANNING gameweek: [ %d ] URL: [ %d ]..." % (gw, u)
         yield Request('http://fantasy.premierleague.com/fixtures/' + str(u) +'/', self.parse)

   def parse(self, response):
      sel0 = Selector(response)
      print "GETTING fixture data for gameweek: [ %d ]" % (gw)
      xx = getfixdata(sel0, gw)
      print "XX = ", xx
      xx+=1

# set xpath point to extract dates & times within the "ism" TR block
# getting the list of dates tells us...
# 1. A count of games that will be played in this weeks gameweek
# 2. the date and time of each game is

def getfixdata(selector, gw):
    sel0 = selector
    xx = gw
    fixchunk = sel0.xpath('//*[@id="ism"]//tr[@class="ismFixture"]//td[1]/text()')
    fixtures = []
    for j, k in enumerate(fixchunk.extract()):
        item = DmozItem()
        a = gethometeam(sel0, j)
        b = getawayteam(sel0, j)
        item['fixdatetime'] = k
        item['fixhometeam'] = a
        item['fixawayteam'] = b
        print "GAMEWEEK: %d - Game: %d starts at: %s - (Home) %s v %s (Away)" % (gw, j+1, k, a, b)
        fixtures.append(item)
    #return fixtures
    xx+=1
    return xx

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
