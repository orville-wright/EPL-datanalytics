import sys
import re
#
import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
from eplda.items import DmozItem

class geteamnameSpider(Spider):
   name = "geteamname"
   allowed_domains = ["premierleague.com"]
   start_urls = ["https://users.premierleague.com/PremierUser/account/login.html",
                "http://fantasy.premierleague.com/my-team/"
                ]

   #def start_requests(self):
   #    print "REQUESTING login URL form..."
   #    #yield Request('https://users.premierleague.com/PremierUser/account/login.html', self.parse)
   #    yield Request('http://fantasy.premierleague.com/', self.parse)

   def parse(self, response):
       print "Setting up login form credentials and auto input using URL: %s" % (response.url)
       #return scrapy.FormRequest.from_response(
       return scrapy.FormRequest.from_response(
           response,
           formdata={'ismEmail': 'orville.wright@yahoo.com', 'id_password': 'sanfran1'},
           #formdata={'ismEmail': 'orville.wright@yahoo.com', 'password': 'sanfran1'},
           #formdata={'email': 'orville.wright@yahoo.com', 'id_password': 'sanfran1'},
           #formdata={'email': 'orville.wright@yahoo.com', 'password': 'sanfran1'},
           dont_click=True,
           #callback=self.after_login
           callback=self.get_myteam
      )

   def after_login(self, response):
        # check login succeed before going on
        print "CHECKING login credentials post status..."
        #print "RESPONSE BODY: %s" % (response.body)
        #if "Error logging in" in response.body:
        #    self.logger.error("Login failed")
        #    print "LOGIN credentials failure !!"
        #    return
        #print "LOGIN credentials entered SUCCESSFULLY !!"
        #response = scrapy.Request('http://fantasy.premierleague.com/my-team/')


   def get_myteam(self, response):
        print "GETTING team name - Old URL %s" % (response.url)
        print response.body
        #response2 = scrapy.Request.replace(response.request, url="http://fantasy.premierleague.com/my-team/")
        #print "GETTING team name - New URL %s" % (response2.url)
        sel0 = Selector(response)
        #sel1 = Selector(response2)
        print "GETTING team name..."
        #datachunk = sel0.xpath('//*[@id="ismTeamForm"]/div[1]/div[1]/div[1]/h2/text()')
        myteamname = sel0.xpath('//*[@id="ismTeamForm"]/div[1]/div[1]/div[1]/h2/text()').extract()
        #my-teamname = datachunk.extract()
        print "TEAM NAME is: %s" % (myteamname)
        return
