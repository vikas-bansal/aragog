from bs4 import BeautifulSoup
from sys import argv
from os.path import exists
from urlparse import urlparse, urlunparse
from keywordFreq import countWords
import urllib2
import re
import nltk

parent = "www.google.com"

keywordFreqFile = "keywordFreq.txt"


def createSoup(html):
    return BeautifulSoup(html,from_encoding="utf-8")    

#retriving links from anchor tags
def extractLinks(soup, extractedText):
    tags = soup.find_all('a')
    anchorList = []
    for tag in tags:
        link = tag.get('href')
        if(link!=None and link!="javascript:void(0);" and link!="#"):
            anchorList.append(link)
    anchorList += re.findall(r'(https?://[^\s]+)', extractedText)
    set_anchorList = set(anchorList)
    anchorList = list(set_anchorList)
    return anchorList

#extracting text from html    
def extractText(soup):
    # Removing Javascript and Css before extracting text
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text().encode("utf-8")

def validateLinks(anchorList):
    global parent
    newParent=str()
    newScheme = str()
    validAnchorList = []
    for link in anchorList:
        parsedLink = urlparse(link)
        if not parsedLink.scheme:
            if not parsedLink.netloc:
                newParent = parent
            newScheme = "https"
            if not newParent:
                newLink = (newScheme,) + parsedLink[1:]
            else:
                newLink = (newScheme, newParent) + parsedLink[2:]
            validAnchorList.append(urlunparse(newLink))
        else:
            validAnchorList.append(link)
    return validAnchorList    
 
#writing keywordCount in a seperate file    
def keywordFrequencyInFile(fileName):
    countDict = countWords(fileName)
    f = open(keywordFreqFile,'a')
    f.write("FileName: "+fileName+"\n")
    f.write(str(countDict))
    f.write("\n\n")
    f.close()  

def openAllLinks(anchorList):
    i = 1
    for link in anchorList:
        try:
            response = urllib2.urlopen(link)
            html = response.read()
            text = extractText(createSoup(html))
            f = open(str(i),'w')
            f.write(text)
            f.close()
            keywordFrequencyInFile(str(i))
            i += 1
        except :
            continue

def main():
    script,srcFile = argv
    if (exists(srcFile)):
        src = open(srcFile)
        html = src.read()
        soup = createSoup(html)
        extractedText = extractText(soup)
        print extractedText
        anchorList = validateLinks(extractLinks(soup,extractedText))
        for anchor in anchorList:
            print anchor
            print "\n"
        openAllLinks(anchorList)
        src.close()
    else:
        print "Text file does not exists"
    
if __name__ == '__main__':
    main()
