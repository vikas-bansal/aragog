#!/usr/bin/env python

##inbuilt modules
import urllib2
import os

## downloaded modules
from bs4 import BeautifulSoup

## local directory holds all local module files
""" Note constructors are called for each module class"""
from local.links import Links
from local.UrlOrdering import UrlOrdering
from local.relevanceCalculator import RelevanceCalculator
#from local.keywordFreq import countWords
from local.googlesearch import google
from local.querySearch import querySearch

##inputs
seeds_file = "inputs/seeds.txt"
keywords_file = "inputs/sampleKeywordList.txt"
surnames_file = "inputs/surnames.txt"
cities_file = "inputs/cities.txt"

#fix filecheck for all above files

keywordsList = {}
urlOrderObj = None
linksObj = None
relevanceCalculatorObj = None
keywords = []
#google search parameters
apiKey = "AIzaSyCO-m_ZU8Z2HKw4xbW1LegZjvAsOABXGL0"
cx  = "016070814652324639602:ajhiexm-yfe" #engine ID

depth = 5


#extracting text from html   
def extractText(soup):
    # Removing Javascript and Css before extracting text
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text().encode("utf-8")

def init():
    #creating object of UrlOrdering class
    global urlOrderObj,linksObj,relevanceCalculatorObj,keywords
    urlOrderObj =  UrlOrdering(keywords_file)
    linksObj = Links()
    relevanceCalculatorObj = RelevanceCalculator(surnames_file,cities_file)
    keywords = getKeywordsFromFile()

def getKeywordsFromFile():
    keywords = []
    with open(keywords_file, 'r') as f:
        for line in f:
            word = line.strip()
            keywords.append(word)
        f.closed
    print keywords
    return keywords


def keywordFrequencyInFile(link):
    fileName = currentFile +'/'+str(link.replace('/','.'))
    countDict = countWords(fileName)
    relevanceCalculatorObj.matchGivenKeywords(countDict, link,currentFile)
    
def crawl(linkDepth,visited, existRobot):
    while urlOrderObj.openLinks:
        try:
            link = urlOrderObj.popLink()
            print "Traversing Link: "+link
            visited[link] = True

            if existRobot and not linksObj.robot_allowed(link):
                print "Returning robot check "+ link
                continue

            response = urllib2.urlopen(link)
            info = response.info()
            mime = info.gettype()
            if 'text' not in mime: #avoiding pdf,ppt etc
                continue
            html = response.read()
            soup = BeautifulSoup(html,from_encoding="utf-8") 
            text = extractText(soup)
            anchorList = linksObj.extractLinks(soup,text)
            print len(anchorList)
            anchorList,rejected = linksObj.validateLinks(anchorList,link)
            print len(anchorList)
            print rejected
            for link in anchorList:
                #print link
                if urlOrderObj.openLinks.get(link) == None and visited.get(link) == None:
                    urlOrderObj.addLink(link)
            #exit()
        except IOError :
                print "IOError reading: "+link
                continue

def getShootQueryResultUrls(domain):
    global keywords
    querySrchObj = querySearch(keywords, domain)
    return querySrchObj.exhaustiveSearch()
    
def getGoogleSearchUrls(domain):
    global apiKey,cx,keywords
    googleResults = {}  
    gobj = google(apiKey,cx)
    for keyword in keywords:
        urls = gobj.apisearch(keyword+"site:"+ domain)
        for i,url in enumerate(urls):
            urls[i] = str(unicode(url))
        googleResults[keyword] = urls
        print "\n"+keyword+"\n"
        print urls
    return googleResults

def findInitialUrlsSet(domain):
    global keywords
    googleResults = getGoogleSearchUrls(domain)
    queryResults = getShootQueryResultUrls(domain)
    mergedResults = {}
    print "Lets Merge"
    for word in keywords:
        mergedResults[word] = googleResults[word]+queryResults[word]
        print "\n" + word
        print mergedResults[word]
    return mergedResults
               
def main():
    global depth,currentFile
    init()
    if not os.path.exists('results'):
        os.makedirs('results')
    counter = 1
    with open(seeds_file, 'r') as f: 
        for seedUrl in f: 
            seedUrl = seedUrl.rstrip().lower()
            if linksObj.isValid(seedUrl):
                domain = linksObj.domainOf(seedUrl)
                if not domain:
                    domain = counter
                    counter = counter+1
                currentFile = 'results/'+domain
                findInitialUrlsSet(seedUrl)
                urlOrderObj.addLink(seedUrl)
                if not os.path.exists(currentFile):
                    os.makedirs(currentFile)
                existRobot = linksObj.robotcheck(seedUrl)
                #crawl(depth,{}, existRobot)
                #relevanceCalculatorObj.createPriortizedUrlFile(currentFile)
main()
