# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

#class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
#    pass


class FixtureItem(Item):
    fixnum = Field()
    fixdatetime = Field()
    fixhometeam = Field()
    fixawayteam = Field()
    fixplayed = Field()
    fixwin = Field()
    fixscore = Field()
    fixscorea = Field()
    fixscoreh = Field()
