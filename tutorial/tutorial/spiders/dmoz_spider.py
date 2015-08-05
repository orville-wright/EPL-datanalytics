from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from tutorial.items import DmozItem

class DmozSpider(BaseSpider):

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

   name = "dmoz"
   allowed_domains = ["dmoz.org"]
   start_urls = ["http://www.premierleague.com/en-gb.html"]

   def parse(self, response):
       sel = Selector(response)
       #sites = sel.xpath('//*[@id="masthead"]/div[2]/div/div[2]/div[1]/ul')
       sites = sel.xpath('//*[@id="masthead"]/div[2]/div/div[2]/div[1]/ul/li[*]')
       clubs = []
       for site in sites:
           item = DmozItem()
           item['clubname'] = site.xpath('a/@title').extract()
           item['clublink'] = site.xpath('a/@href').extract()
           item['clublogo'] = site.xpath('@class').extract()
           clubs.append(item)
       return clubs
