# flipkart-webscrapping-selenium

In this project we are going to automate chrome browser using selenium package in python
This is a web based project which has been accomplished using Flask, Selenium, MongoDB, GoogleChromeDriver, Python

### We just have to run app.py file:
  As it is the main app on which our WSGI will run

### The FlipkartScrapping.py file:
  It contains all the necessary modules and model which is used to get the all the information from the Flipkart.com
 
### The mongoDBOperations.py :
  This file consist of necessary MongoDB operations needed to store the collected data
  in the form of arrays as it is NoSQL Database

### The RepositoryForObject.py file:
  This file contains all the Classes, XPath, ID of the HTML tags on flipkart website necessary to lookup so as to 
  gather the information from the flipkart.com website and apply some processing on it get get the productive output


### The requirements.txt file:
  This contains all the required python libraries required in order to run the app
 
###  The properties.txt file:
  This file consist of just a single line for logger.py file import
  whether to log in 'DEBUG' or 'INFO' mode
  
###  The logger_class.py file:
  This file handles and maintains the logger work done ein the application by saving the iformation of log in it
