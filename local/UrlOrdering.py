class UrlOrdering:
    
    counter = itertools.count()          # unique sequence count
    
    def __init__(self,keywordsList):
        self.keywordsList = keywordsList
        self.pq = []                     # list of entries arranged in a heap
        self.counter = itertools.count() # unique sequence count

    def addLink(self,link):
        'Add a new link or update the priority of an existing link'
        priority = calculatePriority(link)
        count = next(counter)
        entry = [priority, count, link]
        heappush(pq, entry)
  
    def popLink(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
         if pq not None:
            priority, count, link = heappop(pq)
            return link
        raise KeyError('pop from an empty priority queue')
        
    def calculatePriority(self,link):
        #fix break url into words and match with kwyworklisd
        priority = 0
        for keyword in self.keywordsList:
            if keyword in link:
            priority = priority - keywordsList[keyword]  
        return priority 
        
