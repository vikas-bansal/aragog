from bs4 import BeautifulSoup
from sys import argv
from urlparse import urlparse, urlunparse,urljoin
from keywordFreq import countWords
from pprint import pprint
import urllib2
import re
import os
import robotparser

keywordFreqFile = "keywordFreq.txt"
seedUrlFile = "seedUrls.txt"
surnamesFile = "surnames.txt"
relevantLinks = "relevantLinks.txt"
rp= robotparser.RobotFileParser()
surnamesList = {}
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
    f=open('results/anchorList', 'w')
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
   

def matchGivenKeywords(countDict, link):           
    matchedWords = {} 
    for word, count in countDict.iteritems():
        try:
            exist = surnamesList[word]
            if exist:
                matchedWords[word] = count
        except KeyError:
            continue
    if len(matchedWords) > 0:
        with open(relevantLinks, 'a') as out:
            out.write("\n\nLink: %s"%(link))
            for word,count in matchedWords.iteritems():
                out.write("\nWord: %s\t Count: %s" %(word,count))
           

#writing keywordCount in a seperate file   
def keywordFrequencyInFile(link):
    fileName = 'results/'+str(link.replace('/','.'))
    countDict = countWords(fileName)
    matchGivenKeywords(countDict, link)
    with open(keywordFreqFile, 'a') as out:
        out.write("FileName: "+fileName+"\n")
        pprint(countDict, stream=out)
        out.write('\n\n')

def iterativeDFS(link,linkDepth,visited, existRobot):
    if existRobot and not rp.can_fetch("*",link):
            print "Returning robot check "+ link
            return
    visited.append(link)
    try:
        response = urllib2.urlopen(link)
        html = response.read()
        soup = createSoup(html)
        text = extractText(soup)
        f = open('results/'+str(link.replace('/','.')),'w')
        f.write(text)
        f.close()
        keywordFrequencyInFile(link)
        anchorList = validateLinks(extractLinks(soup,text),link)
        for link in anchorList:
            print link+"\n"
        f=open('results/validLinks','w')
        for link in anchorList:
            f.write(link+"\n")
        f.close()
        for link in anchorList:
            if link not in visited and linkDepth<=depth:
                iterativeDFS(link,linkDepth+1,visited,existRobot)
    except :
            print "Exception while processing link: "+link
            return 

def main():
    global depth
    script,seedUrlFile,depth = argv
    print int(depth)
    initSurnamesDict()
    with open(seedUrlFile, 'r') as f:
            for seedUrl in f:
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
                if not os.path.exists('results'):
                    os.makedirs('results')
                iterativeDFS(seedUrl,0,[], existRobot)

main()
