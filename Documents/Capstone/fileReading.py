from bs4 import BeautifulSoup
from sys import argv
from urlparse import urlparse, urlunparse
from keywordFreq import countWords
from pprint import pprint
import urllib2
import re
import os

keywordFreqFile = "keywordFreq.txt"

def createSoup(html):
    return BeautifulSoup(html,from_encoding="utf-8")    

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
    set_anchorList = set(anchorList)
    anchorList = list(set_anchorList)
    return anchorList

#extracting text from html    
def extractText(soup):
    # Removing Javascript and Css before extracting text
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text().encode("utf-8")

def validateLinks(anchorList,parent):
    newParent=str()
    newScheme = str()
    validAnchorList = []
    # expected formats
    # www.example.com ( urlparse put this domain into path not netloc )
    # example.com
    # http://example.com
    # https://example.com
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
    with open(keywordFreqFile, 'a') as out:
        out.write("FileName: "+fileName+"\n")
        pprint(dict(countDict), stream=out)
        out.write('\n\n')

def openAllLinks(anchorList):
    for link in anchorList:
        try:
            response = urllib2.urlopen(link)
            html = response.read()
            text = extractText(createSoup(html))
            f = open('results/'+str(link.replace('/','.')),'w')
            f.write(text)
            f.close()
            keywordFrequencyInFile('results/'+str(link.replace('/','.')))
        except :
            continue

def main():
    script,srcFile,parentDomain = argv
    if (os.path.exists(srcFile)):
        src = open(srcFile)
        parent = parentDomain
        html = src.read()
        soup = createSoup(html)
        extractedText = extractText(soup)
        if not os.path.exists('results'):
            os.makedirs('results')
        f = open('results/sourcetext.txt','w')
        f.write(extractedText)
        f.close()
        anchorList = validateLinks(extractLinks(soup,extractedText),parent)
        with open('results/extractedLinks.txt', 'wt') as out:
            pprint(anchorList, stream=out)
        openAllLinks(anchorList)
        src.close()
    else:
        print "Text file does not exists"
    
if __name__ == '__main__':
    main()
