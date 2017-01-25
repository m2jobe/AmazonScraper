



# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from amazonJoma.items import AmazonjomaItem
from difflib import SequenceMatcher


LISTVAL = 5200


script = """
function main(splash)
  splash:on_request(function(request)
    request:set_proxy{
        host = "tor",
        port = 9050,
        type = 'HTTP',
    }
  end)

  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    http_status = last_response.status,
    html = splash:html(),
  }
end
"""

class AmazonSpider(scrapy.Spider):
    #http_user = "spidy" only needed if you set up authentication for your splash servers
    #http_pass = "spiderman"
    name = "amazon"
    allowed_domains = ["amazon.com", "jomashop.com"]
    #start_urls = ['http://amazon.com/']

    inp = 'url.txt'
    data = open(inp)
    dat = data.read()
    url = dat.splitlines()

    inp1 = 'name.txt'
    data1 = open(inp1)
    dat1 = data1.read()
    prodName = dat1.splitlines()

    inp2 = 'retailPrice.txt'
    data2 = open(inp2)
    dat2 = data2.read()
    retailPrice = dat2.splitlines()

    inp3 = 'promoPrice.txt'
    data3 = open(inp3)
    dat3 = data3.read()
    promoPrice = dat3.splitlines()

    inp4 = 'brand.txt'
    data4 = open(inp4)
    dat4 = data4.read()
    brand = dat4.splitlines()

    inp5 = 'id.txt'
    data5 = open(inp5)
    dat5 = data5.read()
    id = dat5.splitlines()

    inp6 = 'reviews.txt'
    data6 = open(inp6)
    dat6 = data6.read()
    reviews = dat6.splitlines()

    def access_only(self):
      global LISTVAL
      return int(LISTVAL)

    def increment(self):
        global LISTVAL
        LISTVAL = LISTVAL+1

    def start_requests(self):

    
        yield scrapy.Request("https://www.amazon.com/dp/1482703270/" , self.parse_result_page, dont_filter=True, meta={
                    'splash': {
                'args': {
                        'html': 0,
                        'png': 0,
                        'lua_source': script,
                        'timeout': 100,

                },
                'endpoint': 'render.json',
            }, 
         }) 


    def parse_result_page(self, response):
      #if LISTVAL < 7 :
       jomaBrand = self.brand[LISTVAL]
       jomaProductName = self.prodName[LISTVAL]
       jomaProductID = self.id[LISTVAL]
       jomaRetailPrice = self.retailPrice[LISTVAL]
       jomaPromotedPrice = self.promoPrice[LISTVAL]
       jomaUrl = self.url[LISTVAL]
       jomaReviews = self.reviews[LISTVAL]

      

       if response.xpath('//*[@id="noResultsTitle"]/text()').extract():
            print "No results"
            print response.url
       else: 
            if response.xpath('//*[@id="productTitle"]/text()').extract_first() or response.xpath('//*[@id="title"]/text()').extract_first():
                comic = AmazonjomaItem() 
                jomaBrand = response.meta.get('jomaBrand')
                jomaProductName = response.meta.get('jomaProductName')
                jomaProductID = response.meta.get('jomaProductID')
                jomaRetailPrice = response.meta.get('jomaRetailPrice')
                jomaPromotedPrice = response.meta.get('jomaPromotedPrice')
                jomaUrl = response.meta.get('jomaUrl')
                jomaReviews = response.meta.get('jomaReviews')
                comic['jomaBrand'] = jomaBrand
                comic['jomaProductName'] = jomaProductName
                comic['jomaProductID'] = jomaProductID
                comic['jomaRetailPrice'] = jomaRetailPrice
                comic['jomaPromotedPrice'] = jomaPromotedPrice
                comic['jomaUrl'] = jomaUrl
                comic['jomaReviews'] = jomaReviews
                comic['amazonUrl'] = response.url
                comic['amazonComp1Name'] = "N/A"
                comic['amazonComp2Name'] = "N/A"
                comic['amazonComp3Name'] = "N/A"
                comic['amazonComp1Price'] = "N/A"
                comic['amazonComp2Price'] = "N/A"
                comic['amazonComp3Price'] = "N/A"
                if response.xpath('//*[@id="price-shipping-message"]').extract_first():
                   comic['amazonRetailer'] = "amazon"
                elif response.xpath('//*[@id="soldByThirdParty"]/b').extract_first():
                   comic['amazonRetailer'] = response.xpath('//*[@id="soldByThirdParty"]/b').extract_first()
                if response.xpath('//*[@id="productTitle"]/text()').extract_first():
                    comic['amazonTitle'] = response.xpath('//*[@id="productTitle"]/text()').extract_first()
                elif response.xpath('//*[@id="title"]/text()').extract_first():
                    comic['amazonTitle'] = response.xpath('//*[@id="title"]/text()').extract_first()        
                else :
                    comic['amazonTitle'] = "N/A"

                if response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first():
                        comic['amazonPrice'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()  
                else :
                        comic['amazonPrice'] = "N/A"
            
                if response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first():
                        comic['amazonReview'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
                else :
                        comic['amazonReview'] = "N/A"

                if response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first():
                        comic['amazonStars'] = response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first()
                else :
                        comic['amazonStars'] = "N/A"

                if response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[2]/span[2]').extract_first():
                        comic['amazonComp1Name'] = response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                        comic['amazonComp1Price'] = response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[1]/span[1]/text()').extract_first()


                if response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[2]/span[2]').extract_first():
                        comic['amazonComp2Name'] = response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                        comic['amazonComp2Price'] = response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[1]/span[1]/text()').extract_first()

                if response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[2]/span[2]').extract_first():
                        comic['amazonComp3Name'] = response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                        comic['amazonComp3Price'] = response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[1]/span[1]/text()').extract_first()
            



                yield comic


            if response.xpath('//*[@id="result_0"]/div/div[3]/div/a/h2/text()').extract():
                searchStringResult = response.xpath('//*[@id="result_0"]/div/div[3]/div/a/h2/text()').extract_first()
                matchPerc = SequenceMatcher(None, jomaProductName, searchStringResult ).ratio()
                print "Joma name: " + jomaBrand
                print "Joma prod name: " + jomaProductName
                print "Joma prod id: " + jomaProductID
                print "Joma prod list val: " + str(LISTVAL)
                print "Match perc: " +str(matchPerc)
                print response.url
                if matchPerc > 0.50 :
                        print "Fetching page"
                	if response.xpath('//*[@id="result_0"]/div/div[3]/div[2]/a/@href').extract_first():
                                print "Processing Page"
                		yield scrapy.Request(response.xpath('//*[@id="result_0"]/div/div[3]/div[2]/a/@href').extract_first(), self.parse_final_result, dont_filter=True, meta={
                                                'splash': {
                                                        'args': {
                                                                'html': 1,
                                                                'png': 0,
                                                                'lua_source': script,
                                                                'timeout': 200,

                                                                                            },
                                                        'endpoint': 'render.json'
                                                }, 'jomaProductName' : jomaProductName, 'jomaBrand' : jomaBrand, 'jomaProductID' : jomaProductID, 'jomaRetailPrice' : jomaRetailPrice, 'jomaPromotedPrice' : jomaPromotedPrice, 'jomaUrl' : jomaUrl, 'jomaReviews' : jomaReviews
                                 })
       self.increment()
       jomaBrand = self.brand[LISTVAL]
       jomaProductName = self.prodName[LISTVAL]
       jomaProductID = self.id[LISTVAL]
       jomaRetailPrice = self.retailPrice[LISTVAL]
       jomaPromotedPrice = self.promoPrice[LISTVAL]
       jomaUrl = self.url[LISTVAL]
       jomaReviews = self.reviews[LISTVAL]
       keyword = jomaBrand + " " + jomaProductName +  " " + jomaProductID
       yield scrapy.Request("https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dfashion&field-keywords="+ keyword.decode('unicode_escape').encode('ascii','ignore'), self.parse_result_page, dont_filter=True, meta={
                'splash': {
                        'args': {
                            'html': 1,
                            'png': 0,
                            'lua_source': script,
                            'timeout': 100,

                    },
                    'endpoint': 'render.json',
            },
       })
    
    def parse_final_result(self, response):
        print "Final processing..."

        jomaBrand = response.meta.get('jomaBrand')
        jomaProductName = response.meta.get('jomaProductName')
        jomaProductID = response.meta.get('jomaProductID')
        jomaRetailPrice = response.meta.get('jomaRetailPrice')
        jomaPromotedPrice = response.meta.get('jomaPromotedPrice')
        jomaUrl = response.meta.get('jomaUrl')
        jomaReviews = response.meta.get('jomaReviews')
        if response.xpath('//*[@id="availability"]/span/a/@href').extract():
            print "Alternative sellers processing.."
            href = response.xpath('//*[@id="availability"]/span/a/@href').extract_first()
            yield scrapy.Request("https://www.amazon.com" + (href), self.parse_deeper_page, dont_filter=True, meta={
                                'splash': {
                                        'args': {
                                                'html': 1,
                                                'png': 0,
                                                'lua_source': script,
                                                'timeout': 100,

                                                            },
                                        'endpoint': 'render.json'
                                }, 'jomaProductName' : jomaProductName, 'jomaBrand' : jomaBrand, 'jomaProductID' : jomaProductID, 'jomaRetailPrice' : jomaRetailPrice, 'jomaPromotedPrice' : jomaPromotedPrice, 'jomaUrl' : jomaUrl, 'jomaReviews' : jomaReviews
                        })
        else : 
            comic = AmazonjomaItem() 
            comic['jomaBrand'] = jomaBrand
            comic['jomaProductName'] = jomaProductName
            comic['jomaProductID'] = jomaProductID
            comic['jomaRetailPrice'] = jomaRetailPrice
            comic['jomaPromotedPrice'] = jomaPromotedPrice
            comic['jomaUrl'] = jomaUrl
            comic['jomaReviews'] = jomaReviews
            comic['amazonUrl'] = response.url
            comic['amazonComp1Name'] = "N/A"
            comic['amazonComp2Name'] = "N/A"
            comic['amazonComp3Name'] = "N/A"
            comic['amazonComp1Price'] = "N/A"
            comic['amazonComp2Price'] = "N/A"
            comic['amazonComp3Price'] = "N/A"
            if response.xpath('//*[@id="price-shipping-message"]').extract_first():
           	   comic['amazonRetailer'] = "amazon"
            elif response.xpath('//*[@id="soldByThirdParty"]/b').extract_first():
    	       comic['amazonRetailer'] = response.xpath('//*[@id="soldByThirdParty"]/b').extract_first()
            elif response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first():
                comic['amazonRetailer'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first()

            if response.xpath('//*[@id="productTitle"]/text()').extract_first():
        	   comic['amazonTitle'] = response.xpath('//*[@id="productTitle"]/text()').extract_first()
            elif response.xpath('//*[@id="title"]/text()').extract_first():
                comic['amazonTitle'] = response.xpath('//*[@id="title"]/text()').extract_first()
            elif response.xpath('//*[@id="olpProductDetails"]/div[1]/h1/text()').extract_first():     
                comic['amazonTitle'] = response.xpath('//*[@id="olpProductDetails"]/div[1]/h1/text()').extract()           
            else :
        		comic['amazonTitle'] = "N/A"

            if response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first():
                    comic['amazonPrice'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()  
            else :
                    comic['amazonPrice'] = "N/A"
    	
            if response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first():
                    comic['amazonReview'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
            else :
                    comic['amazonReview'] = "N/A"

            if response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first():
                    comic['amazonStars'] = response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first()
            else :
                    comic['amazonStars'] = "N/A"

            if response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[2]/span[2]').extract_first():
                    comic['amazonComp1Name'] = response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                    comic['amazonComp1Price'] = response.xpath('//*[@id="mbc"]/div[2]/div/span[2]/div/div[1]/span[1]/text()').extract_first()


            if response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[2]/span[2]').extract_first():
                    comic['amazonComp2Name'] = response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                    comic['amazonComp2Price'] = response.xpath('//*[@id="mbc"]/div[3]/div/span[2]/div/div[1]/span[1]/text()').extract_first()

            if response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[2]/span[2]').extract_first():
                    comic['amazonComp3Name'] = response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[2]/span[2]/text()').extract_first()
                    comic['amazonComp3Price'] = response.xpath('//*[@id="mbc"]/div[4]/div/span[2]/div/div[1]/span[1]/text()').extract_first()
    	
            if response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first():
                    comic['amazonComp1Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first()
                    comic['amazonComp1Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[1]/span[1]/text()').extract_first()


            if response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[4]/h3/span/a/text()').extract_first():
                    comic['amazonComp2Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[4]/h3/span/a/text()').extract_first()
                    comic['amazonComp2Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[1]/span[1]/text()').extract_first()

            if response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[4]/h3/span/a/text()').extract_first():
                    comic['amazonComp3Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[4]/h3/span/a/text()').extract_first()
                    comic['amazonComp3Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[1]/span[1]/text()').extract_first()


            yield comic 

    def parse_deeper_page(self, response):
        print "Alternative processing now"


        comic = AmazonjomaItem() 
        jomaBrand = response.meta.get('jomaBrand')
        jomaProductName = response.meta.get('jomaProductName')
        jomaProductID = response.meta.get('jomaProductID')
        jomaRetailPrice = response.meta.get('jomaRetailPrice')
        jomaPromotedPrice = response.meta.get('jomaPromotedPrice')
        jomaUrl = response.meta.get('jomaUrl')
        jomaReviews = response.meta.get('jomaReviews')
        comic['jomaBrand'] = jomaBrand
        comic['jomaProductName'] = jomaProductName
        comic['jomaProductID'] = jomaProductID
        comic['jomaRetailPrice'] = jomaRetailPrice
        comic['jomaPromotedPrice'] = jomaPromotedPrice
        comic['jomaUrl'] = jomaUrl
        comic['jomaReviews'] = jomaReviews
        comic['amazonUrl'] = response.url
        comic['amazonComp1Name'] = "N/A"
        comic['amazonComp2Name'] = "N/A"
        comic['amazonComp3Name'] = "N/A"
        comic['amazonComp1Price'] = "N/A"
        comic['amazonComp2Price'] = "N/A"
        comic['amazonComp3Price'] = "N/A"
        if response.xpath('//*[@id="price-shipping-message"]').extract_first():
           comic['amazonRetailer'] = "amazon"
        elif response.xpath('//*[@id="soldByThirdParty"]/b').extract_first():
           comic['amazonRetailer'] = response.xpath('//*[@id="soldByThirdParty"]/b').extract_first()
        elif response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first():
            comic['amazonRetailer'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first()
        
        if response.xpath('//*[@id="productTitle"]/text()').extract_first():
            comic['amazonTitle'] = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        elif response.xpath('//*[@id="title"]/text()').extract_first():
            comic['amazonTitle'] = response.xpath('//*[@id="title"]/text()').extract_first()  
        elif response.xpath('//*[@id="olpProductDetails"]/div[1]/h1/text()').extract_first():     
            comic['amazonTitle'] = response.xpath('//*[@id="olpProductDetails"]/div[1]/h1/text()').extract_first()   
        else :
            comic['amazonTitle'] = "N/A"

        if response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first():
                comic['amazonPrice'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()  
        else :
                comic['amazonPrice'] = "None"
    
        if response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first():
                comic['amazonReview'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        else :
                comic['amazonReview'] = "N/A"

        if response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first():
                comic['amazonStars'] = response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract_first()
        else :
                comic['amazonStars'] = "None"

        if response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first():
                comic['amazonComp1Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[4]/h3/span/a/text()').extract_first()
                comic['amazonComp1Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[2]/div[1]/span[1]/text()').extract_first()


        if response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[4]/h3/span/a/text()').extract_first():
                comic['amazonComp2Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[4]/h3/span/a/text()').extract_first()
                comic['amazonComp2Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[4]/div[1]/span[1]/text()').extract_first()

        if response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[4]/h3/span/a/text()').extract_first():
                comic['amazonComp3Name'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[4]/h3/span/a/text()').extract_first()
                comic['amazonComp3Price'] = response.xpath('//*[@id="olpOfferList"]/div/div/div[6]/div[1]/span[1]/text()').extract_first()
    



        yield comic 
