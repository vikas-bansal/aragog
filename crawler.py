#!/usr/bin/env python3

##inbuilt modules
from sys import argv
from pprint import pprint
from urlparse import urlparse, urlunparse,urljoin
from collections import defaultdict
import urllib2
import re
import os
import robotparser

## downloaded
from bs4 import BeautifulSoup

## local (created)
from keywordFreq import countWords

currentFile = ''
keywordFreqFile = "keywordFreq.txt"
seedUrlFile = "seedUrls.txt"
surnamesFile = "surnames.txt"
citiesFile = "cities.txt"
relevantLinks = "relevantLinks.txt"
priortizedUrlFile = "priortizedUrls.txt"
rejectedFormats = ['pdf','ppt','doc','docx','png','jpg','jpeg','zip']
rp= robotparser.RobotFileParser()
surnamesList = {}
citiesList = {}
linkToKeywordsMap = {}
'''
structure of linkTokeywordsMap
{ link1 : {
    surnames : {
        word1:count1
        ......
    },
    cities : {
        word1:count1
        .......
    }
  },
  link2 : {
      .......
  }
}
'''
keywordCountToUrlMap = defaultdict(set)
# eg: { 22 : ('link1','link2'...) , 17 : ('link3','link4...) ....} 
depth=0

def createSoup(html):
    return BeautifulSoup(html,from_encoding="utf-8") 


#extracting text from html   
def extractText(soup):
    # Removing Javascript and Css before extracting text
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text().encode("utf-8")


#retriving links from anchor tags
def extractLinks(soup, extractedText):
    tags = soup.find_all('a')
    anchorList = []
    for tag in tags:
        link = tag.get('href')
        if(link!=None and link!="javascript:void(0);" and link[:1]!="#"):
            anchorList.append(link)
    anchorList += re.findall(r'(https?://[^\s]+)', extractedText)
    # not picking www.example.com or google.com/
    f=open(currentFile+'/anchorList', 'w+')
    for link in anchorList:
        f.write(link+"\n")
    f.close()
    set_anchorList = set(anchorList)
    anchorList = list(set_anchorList)
    return anchorList


def validateLinks(anchorList,parent):
    newParent=str()
    newScheme = str()
    validAnchorList = []
    # expected formats
    # www.example.com ( urlparse put this domain into path not netloc )
    # example.com
    # http://example.com
    # https://example.com
    parent = urlparse(parent)
    for link in anchorList:
        parsedLink = urlparse(link)
        if parsedLink.netloc and parsedLink.netloc != parent.netloc:
            #print link
            continue
        if parsedLink.path and (parsedLink.path[-3:] in rejectedFormats or parsedLink.path[-4:] in rejectedFormats):
            continue
        if not parsedLink.scheme:
            if not parsedLink.netloc:
                newParent = parent.netloc
            newScheme = parent.scheme
            if not newParent:
                newLink = (newScheme,) + parsedLink[1:]
            else:
                newLink = (newScheme, newParent) + parsedLink[2:]
            validAnchorList.append(urlunparse(newLink))
        else:
            validAnchorList.append(link)
    return validAnchorList

def initSurnamesDict():
    with open(surnamesFile,'r') as f:
        for word in f:
            surnamesList[word.rstrip().lower()]=1
            

def initCitiesDict():
    with open(citiesFile,'r') as f:
        for word in f:
            citiesList[word.rstrip().lower()]=1
            
def createPriortizedUrlFile():
    global linkToKeywordsMap,keywordCountToUrlMap
    with open(currentFile+'/'+priortizedUrlFile, 'w+') as out:
         for key in sorted(keywordCountToUrlMap.keys(), reverse=True):
             keywordCount = key
             links = keywordCountToUrlMap[key]
             for link in links:
                 out.write("\n\nLink: %s \t keywordCount: %s"  %(link,keywordCount))
                 surnames = linkToKeywordsMap[link]["surnames"]
                 cities = linkToKeywordsMap[link]["cities"]
                 if len(surnames) > 0:
                     out.write("\n\nSurnames:")
                     for word,count in surnames.iteritems():
                         out.write("\nWord: %s\t Count: %s" %(word,count))
                 if len(cities) > 0:
                     out.write("\n\nCities:")
                     for word,count in cities.iteritems():
                         out.write("\nWord: %s\t Count: %s" %(word,count))
                         
