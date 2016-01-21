from itertools import count
from heapq import heappush, heappop
class UrlOrdering:
    
    #static variables
    linkHash = {}
    counter = count()          # unique sequence count
    
    def __init__(self,keywordsList):
        self.keywordsList = keywordsList
        self.pq = []                     # list of entries arranged in a heap
        self.counter = count() # unique sequence count

    def calculatePriority(self,link):
        #fix break url into words and match with kwyworklisd
        priority = 0
        for keyword in self.keywordsList:
            if keyword in link:
                priority = priority - self.keywordsList[keyword]  
        return priority 

    def addLink(self,link):
        'Add a new link or update the priority of an existing link'
        self.linkHash[link] = True
        priority = self.calculatePriority(link)
        count = next(self.counter)
        entry = [priority, count, link]
        heappush(self.pq, entry)
  
    def popLink(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        if self.pq:
            priority, count, link = heappop(self.pq)
            return link
        raise KeyError('pop from an empty priority queue')
        

        
