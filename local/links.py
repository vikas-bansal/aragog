from urlparse import urlparse
import re
from urlparse import urlparse, urlunparse,urljoin
import robotparser

"""Class with functions related to links found during crawling like extracting list of links, validating them etc."""

class Links:
    def __init__(self):
        global rp
        self.rejectedFormats =  ['pdf','ppt','doc','docx','png','jpg','jpeg','zip']
        rp= robotparser.RobotFileParser()

    def isValid(self,link):
        l = urlparse(link)
        if l.scheme and l.netloc:
            return True
        else:
            return False

    def domainOf(self,url):
        url_components = urlparse(url)
        return url_components.netloc

    #retriving links from anchor tags and regex search
    def extractLinks(self, soup, extractedText):
        tags = soup.find_all('a')
        anchorList = []
        for tag in tags:
            link = tag.get('href')
            if(link!=None and link!="javascript:void(0);" and link[:1]!="#"):
                anchorList.append(link)
        anchorList += re.findall(r'(https?://[^\s]+)', extractedText)
        #fix not picking www.example.com or google.com/
        set_anchorList = set(anchorList)
        anchorList = list(set_anchorList)
        return anchorList

    def robotcheck(self,seedUrl):
        # get robot.txt                
        #base = page_url[0] + '://' + page_url[1]
        robots_url = urljoin(seedUrl,'/robots.txt')
        rp.set_url(robots_url)
        existRobot=0
        try:
            rp.read()
            existRobot = 1
        except:
            print "Robot.txt does not exist." + seedUrl
        return existRobot

    def robot_allowed(self,link):#needs semantic fix
        return rp.can_fetch("*",link)

    # Validating links in anchor list to form list of valid urls to be crawled.
    def validateLinks(self,anchorList,parent):
        newParent=str()
        newScheme = str()
        validAnchorList = []
        rejectedList = []
        parent = urlparse(parent)
        for link in anchorList:
            parsedLink = urlparse(link)
            if parsedLink.netloc and parsedLink.netloc != parent.netloc:
                rejectedList.append(link)
                continue
            if parsedLink.path and (parsedLink.path[-3:] in self.rejectedFormats or parsedLink.path[-4:] in self.rejectedFormats):
                rejectedList.append(link)
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
        return validAnchorList,rejectedList


#test
links_utility = Links()
cases=[
'http://tech.mit.edu',
'tech.mit.edu',
'mit.edu',
'www.pec.ac.in',
'http://www.pec.ac.in',
'https://www.mit.edu'
]
for url in cases:
    print links_utility.isValid(url)