from bs4 import BeautifulSoup
from sys import argv
from os.path import exists
import re

anchorList = []
extractedText = ''

#retriving links from anchor tags
def extractLinks(soup):
    global anchorList,extractedText
    tags = soup.find_all('a')
    for tag in tags:
        link = tag.get('href')
        anchorList.append(link)
    anchorList += re.findall(r'(https?://[^\s]+)', extractedText)
    set_anchorList = set(anchorList)
    anchorList = list(set_anchorList)
    print anchorList

#extracting text from html    
def extractText(soup):
    global anchorList,extractedText
    extractedText = soup.get_text().encode("utf-8")
    
    
def main():
    script,srcFile = argv
    if (exists(srcFile)):
        src = open(srcFile)
        html = src.read()
        soup = BeautifulSoup(html,from_encoding="utf-8")
        extractText(soup)
        extractLinks(soup)
       # openAllLinks()
        src.close()
    else:
        print "Text file does not exists"
    
if __name__ == '__main__':
    main()
