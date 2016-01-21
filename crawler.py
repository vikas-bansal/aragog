#!/usr/bin/env python

# #######################
# A BROAD TODO LIST
#
# write unit tests
# fix issues in this file - search #fix tag
# #######################


##inbuilt modules
from sys import argv
from pprint import pprint
from urlparse import urlparse, urlunparse,urljoin
from collections import defaultdict
import urllib2
import re
import os
import robotparser

## downloaded modules
from bs4 import BeautifulSoup

## local directory holds all local module files
from local.links import Links
from local.UrlOrdering import UrlOrdering
from local.relevanceCalculator import RelevanceCalculator
from local.keywordFreq import countWords


keywordsListFile = "inputs/keywords.txt"
keywordsList = {}

rp= robotparser.RobotFileParser()
surnamesList = {}
citiesList = {}
linkToKeywordsMap = {}
urlOrderObj = None
linksObj = None
relevanceCalculatorObj = None

keywordCountToUrlMap = defaultdict(set)
# eg: { 22 : ('link1','link2'...) , 17 : ('link3','link4...) ....} 

#extracting text from html   
def extractText(soup):
    # Removing Javascript and Css before extracting text
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text().encode("utf-8")


seedUrlFile = "inputs/seeds.txt"
surnamesFile = "inputs/surnames.txt"
citiesFile = "inputs/cities.txt"

depth=5


def init():
    #SurnamesDict
    with open(surnamesFile,'r') as f:
        for word in f:
            surnamesList[word.rstrip().lower()]=1

    #CitiesDict
    with open(citiesFile,'r') as f:
        for word in f:
            citiesList[word.rstrip().lower()]=1

    #keyword dict - keywords to look for in url with their priority
    priority = 0
    for line in reversed(open(keywordsListFile).readlines()) :
        keywordsList[line.rstrip().lower()] = priority
        priority = priority+1
        
    #creating object of UrlOrdering class
    global urlOrderObj,linksObj,relevanceCalculatorObj
    urlOrderObj =  UrlOrdering(keywordsList)
    linksObj = Links()
    relevanceCalculatorObj = RelevanceCalculator()
            
#writing keywordCount in a seperate file   
def keywordFrequencyInFile(link):
    fileName = currentFile +'/'+str(link.replace('/','.'))
    countDict = countWords(fileName)
    relevanceCalculatorObj.matchGivenKeywords(countDict, link)
    with open(keywordFreqFile, 'a') as out:
        out.write("FileName: "+fileName+"\n")
        pprint(countDict, stream=out)
        out.write('\n\n')
    
def crawl(linkDepth,visited, existRobot):
    global rp #fix valueError?
    while OPEN:
        try:
            link = urlOrderObj.popLink(OPEN)
            print "Traversing Link: "+link
            visited[link] = True

            if existRobot and not rp.can_fetch("*",link):
                print "Returning robot check "+ link
                continue

            response = urllib2.urlopen(link)
            info = response.info()## meta info for the above request - used to get mime type    text/html is expected
            mime = info.gettype()
            #fix avoid mime types here

            html = response.read()
            soup = BeautifulSoup(html,from_encoding="utf-8") 
            text = extractText(soup)

            #keywordFrequencyInFile(link) #fix :  we don't need this NOW I think

            anchorList = linksObj.validateLinks(linksObj.extractLinks(soup,text),link) 
            # this module would later be made to run on a different thread 

            for link in anchorList:
                if link not in linkHash and visited.get(link) != None:
                    urlOrderObj.addLink(link)
        except IOError :
                print "IOError reading: "+link
                return 

def robotcheck(page_url):
    # get robot.txt                
    base = page_url[0] + '://' + page_url[1]
    robots_url = urljoin(base,'/robots.txt')
    rp.set_url(robots_url)
    existRobot=0
    try:
        rp.read()
        existRobot = 1
    except:
        print "Robot.txt does not exist." + seedUrl
    return existRobot


def main():
    global depth,currentFile
    init()

    if not os.path.exists('results'):
        os.makedirs('results')

    with open(seedUrlFile, 'r') as f: 
    #fix: assumption seed Urls are expected to be in proper format?
            for seedUrl in f: 
                seedUrl = seedUrl.rstrip()
                if linksObj.isValid(seedUrl):
                    page_url = urlparse(seedUrl)
                    currentFile = 'results/'+page_url.netloc
                    urlOrderObj.addLink(seedUrl)

                    if not os.path.exists(currentFile):
                        os.makedirs(currentFile)

                    existRobot = robotcheck(page_url)
                    crawl(depth,{}, existRobot)
                    relevanceCalculatorObj.createPriortizedUrlFile()
main()
