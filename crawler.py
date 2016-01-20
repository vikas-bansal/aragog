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
from local.links import validateLinks
from local.keywordFreq import countWords


keywordsListFile = "keywords.txt"
keywordsList = {}

rp= robotparser.RobotFileParser()
surnamesList = {}
citiesList = {}
linkToKeywordsMap = {}

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
            
#writing keywordCount in a seperate file   
def keywordFrequencyInFile(link):
    fileName = currentFile +'/'+str(link.replace('/','.'))
    countDict = countWords(fileName)
    matchGivenKeywords(countDict, link)
    with open(keywordFreqFile, 'a') as out:
        out.write("FileName: "+fileName+"\n")
        pprint(countDict, stream=out)
        out.write('\n\n')
    
def calculatePriority(link):
    #fix break url into words and match with kwyworklisd
    priority = 0
    for keyword in keywordsList:
        if keyword in link:
            priority = priority + keywordsList[keyword]  
    return priority  
    

def removeBestUrl(OPEN):
    #remove best link and return
    


def crawl(OPEN,linkDepth,visited, existRobot):
    global rp #fix valueError?
    while OPEN:
        try:
            link = removeBestUrl(OPEN)
            print "Traversing Link: "+link
            del OPEN[link]
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

            anchorList = validateLinks(extractLinks(soup,text),link) 
            # this module would later be made to run on a different thread 

            for link in anchorList:
                if link not in OPEN and visited.get(link) != None:
                    priority = calculatePriority(link)
                    OPEN[link] = priority
                    print priority
        except IOError :
                print "IOError reading: "+link
                return 

def robotcheck():
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


def main():
    global depth,currentFile
    init()

    if not os.path.exists('results'):
        os.makedirs('results')

    with open(seedUrlFile, 'r') as f: 
    #fix: assumption seed Urls are expected to be in proper format?
    	if links.isValid(seedUrlFile):
            for seedUrl in f: 
                seedUrl = seedUrl.rstrip()
                page_url = urlparse(seedUrl)
                currentFile = 'results/'+page_url.netloc

                if not os.path.exists():
                    os.makedirs(currentFile)

                robotcheck()
                #iterativeDFS(seedUrl,0,[], existRobot)
                crawl({0:[seedUrl]},depth,{}, existRobot)
                createPriortizedUrlFile()
main()
