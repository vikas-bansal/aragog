#!/usr/bin/env python

##inbuilt modules
import urllib2
import os

## downloaded modules
from bs4 import BeautifulSoup

## local directory holds all local module files
"""Note constructors are called for each module class"""
from local.links import Links
from local.UrlOrdering import UrlOrdering
from local.relevanceCalculator import RelevanceCalculator

#from local.keywordFreq import countWords
from local.googlesearch import google
from local.seleniumSearch import querySearch


##input files
seeds_file = "inputs/seeds.txt"
keywords_file = "inputs/keywords.txt"
surnames_file = "inputs/surnames.txt"
cities_file = "inputs/cities.txt"
tags_file = "inputs/tags.txt"



keywordsList = {}
urlOrderObj = None
linksObj = None
relevanceCalculatorObj = None
keywords = []

#google search parameters
apiKey = "AIzaSyCO-m_ZU8Z2HKw4xbW1LegZjvAsOABXGL0"
cx  = "016070814652324639602:ajhiexm-yfe" #engine ID

depth = 5

def init():
    global urlOrderObj,linksObj,relevanceCalculatorObj,keywords
    linksObj = Links()
    relevanceCalculatorObj = RelevanceCalculator(surnames_file,cities_file,tags_file)    
    with open(keywords_file, 'r') as f:
        for line in f:
            keywords.append(line.strip())
        f.closed
    
    
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
            # Removing Javascript and Css before extracting text
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text().encode("utf-8")

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

def intelligent_crawl(url_bucket,currentFile):
    for link in url_bucket:
        try:
            print link
            response = urllib2.urlopen(link)
            info = response.info()
            mime = info.gettype()
            if 'text' not in mime: #avoiding pdf,ppt etc
                continue
            html = response.read()
            soup = BeautifulSoup(html,from_encoding="utf-8") 
            link_score = relevanceCalculatorObj.get_score(soup)
            with open(currentFile,"a+") as f:
                f.write(link)
                f.write(link_score)
                f.write("\n\n")
        except:
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

def findInitialUrlsSet(domain):  #fix remove duplicate 
    global keywords
    googleResults = getGoogleSearchUrls(domain)
    queryResults = getShootQueryResultUrls(domain)
    mergedResults = {}
    url_bucket = []
    print "Lets Merge"
    for word in keywords:
        mergedResults[word] = googleResults[word]+queryResults[word]
        url_bucket.extend(mergedResults[word])
        print "\n" + word
        print mergedResults[word]
    url_bucket = list(set(url_bucket))
    print("\n"+"\nfinal List"+ ''.join(url_bucket)) 
    return url_bucket
               
def main():
    global depth,currentFile
    init()
    if not os.path.exists('results'):
        os.makedirs('results')
    
    with open(seeds_file, 'r') as f: 
        for seedUrl in f: 
            seedUrl = seedUrl.rstrip().lower()

            if linksObj.isValid(seedUrl):
                domain = linksObj.domainOf(seedUrl)
                if not domain:
                    domain = counter
                    counter = counter+1
                currentFile = 'results/'+domain.upper()

                url_bucket = findInitialUrlsSet(seedUrl)

                if not os.path.exists(currentFile):#we log json here {url,priority,matches}
                    os.makedirs(currentFile)
                intelligent_crawl(url_bucket,currentFile+"/log.txt")

                #existRobot = linksObj.robotcheck(seedUrl)
                #crawl(depth,{}, existRobot)

main()
