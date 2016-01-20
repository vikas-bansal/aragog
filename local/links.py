class Links:
	"""Class with functions related to links found during crawling like extracting list of links, validating them etc."""
	
	def __init__(self):
    	self.rejectedFormats =  ['pdf','ppt','doc','docx','png','jpg','jpeg','zip']
	
	#retriving links from anchor tags
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
    
	# Validating links in anchor list to form list of valid urls to be crawled.

    def isValid(link):
        l = urlparse(link)
        if l.scheme and l.netloc:
            return True
        else:
            return False

	def validateLinks(self,anchorList,parent):
    	newParent=str()
    	newScheme = str()
    	validAnchorList = []
   		#fix expected formats
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
        	if parsedLink.path and (parsedLink.path[-3:] in self.rejectedFormats or parsedLink.path[-4:] in rejectedFormats):
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
