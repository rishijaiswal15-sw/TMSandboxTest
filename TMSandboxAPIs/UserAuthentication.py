"""''
This class generates the oauth access token and secret and returns the Authorization error.
It incorporates APIs and Selenium to achieve the OAUTH1 authentication flow.
To authenticate an user from the start, call the method authenticateUser and pass the below parameters
consumer key, consumer secret, user name, password and access scope
If an user has already granted the privileges then invoke generateAccessHeader to generate the authorization header.
Parameters for generateAccessHeader are as below
consumer key, consumer secret, oauth access token and oauth access token secret

''"""
import requests
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class AuthenticationAccess:

    def authenticateUser(self, counsumerKey, consumerSecret, userName, password, accessScope='MyTradeMeRead,MyTradeMeWrite'):
        oauthDict = self.generateTempToken(counsumerKey, consumerSecret, accessScope)
        oauthToken = oauthDict['oauthToken']
        logging.info("Oauth Token= " + oauthToken)
        oauthTokenSecret = oauthDict['oauthTokenSecret']
        logging.info("Oauth Token Secret= " + oauthTokenSecret)
        oauthVerifier = self.getOauthVerifier(oauthToken, userName, password)
        logging.info("Oauth Verifier= " + oauthVerifier)
        header = self.generateAccessToken(counsumerKey, consumerSecret, oauthToken, oauthTokenSecret, oauthVerifier)
        logging.info("Access Header: " + str(header))
        return header

    def generateTempToken(self, consumerKey, consumerSecret, accessScope='MyTradeMeRead,MyTradeMeWrite'):
        oauthTokengenerateURL='https://secure.tmsandbox.co.nz/Oauth/RequestToken?scope='+accessScope
        encodedConsumerSecret=consumerSecret+'%26'
        oauthDetails = 'OAuth  oauth_consumer_key='+consumerKey +\
                       ', oauth_signature_method=PLAINTEXT, oauth_signature='+encodedConsumerSecret
        payload = {}
        header = {
            "Authorization": oauthDetails
        }
        response = requests.request("POST", oauthTokengenerateURL, headers=header, data=payload)
        inputString = response.text
        splitString = inputString.split('&')

        for i in range(len(splitString) - 1):
            tempString = splitString[i].split('=')
            splitString[i] = tempString[1]

        oauthDict = {
            "oauthToken": splitString[0],
            "oauthTokenSecret": splitString[1]
        }
        return oauthDict



    def getOauthVerifier(self, oauthToken, userName, password):
        #userName = 'test@infspark.com'
        #password = 'abc12345'
        driver = webdriver.Chrome(executable_path="D:\\chromedriver.exe")
        url = 'https://secure.tmsandbox.co.nz/Oauth/Authorize?oauth_token='+oauthToken
        driver.get(url)
        driver.implicitly_wait(5)
        email = driver.find_element_by_name("page_email").send_keys(userName)
        password = driver.find_element_by_name("page_password").send_keys(password)
        loginButton = driver.find_element_by_id("LoginPageButton").click()

        getUrl = ''

        try:
            allowButton = driver.find_element_by_id("AllowButton").click()
            getUrl = driver.current_url
        except NoSuchElementException:
            getUrl = driver.current_url

        driver.close()

        splitString = getUrl.split('&')
        temp = splitString[1].split("=")
        oauthVerifier = temp[1]

        return oauthVerifier

    def generateAccessToken(self, consumerKey, consumerSecret, oauthToken, oauthTokenSecret, oauthVerifier):
        accessTokenURL = 'https://secure.tmsandbox.co.nz/Oauth/AccessToken'
        oauthSignature=consumerSecret+'%26'+oauthTokenSecret

        oauthDetails = 'OAuth oauth_verifier='+str(oauthVerifier)+', oauth_consumer_key='+consumerKey +\
                       ', oauth_token='+oauthToken+', oauth_signature_method=PLAINTEXT, oauth_signature='+oauthSignature
        payload = {}
        header = {
            "Authorization": oauthDetails
        }
        response = requests.request("GET", accessTokenURL, headers=header, data=payload)
        inputString = response.text
        splitString = inputString.split('&')

        for i in range(len(splitString)):
            tempString = splitString[i].split('=')
            splitString[i] = tempString[1]

        accessOauthToken = splitString[0]
        accessOauthTokenSecret = splitString[1]
        oauthSignature = consumerSecret + '%26' + accessOauthTokenSecret

        accessAPIOauth = 'OAuth oauth_consumer_key='+consumerKey+', oauth_token='+accessOauthToken +\
                         ', oauth_signature_method=PLAINTEXT, oauth_signature='+oauthSignature
        header = {
            "Authorization": accessAPIOauth
        }
        return header

    def generateAccessHeader(self, consumerKey, consumerSecret, accessOauthToken, oauthTokenSecret):
        oauthSignature = consumerSecret + '%26' + oauthTokenSecret
        accessAPIOauth = 'OAuth oauth_consumer_key=' + consumerKey + ', oauth_token=' + accessOauthToken + \
                         ', oauth_signature_method=PLAINTEXT, oauth_signature=' + oauthSignature
        header = {
            "Authorization": accessAPIOauth
        }
        return header

