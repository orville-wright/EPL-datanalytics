import sys
import re
#
import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import FixtureItem
#
import logging

class geteamnameSpider(scrapy.Spider):
   name = "geteamname"
   allowed_domains = ["premierleague.com"]
   logging.basicConfig(level=logging.INFO)
   logging.info('*** _class_ : instantiated')


   def start_requests(self):
      logging.basicConfig(level=logging.INFO)
      logging.info('*** start_requests : Started')

      # control the inital 200 GET and all subsequent GETS. Don't reply on start_urls TAG (which sucks)
      logging.info('*** Exec initial GET')
      yield Request('http://fantasy.premierleague.com', self.parse)


   def parse(self, response):
       logging.info('*** parse : STATE: %s triggered with URL %s' % (response.status, response.url) )

       if response.url == "http://fantasy.premierleague.com/my-team/":
          logging.info('*** Credenitals posted successfully : skipping form FormRequest.post')
          return
       else:
          logging.info('*** Setup credentials form.login.post using URL: %s', response.url)
          return scrapy.FormRequest.from_response(
             response,
             formdata={'email': 'trashcan_x@yahoo.com', 'password': 'sanfran1'},
             dont_click=True,
             callback=self.after_login
          )
       logging.info('*** UNKNONW STATE ***')


   def after_login(self, response):
       logging.info('*** after_login : STATE: %s URL: %s' % (response.status, response.url) )
       yield Request('http://fantasy.premierleague.com/my-points/', self.get_myteam)
       logging.info('*** 2nd GET executed ***')


   def get_myteam(self, response):
       logging.info('*** get_myteam : incomming URL: %s' % response.url )
       if response.url == "http://fantasy.premierleague.com/?fail":
          logging.info('*** ABORTING we are not logged in yet')
          return
       else:
          logging.info("*** SETTING up selector for URL: %s" % response.url)
          sel0 = Selector(response)
          logging.info("*** GETTING team info...")
          user_uuid = response.url.split('/')
          #logging.info('**** url splits - 0:%s 1:%s 2:%s 3:%s 4:%s' % (user_uuid[0], user_uuid[1], user_uuid[2], user_uuid[3], user_uuid[4]) )
          print "Player unique uid: %s" % (user_uuid[4])
          print "Player name; %s" % (sel0.xpath('//*[@id="ism"]/section[2]/h1/text()').extract())
          print "Team name; %s" % (sel0.xpath('//*[@id="ism"]/section[2]/div[1]/h2/text()').extract())
          print "Gameweek points: %s" % (sel0.xpath('//*[@id="ism"]/section[2]/div[2]/div[2]/dl/dd[4]/a/text()').extract())
       return
