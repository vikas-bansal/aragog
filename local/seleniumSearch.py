from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urlparse import urlparse, urlunparse,urljoin
from bs4 import BeautifulSoup
from links import Links

import re
import urllib2

class querySearch:

    def __init__(self, keywords, domain):
        self.keywords = keywords
        self.domain = domain
        self.srchInterface = []
        self.radioInterface = []
        self.chkboxInterface = []
        self.driver = None
        self.linksObj = Links()
        self.srchResults = {}
        self.srchIdFound = True

    def getInputInterfaces(self):
        response = urllib2.urlopen(self.domain)
        html = response.read()
        soup = BeautifulSoup(html,from_encoding="utf-8")
        # Search all input elements: searchbox, radioBtn, checkbox
        inputInterfaces = soup.find_all('input')
        for interface in inputInterfaces:
            if interface.get('type') == "text" or interface.get('type') == "search":
                if interface.get('id') != None:
                    self.srchInterface.append(interface.get('id'))
                else:
                    self.srchInterface.append(interface.get('name'))
                    self.srchIdFound = False
            elif interface.get('type')== "radio":
                self.radioInterface.append(interface.get('id'))
            elif interface.get('type') == "checkbox":
                self.chkboxInterface.append(interface.get('id'))

    def exhaustiveSearch(self):
        self.getInputInterfaces()
        self.driver = webdriver.Firefox()
        #In chrome you may need to install chromedriver at path given below if !present
        #self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver.get(self.domain)
        srchInterface = self.srchInterface
        radioInterface = self.radioInterface
        chkboxInterface = self.chkboxInterface
        print srchInterface
        print radioInterface
        print chkboxInterface
        for searchId in srchInterface:
            if radioInterface:
                for radioId in radioInterface:
                    self.driver.execute_script("document.getElementById(arguments[0]).checked = true;",radioId)
                    if chkboxInterface:
                        for chkboxId in chkboxInterface:
                            self.driver.execute_script("document.getElementById(arguments[0]).checked = true;",chkboxId)
                            self.shootQuery(searchId)
                    else:
                        self.shootQuery(searchId)
            else:
                if chkboxInterface:
                    for chkboxId in chkboxInterface:
                        self.driver.execute_script("document.getElementById(arguments[0]).checked = true;",chkboxId)
                        self.shootQuery(searchId)
                else:
                     self.shootQuery(searchId)

        return self.srchResults
                        

    def shootQuery(self, srchInterfaceId):
        keywords = self.keywords
        if self.srchIdFound == True:
            inputElement = self.driver.find_element_by_id(srchInterfaceId)
        else:
            inputElement = self.driver.find_element_by_name(srchInterfaceId)
        print keywords
        inputElement.send_keys(keywords[0])
        inputElement.send_keys(Keys.ENTER)
        url = self.driver.current_url
        for word in keywords:
            newUrl = re.sub(keywords[0],word,url)
            print newUrl
            response1 = urllib2.urlopen(newUrl)
            html1 = response1.read()
            soup1 = BeautifulSoup(html1,from_encoding="utf-8")
            text = self.extractText(soup1)
            urls = self.linksObj.extractLinks(soup1,text)
            #print soup1
            print "\n"+word  
            print "\n URLS: "
            print urls
            #print "\n REJECTED: "
            #print rejectedUrls        
            if word in self.srchResults:
                self.srchResults[word] += urls
            else:
                self.srchResults[word] = urls
            #print self.srchResults[word]
        self.driver.get(self.domain)
        

    def extractText(self, soup):
        # Removing Javascript and Css before extracting text
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text().encode("utf-8")
        
