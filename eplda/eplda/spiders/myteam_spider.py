import sys
import re
import logging
#
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import DmozItem
#

class geteamnameSpider(scrapy.Spider):
   name = "geteamname"
   allowed_domains = ["premierleague.com"]
   start_urls = ['http://fantasy.premierleague.com']

   #def start_requests(self):
   # this is incomplete over-ride code for start_urls object, which I hate using.
   #    print "REQUESTING login URL form..."
   #    yield Request('https://users.premierleague.com/PremierUser/account/login.html', self.parse)
   #    yield Request('http://fantasy.premierleague.com/', self.parse)

   def parse(self, response):
       logging.info('*** start_urls.parse triggered with URL %s', response.url)

       # this is incorrect now that only main login URL is being passed
       # either delete it or clean it up

       if response.url == "http://fantasy.premierleague.com/my-team/":
          logging.info('*** Credenitals posted successfully : skipping form FormRequest.post')
          return
       else:
          logging.info('*** Setup credential form.login.post using URL: %s', response.url)
          return scrapy.FormRequest.from_response(
             response,
             formdata={'email': 'trashcan_x@yahoo.com', 'password': 'sanfran1'},
             dont_click=True,
             #callback=self.after_login
             callback=self.get_myteam
          )
       logging.warning('*** UNKNONW STATE ***')
       return

   def get_myteam(self, response):
        if response.url == "http://fantasy.premierleague.com/?fail":
           logging.info('*** ABORTING as we are not logged in yet')
        else:
           logging.info("*** LOGGED IN get_myteam using URL: %s" % response.url)
           logging.info("*** SETTING up response.selector for URL: %s" % response.url)
           sel0 = Selector(response)
           logging.info("*** GETTING team info...")
           user_uuid = response.url.split('/')
           print "Player unique uid: %s" % (user_uuid[4])
           print "Player name; %s" % (sel0.xpath('//*[@id="ism"]/section[2]/h1/text()').extract())
           print "Team name; %s" % (sel0.xpath('//*[@id="ism"]/section[2]/div[1]/h2/text()').extract())
           print "Gameweek points: %s" % (sel0.xpath('//*[@id="ism"]/section[2]/div[2]/div[2]/dl/dd[4]/a/text()').extract())
        return
