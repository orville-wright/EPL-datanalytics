import sys
import re
#
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import DmozItem
#
import logging

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

      #print "*** Checking game results"
      logging.info('*** Checking game results')
      result0 = sel0.xpath('//*[@id="ismFixtureTable"]/tbody/tr[*]/td[4]/text()')
#      print "Game state: %s" % (result0)

      for m, n in enumerate(result0.extract()):
         if n == "v":
            print "Game %s has not been played yet" % (m+1)
         else:
            print "Game %s has been played & result is: %s" % (m+1, n)

      # first we need to see if the game has been played.
      # becasue there are 2 different & complex webpage forms for both class of games
      # if the score != [u'v'] ... (basically a "v") then the game has been played, so
      # we need to use the vmore complex xpath expression
      # otherwise we use the simple xpath
      #
      # xpaths...
      # score state:  //*[@id="ismFixtureTable"]/tbody/tr[*]/td[4]/text().extract()
      # fixture date info (not played): //*[@id="ism"]//tr[@class="ismFixture"]//td[1]/text()
      # fixture date info (played): //*[@id="ismFixtureTable"]/tbody/tr[@class="ismFixture ismResult"]/td[1]/text()')
      #
      
      fixchunk = sel0.xpath('//*[@id="ism"]//tr[@class="ismFixture"]//td[1]/text()')
      #fixchunk = sel0.xpath('//*[@id="ismFixtureTable"]/tbody/tr[*]/td[1]')
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
    #homechunk = selector.xpath('//*[@id="ismFixtureTable"]/tbody/tr[1]/td[2]/text()')
    for x, y in enumerate(homechunk.extract()):
        if x == fixnum:
            return y
    return "NOT_FOUND"

def getawayteam(selector, fixnum):
    awaychunk = selector.xpath('//*[@id="ism"]//tbody//tr[@class="ismFixture"]//td[@class="ismAwayTeam"]/text()')
    #awaychunk = selector.xpath('//*[@id="ismFixtureTable"]/tbody/tr[1]/td[6]/text()')
    for n, m in enumerate(awaychunk.extract()):
        if n == fixnum:
            return m
    return "NOT_FOUND"
