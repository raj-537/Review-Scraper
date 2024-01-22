from logging import raiseExceptions
import random
from sys import executable
from matplotlib.style import available

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository

from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np
import os
from mongoDBOperations import MongoDBManagement

class FlipkartScrapper:
    def __init__(self, chrome_options):
    #def __init__(self):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        self.chrome_options = chrome_options
        try:

            

            self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),  chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f'(__init__): Something went wrong on initialsing webdriver object.\n',str(e))
        
    def getDriver(self):
        try:
            return self.driver
        except Exception as e:
            raise Exception(str(e))

    def refresh_driver(self):
        try:
            self.driver.refresh()
        except Exception as e:
            raise Exception(str(e))

    def waitExplicitlyForCodition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 2, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located(By.CLASS_NAME, element_to_be_found)
            )

            return True
        except Exception:
            return False
    
    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            return self.driver.current_url
        except Exception as e:
            raise Exception(f"(getCurrentWindowUrl) - Something went wrong on retrieving current url.\n" + str(e))
        
    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f'(getLocatorsObject): Could not get the locator.\n'+str(e))
    
    def findElementByXPath(self, xpath):
        """
        This function finds the web element using xpath passed
        """

        try:
            
            self.driver.implicitly_wait(10)
            element = self.driver.find_element(By.XPATH, xpath)
            return element
        except Exception as e:
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    
    def findElementByClass(self, class_name):
        """
        This function finds web element using Classpath provided
        """

        try:
            #self.driver.refresh()
            element = self.driver.find_element(By.CLASS_NAME, class_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementByClass) - CLASS provided was not found.\n" + str(e))
    
    def findElementsByTag(self, tag_name):
        """
        This function finds web element using TAGPATH provided
        """

        try:
            #self.driver.refresh()
            element = self.driver.find_elements(By.TAG_NAME, tag_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementByTag) - TAG provided was not found.\n" + str(e))


    
    def findElementsByClass(self, class_name):
        """
        This function finds all the web elements using Classpath provided
        """

        try:
            #self.driver.refresh()
            element = self.driver.find_elements(By.CLASS_NAME, class_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementsByClass) - CLASS provided was not found.\n" + str(e))

    
    def findElementsByCSSSelector(self, element_name):
        """
        This function finds all the web elements using CSSSelector provided
        """

        try:
            self.driver.refresh()
            element = self.driver.find_elements(By.CSS_SELECTOR, element_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementsByCSSSelector) - CSS provided was not found.\n" + str(e))

        
    def openURL(self, url):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """

        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))

    
    def login_popup_handle(self):
        """
        This function handle/closes the login popup displayed.
        """

        try:
            self.wait()
            locator = self.getLocatorsObject()
            self.findElementByXPath(locator.getLoginCloseButton()).click()
            return True
        
        except Exception as e:
            raise Exception("(login_popup_handle) - Failed to handle popup.\n" + str(e))
    

    def searchProduct(self, search_string):
        """
        This function helps to search product using search string provided by the user
        """

        try:
            locator = self.getLocatorsObject()
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            _ = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, locator.getInputSeacrhArea()))).send_keys(search_string)
            # seacrh_box = locator.getInputSeacrhArea()
            # self.findElementByXPath(seacrh_box).send_keys(search_string)
            self.driver.implicitly_wait(5)
            search_button = locator.getSearchButton()
            button = self.findElementByXPath(search_button)
            button.click()
            
            self.driver.implicitly_wait(5)
            #self.driver.refresh()
            return True
        except Exception as e:
            raise Exception(f"(searchProduct) - Something went wrong on searching.\n" + str(e))


    def generateTitle(self, seacrh_string):
        """
        This function generatesTitle for the products searched using search string
        :param search_string: product to be searched for.
        """

        try:
            title = seacrh_string + "- Buy Products Online at Best Price in India - All Categories | Flipkart.com"
            return title
        except Exception as e:
            raise Exception(f"(generateTitle) - Something went wrong while generating complete title.\n" + str(e))
    

    def getProductLinks(self):
        """
        This function returns all the list of links.
        """
        
        try:
            #locator = ObjectRepository()
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            _ = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions)\
                                    .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, '_10Ermr')))
            links = []
            actual_link = []
            self.driver.refresh()
            all_links = self.findElementsByTag('a')

            for link in all_links:
                links.append(link.get_attribute('href'))
            
            count = 0
            for link in links:
                if count>15:
                    break
                if '?pid=' in link:
                    count += 1
                    actual_link.append(link)
            
            return actual_link
        except Exception as e:
            raise Exception(f"(getProductLinks) - Something went wrong on getting link from the page."+str(e))
        
    
    def getActualProducts(self):
        """
        This function returns the actual product links after filtering.
        """
        try:
            product_links = []
            count = 0
            
            for link in self.getProductLinks():
                if count>15:
                    break
                if '?pid=' in link:
                    product_links.append(link)
                    count+=1
                else:
                    continue
            return product_links
        except Exception as e:
            raise Exception(f"(actualProductLinks) - Something went wrong while searching the url.\n" + str(e))


    def getExpectedCountForLooping(self, expected_review):
        """
        This functoin retrives the total number of pages which should be searched for review
        """
        try:
            expected_count = expected_review / 10
            return int(expected_count)
        except Exception as e:
            raise Exception(f"(getExpectedCountForLooping) - Something went wrong with review count.\n" + str(e))

    def getLinkForExpectedReviewCount(self, expected_review_count, search_string):
        """
        This function extracts the link of product having more than expected count.
        """
        try:
            product_links = self.getActualProducts()
            count = 0
            expected_counts = self.getExpectedCountForLooping(expected_review_count)

            while count < expected_counts:
                url_to_hit = product_links[random.randint(0, len(product_links)-1)]
                self.openURL(url_to_hit)
                total_review_page = self.getTotalReviewPage()
                count = total_review_page
            self.openURL(url_to_hit)
            return True
        except Exception as e:
            raise Exception(
                f"(getLinkForExpectedReviewCount) - Failed to retrive the link for product having more than "
                f"{expected_review_count} expected count of review.\n" + str(
                    e))
        
    
    def isElementVisible(self,element_to_be_checked):
        try:
            if element_to_be_checked in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(isElementVisible) - Not able to check for the element.\n" + str(e))
    

    def getProductName(self):
        """
        This function helps to retrieve actual name of the product.
        """

        try:
            locator = self.getLocatorsObject()
            product_element = locator.getProductNameByClass()
            if self.isElementVisible(product_element):
                product_name = self.findElementByClass(product_element).text
            else:
                product_name = self.findElementByXPath(locator.getProductNameByXpath)
            print(product_name)
            return product_name
        
        except Exception as e:
            raise Exception(f"(getProductName) - Not able to get the product name.\n" + str(e))


    
    def getProductSearched(self, search_string):
        """
        This function returns the name of product searched
        """
        try:
            return search_string
        except Exception:
            return search_string
    
    def getPrice(self):
        """
        This function helps to retrieve the original price of the product.
        """

        try:
            locator = self.getLocatorsObject()
            original_price = self.findElementByClass(locator.getOriginalPriceUsingClass()).text
            return original_price

        except Exception as e:
            #raise Exception(f"(getPrice) - Not able to get the price of product.\n" + str(e))
            return "Product Price not available"

    
    def getDiscountPercent(self):
        """
        This function returns discounted percent for the product.
        """
        try:
            locator = self.getLocatorsObject()
            discounted_price = self.findElementByClass(locator.getDiscountPrice()).text
            return discounted_price
        except Exception:
            return "No Discount"
        
    
    def checkForMoreOffers(self):
        """
        This function checks whether more offer links is provided for the product or not.
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreOffers() in self.driver.page_source:
                return True
            else:
                 return False
        except Exception as e:
            raise Exception(f"(checkMoreOffer) - Trouble in finding more offer link.\n" + str(e))


    def clickOnMoreOffers(self):
        """
        This function clicks on more offer button.
        """

        try:
            if self.checkForMoreOffers():
                locator = self.getLocatorsObject()
                self.findElementByClass(locator.getMoreOffers()).click()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(clickOnMoreOffer) - Not able to click on more offer button.\n" + str(e))

    
    def getAvailableOffers(self):
        """
        This function returns offers available
        """

        try:
            locator = self.getLocatorsObject()
            self.driver.refresh()
            if self.checkForMoreOffers():
                
                self.clickOnMoreOffers()
            offers = locator.getAvailableOffers()
            if  offers[0] in self.driver.page_source:
                offer_details = self.findElementByClass(locator.getAvailableOffers()[0])
                return offer_details
            elif offers[1] in self.driver.page_source:
                offer_details = self.findElementByClass(locator.getAvailableOffers()[1])
                return offer_details
            elif offers[2] in self.driver.page_source:
                offer_details = self.findElementByClass(locator.getAvailableOffers()[2])
                return offer_details
            else:
                offers_details = "No offer for the product"
            return offers_details
        except Exception as e:
            raise Exception(f'(getAvailableOffer): - Not able Not able to get the offer details of product.\n' + str(e))
    
    def getOfferDetails(self):
        """
        This function returns the offers in formatted way.
        """
        try:
            available_offers = self.getAvailableOffers()
            
            return str(available_offers.text).replace('\n','.  ')
        except Exception:
            return "No offer Available"
    
    def isEMIAvailable(self):
        """
        This function returns boolean value for EMI is available or not.
        """
        try:

            locator  = self.getLocatorsObject()

            if locator.getViewPlanLinkUsingClass() in self.driver.page_source:
                return True
            else:
                return False
            
        except Exception as e:
            raise Exception(f"(checkViewPlanForEMI) - Error on finding view plans link for EMI.\n" + str(e))

    
    def getEMIDetails(self):
        """
        This function returns EMI details of the product.
        """

        try:
            locator  = self.getLocatorsObject()

            if self.isEMIAvailable():
                emi_details = self.findElementByXPath(locator.getEMIDetail()).text
                return emi_details
            else:
                return "NO EMI Plans"
        except Exception as e:
            return "NO EMI Plans"
    
    def getTotalReviewPage(self):
        """
        This function retrieves total number of pages available for review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreReviewUsingClass() in self.driver.page_source:
                self.findElementByClass(locator.getMoreReviewUsingClass()).click()
            
            else: return int(1)

            total_review_page = [self.findElementByClass(locator.getTotalReviewPage()).text][0]
            #total_page_review contains 1 to last_page
            #and nav_bar for page traversal like next
            #and previous page_no
            split_values = total_review_page.split('\n')
            value = str(split_values[0]).split()[-1]
            return int(value)
        except Exception as e:
            return int(1)


    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(2)
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))
    
    def getRatings(self):
        """
        This function gets rating for the product.
        """
        try:
            locator = self.getLocatorsObject()
            ratings = self.findElementsByCSSSelector(locator.getRatings())
            return ratings
        except Exception as e:
            raise Exception(f"(getRatings) - Not able to get the rating details of product.\n" + str(e))

    def ClickIfAble(self,more_comments):
        try:
            more_comments.click()
        except Exception:
            pass

    def getComments(self):
        """
        This function gets review comment for the product
        """

        try:
            locator = self.getLocatorsObject()
            if locator.getReadMoreClass() in self.driver.page_source:
                read_more_in_comments = self.findElementsByClass(locator.getReadMoreClass())
                

                [self.ClickIfAble(read_more) for read_more in read_more_in_comments]
            
            self.driver.implicitly_wait(5)
            if locator.getComment() in self.driver.page_source:
                comments = self.findElementsByClass(locator.getComment())
                return comments
            else:
                return 'No comments present'
        
        except Exception as e:
            return 'No comments present'
            #raise Exception(f"(getComment) - Not able to get the comment details of product.\n" + str(e))


            
    
    def getCustomerNameReviewAge(self):
        """
        This function gets customername for the review
        """
        try:
            locator = self.getLocatorsObject()
            
            review_age_names = self.findElementsByClass(locator.getAgeOfReviewAndName())
            return review_age_names
        except Exception as e:
            raise Exception(f"(getCustomerNamesAndReviewAge) - Not able to get the name of product.\n" + str(e))

    
    def checkForNextPageLink(self):
        """
        This function click on the next page for the review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getNextFromTotalReviewPage() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkForNextPageLink) - Not able to click on next button.\n" + str(e))


    def getReviewDeatilsForProduct(self):
        """
        This function gets all Review Details for the product
        """

        try:
            ratings, comments, names, review_age = [],[],[],[]
            
            ratings.append([i.text if not isinstance(i,str) else i for i in self.getRatings()])
            
            
            for i in self.getComments():
                if not isinstance(i,str):
                    comments.append([i.text])
                    
            if (len(ratings)-len(comments))!=0:
                for i in range(len(ratings)-len(comments)-1):
                    comments.append(['No Comments'])


            

            # comments.append([i.text if not isinstance(i,str) for i in self.getComments()])
            review_age_names = self.getCustomerNameReviewAge()
            for i in range(len(review_age_names)):
                if not isinstance(review_age_names[i],str):
                    if(i%2!=0):
                        review_age.append(review_age_names[i].text)
                    else:
                        names.append(review_age_names[i].text)
                

            #review_age = [[reviewAge.text for reviewAge in review_age]]
            review_age = [review_age]
            names = [names]
            return  ratings, comments, names, review_age
        except Exception as e:
            raise Exception(f"(getReviewDetailsForProduct) - Something went wrong on getting details of review for the product.\n" + str(e))


    def generatingResponse(self, product_searched, product_name, price, discount_price, offer_details, EMI, result):
        """
        This function generates the final response to send.
        """

        try:
            response_dict = {"product_searched": [], "product_name": [], "price": [], "discount_price": [],
                             "offer_details": [], "EMI": [], "ratings": [], "comments": [], "customer_name": [],
                             "review_Age": []}

            ratings, comments, names, review_age = result[0], result[1], result[2], result[3]
            response_dict['ratings'] = ratings
            response_dict["comments"] = comments
            response_dict["customer_name"] = names
            response_dict["review_Age"] = review_age
            response_dict["product_name"] = product_name
            response_dict["product_searched"] = product_searched
            response_dict["offer_details"] = offer_details
            response_dict["EMI"] = EMI
            response_dict["price"] = price
            response_dict["discount_price"] = discount_price
            return response_dict
        except Exception as e:
            raise Exception(f"(generatingResponse) - Something went wrong on generating response")


    def generateDataForColumnAndFrame(self, response):
        """
        This function generates data for the column where only single data is presented. And then frames it in data frame.
        """
        try:
            
            
            count = 0
            dict_value = {'product_searched':[],
             'product_name':[],
             'price':[],
             'discount_price':[],
             'offer_details':[],
             'EMI':[]}
            
            for i in response['ratings']:
                for column_name, _ in response.items():
                    if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_price' or  column_name == 'EMI' or column_name == 'offer_details':
                        dict_value[column_name].extend([str(response[column_name])]*len(i))
                
                        
            data_frame1 = pd.DataFrame(dict_value)
            
            return data_frame1
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def frameToDataSet(self, response):
        """
        This function frames the column to dataframe.
        """
        dict_value = {'ratings' : [], 'customer_name' : [], 'comments':[], 'review_Age' : []}
        try:
            
            for column_name, _ in response.items():
                if column_name == 'ratings' or column_name == 'customer_name' or column_name == 'review_Age' or column_name=='comments':
                    dict_value[column_name] = response[column_name][0]
                
            return pd.DataFrame(dict_value)
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def createDataFrameIncludingAllColumn(self, response):
        """
        This function creates dataframe from given data.
        """
        try:
            data_frame1 = self.generateDataForColumnAndFrame(response=response)
            data_frame2 = self.frameToDataSet(response=response)
            frame = [data_frame1, data_frame2]
            data_frame = pd.concat(frame, axis=1)
            return data_frame
        except Exception as e:
            raise Exception(f"(createDataFrame) - Something went wrong on creating data frame.\n" + str(e))

    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))

    def getReviewsToDisplay(self, searchString, username, password):
        """
        This function returns the review and other detials of product
        """
        try:
            searchString = str(searchString).replace(' ','')
            link_count = 0
            
            mongoClient = MongoDBManagement(username=username, password=password)
            self.driver.implicitly_wait(5)
            locator = self.getLocatorsObject()
            self.driver.implicitly_wait(5)
            links = self.getProductLinks()
            
            for link in links:
                if link_count>7:
                    break
                link_count += 1
                print('reviewing: ' + str(link))

                self.openURL(url=link)
                if locator.getCustomerName() in self.driver.page_source:
                    product_name = self.getProductName()

                    db_search = mongoClient.findFirstRecord(db_name="Flipkart-Scrapper",
                                                            collection_name=searchString,
                                                            query={'product_name': product_name})
                    print(db_search)
                    if db_search is not None:
                        print("Yes present" + str(len(db_search)))
                        #return True



                    else:
                        ratings_main = []
                        comments_main = []
                        names_main = []
                        reviews_age_main = []
                        print("False")
                        product_searched = self.getProductSearched(search_string=searchString)
                        price = self.getPrice()
                        offer_details = self.getOfferDetails()
                        discount_price = self.getDiscountPercent()
                        EMI = self.getEMIDetails()
                        total_review = self.getTotalReviewPage()
                        count = 0
                        
                        product_page_url = self.driver.current_url
                        while count < total_review:
                            if count >7:
                                break
                            
                            self.openURL(product_page_url+'&page='+str(count+1))
                            ratings,comment,customer_name,review_age = self.getReviewDeatilsForProduct()
                            ratings_main.extend(ratings[0])
                            names_main.extend(customer_name[0])
                            comments_main.extend(comment)
                            reviews_age_main.extend(review_age[0])
                            count = count+1

                        response = self.generatingResponse(product_searched,product_name, price, discount_price,offer_details,EMI,([ratings_main],[comments_main],[names_main],[reviews_age_main]))

                        _  =  mongoClient.insertRecord(db_name="Flipkart-Scrapper",
                                                     collection_name=searchString,
                                                     record=response)
            return searchString
                        
        except Exception as e:
            raise Exception(f"(getReviewsToDisplay) - Something went wrong on yielding data.\n" + str(e))













        
