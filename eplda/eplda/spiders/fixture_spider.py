import sys
import re
import string
#
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import FixtureItem
#
import pymongo
from pymongo import MongoClient
#
import logging

class fixturesSpider(Spider):
   name = "fixtures"
   allowed_domains = ["premierleague.com"]

   def start_requests(self):
      logging.basicConfig(level=logging.INFO)
      logging.info('*** Started: fixtures')

      # this is the master scan loop.
      # if controls how many times the webpage is scanned and what the webpage/URL is.
      # Eddectively, it controlls which fixture week range you are scanning i.e. range(x, y)
      for u in range(1, 39):
         gw = u
         # the game week is the number at the end of the fixtures URL
         # so construct the URL and pass it to the request method which goes out and
         # pjysically reads the webpage
         yield Request('http://fantasy.premierleague.com/fixtures/' + str(u) +'/', self.parse)

   def parse(self, response):
      # this callback method is triggered after each webpage read operation
      sel0 = Selector(response)
      gw_url = response.url
      # extract the gameweek that we are scanning, i.e. the number at the end of the fixtures URL
      # becasue this is useful for many reasons
      gw = int(re.sub(r'\D', "", gw_url))

      # setup mongodb
      #logging.info('*** Setup mongodb access ***')
      fixclient = MongoClient()
      fixdb = fixclient.football
      fixcol = fixdb.fixtures2015


      # check to see if this game has been played or is pending.
      # a pending game has no score and has a "v" in the score field
      #logging.info('*** Checking game results')
      # _up_ = unplayed game
      # _pd_ = played game
      result0 = sel0.xpath('//*[@id="ismFixtureTable"]/tbody/tr[*]/td[4]/text()')
      for m, n in enumerate(result0.extract()):
         if n == "v":
            k = get_up_date(sel0, m+1)
            a = get_up_hometeam(sel0, m+1)
            b = get_up_awayteam(sel0, m+1)
            c = "-"

            k = tidy_decoded_txt(k)
            a = tidy_decoded_txt(a)
            b = tidy_decoded_txt(b)

            print "Gameweek: %d - Game %s unplayed - starts at: %s - (Home) %s v %s (Away)" % (gw, m+1, k, a, b)
            mongin_fixarray(fixcol, gw, m+1, k, a, b, c, w="-", v="-", h="-")
            #load_fixarray(k, a, b, c)
         else:
            k = get_pd_date(sel0, m+1)
            a = get_pd_hometeam(sel0, m+1)
            b = get_pd_awayteam(sel0, m+1)
            c = get_pd_score(sel0, m+1)

            k = tidy_decoded_txt(k)
            a = tidy_decoded_txt(a)
            b = tidy_decoded_txt(b)
            c = tidy_decoded_txt(c)

            w, h, v = winning_team(c)

            print "Gameweek: %d - Game %s played - started at: %s - (Home) %s %s %s (Away) : Winner: %s" % (gw, m+1, k, a, c, b, w)

            mongin_fixarray(fixcol, gw, m+1, k, a, b, c, w, v, h)


##########################################################
# functions

def mongin_fixarray(fixcol, gw, fn, k, a, b, c, w, v, h):
   # gw = gameweek
   # fn = fixture number
   # k = start date & time
   # a = home team name
   # b = away team name
   # c = score (if game has been played)
   # w = result state of game (Home win, Away win, Draw)
   # v = away team score
   # h = home team score

   # load array, and/or appropriate mongodb collection
   #logging.info('*** loading fixture data into mongo collection ***')
   fixtures = []
   item = FixtureItem()
   item['fixdatetime'] = k
   item['fixhometeam'] = a
   item['fixawayteam'] = b
   item['fixscore'] = c
   item['fixwin'] = w
   fixtures.append(item)

   result = fixcol.insert(
                   { "gameweek": gw,
                     "fixnum": fn,
                     "fixinfo": {
                                  "dateandtime": k,
                                  "hometeam": a,
                                  "awayteam": b,
                                  "winner": w,
                                  "score": c,
                                  "scorea": v,
                                  "scoreh": h
                                }
                   })

   #logging.info('*** Mongo insert result: %s' % (result) )
   return

def load_fixarray(k, a, b, c):
   # load array, and/or appropriate mongodb collection
   logging.info('*** loading array ***')
   fixtures = []
   item = FixtureItem()
   item['fixdatetime'] = k
   item['fixhometeam'] = a
   item['fixawayteam'] = b
   item['fixscore'] = c
   fixtures.append(item)
   print fixtures
   return

def tidy_decoded_txt(dirty_str):
   # since the data we are working with comes from a scraped website
   # its a bit untidy. So strip off all the stuff we dont like.
   #logging.info('*** tidy decoded text : %s' % (dirty_str) )
   x = str(dirty_str)
   clean_str = x.replace("[u'", "").replace("']", "")
   return clean_str

def winning_team(score):
   # decipher who won (Home, Away or Draw) and return the info
   # along with an INTEGER of the goal scored of the home & away team
   x = score.split(' ')
   xhome = int(x[0])
   xaway = int(x[2])
   if xhome > xaway:
      #logging.info('*** HOME wins: %s AWAY: %s ***' % (xhome, xaway) )
      return "hometeam", xhome, xaway
   elif xhome < xaway:
      #logging.info('*** HOME: %s AWAY wins: %s ***' % (xhome, xaway) )
      return "awayteam", xhome, xaway
   else:
      #logging.info('*** HOME: %s AWAY: %s  - DRAW ***' % (xhome, xaway) )
      return "Draw", xhome, xaway


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
