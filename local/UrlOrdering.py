from itertools import count
from heapq import heappush, heappop
class UrlOrdering:
    
    def __init__(self,keywords_file):
        self.keywordsListFile = keywords_file
        self.keywordsList = {}
        self.pq = [] # list of entries arranged in a heap
        self.counter = count() # unique sequence count
        self.openLinks = {} # links which are in priority queue
        
        #keyword dict - keywords to look for in url with their priority
        priority = 0
        for line in reversed(open(self.keywordsListFile).readlines()) :
            self.keywordsList[line.rstrip().lower()] = priority
            priority = priority+1

    def calculatePriority(self,link):
        priority = 0
        for keyword in self.keywordsList:
            if keyword in link:
                priority = priority - self.keywordsList[keyword]  
        return priority 

    def addLink(self,link):
        'Add a new link or update the priority of an existing link'
        self.openLinks[link] = True
        priority = self.calculatePriority(link)
        count = next(self.counter)
        entry = [priority, count, link]
        heappush(self.pq, entry)
  
    def popLink(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        if self.pq:
            priority, count, link = heappop(self.pq)
            del self.openLinks[link]
            return link
        raise KeyError('pop from an empty priority queue')