def cleanUpLists():
    global linkToKeywordsMap,keywordCountToUrlMap
    linkToKeywordsMap = {}
    keywordCountToUrlMap = defaultdict(set)
    
                     
def updateRelevantLinks(link,surnames,cities):
    keywordCount = 0
    with open(currentFile+'/'+relevantLinks, 'w+') as out:
        out.write("\n\nLink: %s"%(link))
        if len(surnames) > 0:
            out.write("\n\nSurnames:")
            for word,count in surnames.iteritems():
                keywordCount += count
                out.write("\nWord: %s\t Count: %s" %(word,count))
        if len(cities) > 0:
            out.write("\n\nCities:")
            for word,count in cities.iteritems():
                keywordCount += count
                out.write("\nWord: %s\t Count: %s" %(word,count))
    return keywordCount
    
def matchGivenKeywords(countDict, link): 
    global linkToKeywordsMap,keywordCountToUrlMap,surnamesList,citiesLit          
    matchedSurnames = {}
    matchedCities = {} 
    for word,count in countDict.iteritems():
        try:
            if surnamesList[word]:
                matchedSurnames[word] = count
        except KeyError:
            try:
                if citiesList[word]:
                    matchedCities[word] = count
            except KeyError:
                    continue
    totalKeywords = updateRelevantLinks(link,matchedSurnames,matchedCities)
    keywordCountToUrlMap[totalKeywords].add(link)
    linkToKeywordsMap[link] = {}
    linkToKeywordsMap[link]['surnames'] = dict(matchedSurnames)
    linkToKeywordsMap[link]['cities'] = dict(matchedCities)
    
    
#writing keywordCount in a seperate file   
def keywordFrequencyInFile(link):
    fileName = currentFile +'/'+str(link.replace('/','.'))
    countDict = countWords(fileName)
    matchGivenKeywords(countDict, link)
    with open(keywordFreqFile, 'a') as out:
        out.write("FileName: "+fileName+"\n")
        pprint(countDict, stream=out)
        out.write('\n\n')

def iterativeDFS(link,linkDepth,visited, existRobot):
    global rp
    if linkDepth+1 > depth:
        return
    if existRobot and not rp.can_fetch("*",link):
            print "Returning robot check "+ link
            return
    visited.append(link)
    try:
        response = urllib2.urlopen(link)
        info = response.info()## meta info for the above request - used to get mime type    text/html is expected
        mime = info.gettype()
        link = response.geturl()# just in case request is redirected 
        html = response.read()
        soup = createSoup(html)
        text = extractText(soup)


        # download content to a file
        #urllib.urlretrieve(url, filename) 
        
        keywordFrequencyInFile(link)
        anchorList = validateLinks(extractLinks(soup,text),link)
        f=open(currentFile+'/validLinks','w+')
        for link in anchorList:
            f.write(link+"\n")
        f.close()
        for link in anchorList:
            if link not in visited:
                print linkDepth,depth,link+"\n"
                iterativeDFS(link,linkDepth+1,visited,existRobot)
    except IOError :
            print "IOError reading: "+link
            return 

def main():
    global depth,currentFile
    script,seedUrlFile,depth = argv
    depth = int(depth)
    print int(depth)
    initSurnamesDict()
    initCitiesDict()
    if not os.path.exists('results'):
        os.makedirs('results')
    with open(seedUrlFile, 'r') as f:
            for seedUrl in f:
                currentFile = 'results/'+str(seedUrl.replace('/','.'))
                seedUrl = seedUrl.rstrip()
                page_url = urlparse(seedUrl)
                print seedUrl
                base = page_url[0] + '://' + page_url[1]
                robots_url = urljoin(base,'/robots.txt')
                rp.set_url(robots_url)
                existRobot=0
                try:
                    rp.read()
                    existRobot = 1
                except:
                    print "Robot.txt does not exist." + seedUrl
                if not os.path.exists(currentFile):
                    os.makedirs(currentFile)
                iterativeDFS(seedUrl,0,[], existRobot)
                createPriortizedUrlFile()
                cleanUpLists()
                
main()
