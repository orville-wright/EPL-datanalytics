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

   def start_requests(self):
      logging.basicConfig(level=logging.INFO)
      logging.info('*** Started: fixtures')

      for u in range(1, 7):
         gw = u
         # the game week is the number at the end of the fixtures URL
         # so construct the URL and pass it to he request
         yield Request('http://fantasy.premierleague.com/fixtures/' + str(u) +'/', self.parse)

   def parse(self, response):
      sel0 = Selector(response)
      gw_url = response.url
      # extract the gameweek that we are scanning, i.e. the number at the end of the fixtures URL
      gw = int(re.sub(r'\D', "", gw_url))

      # check to see is game has been played or is pending.
      # a pending game has no score and has a "v" in the score field
      #logging.info('*** Checking game results')
      result0 = sel0.xpath('//*[@id="ismFixtureTable"]/tbody/tr[*]/td[4]/text()')

      for m, n in enumerate(result0.extract()):
         if n == "v":
            k = get_up_date(sel0, m+1)
            a = get_up_hometeam(sel0, m+1)
            b = get_up_awayteam(sel0, m+1)
            print "Gameweek: %d - Game %s unplayed - starts at: %s - (Home) %s v %s (Away)" % (gw, m+1, k, a, b)
         else:
            k = get_pd_date(sel0, m+1)
            a = get_pd_hometeam(sel0, m+1)
            b = get_pd_awayteam(sel0, m+1)
            c = get_pd_score(sel0, m+1)
            print "Gameweek: %d - Game %s played - started at: %s - (Home) %s %s %s (Away)" % (gw, m+1, k, a, c, b)

      # load array, or sore in mongodb database
      fixtures = []
      item = DmozItem()
      item['fixdatetime'] = k
      item['fixhometeam'] = a
      item['fixawayteam'] = b
      fixtures.append(item)
      return

# functions for unplayed fixtures
# a simple schema
# _up_ = unplayed
#
def get_up_date(selector, gamenum):
    #logging.info('get_unplayed_date(): gamenum = %s' % (gamenum))
    result1 =  selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[1]/text()') % (gamenum))
    k = result1.extract()
    return k

def get_up_hometeam(selector, gamenum):
    #logging.info('get_unplayed_date(): gamenum = %s' % (gamenum))
    result1 =  selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[2]/text()') % (gamenum))
    k = result1.extract()
    return k

def get_up_awayteam(selector, gamenum):
    #logging.info('get_unplayed_date(): gamenum = %s' % (gamenum))
    result1 =  selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[6]/text()') % (gamenum))
    k = result1.extract()
    return k

# functions for played fixtures
# a much more complex schema where the info is embedded deeply & obscurely inside the webpage
# _pd_ = played
#
def get_pd_date(selector, gamenum):
    if ( gamenum == 1 ):
       #logging.info('*** odd line detected ***')
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[1]/text()') % (gamenum))
       k = result1.extract()
       return k
    else:
       rownum = ((gamenum-1)+gamenum)
       #logging.info('*** even line detected ***')
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[1]/text()') % (rownum))
       k = result1.extract()
       return k

def get_pd_hometeam(selector, gamenum):
    if ( gamenum == 1 ):
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[2]/text()') % (gamenum))
       k = result1.extract()
       return k
    else:
       rownum = ((gamenum-1)+gamenum)
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[2]/text()') % (rownum))
       k = result1.extract()
       return k

def get_pd_score(selector, gamenum):
    if ( gamenum == 1 ):
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[4]/text()') % (gamenum))
       k = result1.extract()
       return k
    else:
       rownum = ((gamenum-1)+gamenum)
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[4]/text()') % (rownum))
       k = result1.extract()
       return k

def get_pd_awayteam(selector, gamenum):
    if ( gamenum == 1 ):
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[6]/text()') % (gamenum))
       k = result1.extract()
       return k
    else:
       rownum = ((gamenum-1)+gamenum)
       result1 = selector.xpath(('//*[@id="ismFixtureTable"]/tbody/tr[%d]/td[6]/text()') % (rownum))
       k = result1.extract()
       return k
