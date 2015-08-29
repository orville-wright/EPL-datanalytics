import sys
import re
#
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import DmozItem

class fixturesSpider(Spider):
   name = "fixtures"
   allowed_domains = ["premierleague.com"]
   login_page = 'https://users.premierleague.com/premierUser/account/login.html'

   def start_requests(self):
      for u in range(3, 7):
         gw = u
         print "SCANNING gameweek: [ %d ] URL: [ %d ]..." % (gw, u)
         # the game week is the number at the end of the fixtures URL
         # so construct the URL and pass it to he request
         yield Request('http://fantasy.premierleague.com/fixtures/' + str(u) +'/', self.parse)

   def parse(self, response):
      sel0 = Selector(response)
      gw_url = response.url
      # extract the gameweek that we are scanning, i.e. the number at the end of the fixtures URL
      gw = int(re.sub(r'\D', "", gw_url))
      print "GETTING fixture data for gameweek: [ %d ]" % (gw)
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
      return

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
