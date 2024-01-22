class ObjectRepository:

    def __init__(self) :
        print()

    def getUsernameForMonogoDB(self):
        username = 'kj'
        return username
    
    def getPasswordforMongoDB(self):
        return 'Kymo007'
    
    def getLoginCloseButton(self):
        login_close_button = '//body[1]/div[2]/div[1]/div[1]/button[1]'
        return login_close_button
    
    def getInputSeacrhArea(self):
        search_area = '/html/body/div/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input'
        return search_area

    def getElementToBeSeached(self):
        element = '_3704LK'
        return element
    
    def getSearchButton(self):
        search_button = '/html/body/div/div/div[1]/div[1]/div[2]/div[2]/form/div/button'
        return search_button

    def getRatingAndReviewsText(self):
        rating_and_review_text = "//div[contains(text(), 'Ratings & Reviews')]"

    def getProductNameByXpath(self):
        product_name = '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1[1]/span[1]'
        return product_name
    
    def getProductNameByClass(self):
        product_name = 'B_NuCI'
        return product_name
    
    def getProductSearchedByXpath(self):
        product_searched = '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1[1]/span[1]'

    def getOriginalPriceUsingClass(self):
        orginal_price = '_3I9_wc._2p6lqe'
        return orginal_price

    def getOriginalPriceUsingXPath(self):
        original_price = '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]'
        return original_price
    
    def getDiscountPercent(self):
        discount_percent = '_3Ay6Sb _31Dcoz'
        return discount_percent
    
    def getDiscountPrice(self):
        discount_price = '_30jeq3._16Jk6d'
        return discount_price
    
    def getEMIDetail(self):
        emi_detail = '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/span[7]/li/span'
        return emi_detail
    

    def getViewPlanLinkUsingClass(self):
        view_plan = '_3IATq1'
        return view_plan
    
    def getAvailableOffers(self):
        
        available_offers1 = '_3TT44I'
        available_offers2 = 'WT_FyS'
        available_offers3= 'XUp0WS'
        return available_offers1, available_offers2, available_offers3

    def getMoreOffers(self):
        more_offer = 'IMZJg1'
        return more_offer
    
    def getMoreOffersUsingClass(self):
        more_offer = "IMZJg1"
        return more_offer

    def getRatings(self):
        rating = "div._3LWZlK._1BLPMq"
        return rating

    def getComment(self):
        comment = 't-ZTKy'
        return comment

    def getReadMoreClass(self):
        return '_1BWGvX'


    def getCustomerName(self):
        customer_name = '_2sc7ZR _2V5EHH'
        return customer_name
    
    def getAgeOfReviewAndName(self):
        review_age = '_2sc7ZR'
        return review_age

    def getCommentDate(self):
        comment_date = "_2sc7ZR"
        return comment_date

    def getTotalReviewPage(self):
        total_page_1 = "_2MImiq"
        return total_page_1



#
    def getMoreReviewUsingClass(self):
        
        more_review_3 = '_3UAT2v'
        return more_review_3
#
    def getNextFromTotalReviewPage(self):
        next_button = "_1LKTO3"
        return next_button

