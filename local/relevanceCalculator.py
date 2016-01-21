from collections import defaultdict
class RelevanceCalculator:
	"""Class to calculate score of downloaded webpage."""

        surnamesFile = "/../inputs/surnames.txt"
        citiesFile = "/../inputs/cities.txt"
        
	def __init__(self):
		self.keywordFreqFile = "keywordFreq.txt"
		self.relevantLinks = "relevantLinks.txt"
		self.priortizedUrlFile = "priortizedUrls.txt"
        self.keywordCountToUrlMap = defaultdict(set)
        self.linkToKeywordsMap = {}
        self.surnamesList = {}
        self.citiesList = {}
        
        #SurnamesDict
        with open(surnamesFile,'r') as f:
            for word in f:
                self.surnamesList[word.rstrip().lower()]=1

        #CitiesDict
        with open(citiesFile,'r') as f:
            for word in f:
                self.citiesList[word.rstrip().lower()]=1

	def createPriortizedUrlFile(self,currentFile):
   		with open(currentFile+'/'+self.priortizedUrlFile, 'w+') as out:
                        for key in sorted(self.keywordCountToUrlMap.keys(), reverse=True):
                                keywordCount = key
                                links = self.keywordCountToUrlMap[key]
                                for link in links:
                                        out.write("\n\nLink: %s \t keywordCount: %s"  %(link,keywordCount))
                                        surnames = self.linkToKeywordsMap[link]["surnames"]
                                        cities = self.linkToKeywordsMap[link]["cities"]
                                        if len(surnames) > 0:
                                                out.write("\n\nSurnames:")
                                                for word,count in surnames.iteritems():
                                                        out.write("\nWord: %s\t Count: %s" %(word,count))
                                        if len(cities) > 0:
                                                out.write("\n\nCities:")
                                                for word,count in cities.iteritems():
                                                        out.write("\nWord: %s\t Count: %s" %(word,count))

    
	def matchGivenKeywords(self,countDict, link,currentFile): 
                matchedSurnames = {}
                matchedCities = {} 
                for word,count in countDict.iteritems():
                        try:
                                if self.surnamesList[word]:
                                        matchedSurnames[word] = count
                        except KeyError:
                                try:
                                        if self.citiesList[word]:
                                                matchedCities[word] = count
                                except KeyError:
                                    continue
                totalKeywords = updateRelevantLinks(link,matchedSurnames,matchedCities,currentFile)
                self.keywordCountToUrlMap[totalKeywords].add(link)
                self.linkToKeywordsMap[link] = {}
                self.linkToKeywordsMap[link]['surnames'] = dict(matchedSurnames)
                self.linkToKeywordsMap[link]['cities'] = dict(matchedCities)
    
	def updateRelevantLinks(self, link,surnames,cities,currentFile):
                keywordCount = 0
                with open(currentFile+'/'+self.relevantLinks, 'w+') as out:
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

