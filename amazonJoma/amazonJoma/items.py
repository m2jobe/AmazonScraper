# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonjomaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jomaBrand = scrapy.Field()
    jomaProductName = scrapy.Field()
    jomaProductID = scrapy.Field()
    jomaRetailPrice = scrapy.Field()
    jomaPromotedPrice = scrapy.Field()
    jomaUrl = scrapy.Field()
    #jomaReviews = scrapy.Field()
    
    #amazonTitle = scrapy.Field()
    #amazonPrice = scrapy.Field()
    #amazonReview = scrapy.Field()
    #amazonStars = scrapy.Field()
    #amazonRetailer = scrapy.Field()
    #amazonComp1Name = scrapy.Field()
    #amazonComp1Price = scrapy.Field()
    #amazonComp2Name = scrapy.Field()
    #amazonComp2Price = scrapy.Field()
    #amazonComp3Name = scrapy.Field()
    #amazonComp3Price = scrapy.Field()
    #amazonUrl = scrapy.Field()
    ashfordName = scrapy.Field()
    ashfordBrand = scrapy.Field()
    ashfordRetailPrice = scrapy.Field()
    ashfordPromoPrice = scrapy.Field()
    ashfordID = scrapy.Field()
    ashfordUrl = scrapy.Field()
