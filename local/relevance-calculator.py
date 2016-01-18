#purpose :  calculate score of downloaded webpage

keywordFreqFile = "keywordFreq.txt"
relevantLinks = "relevantLinks.txt"
priortizedUrlFile = "priortizedUrls.txt"

def createPriortizedUrlFile():
    global linkToKeywordsMap,keywordCountToUrlMap
    with open(currentFile+'/'+priortizedUrlFile, 'w+') as out:
         for key in sorted(keywordCountToUrlMap.keys(), reverse=True):
             keywordCount = key
             links = keywordCountToUrlMap[key]
             for link in links:
                 out.write("\n\nLink: %s \t keywordCount: %s"  %(link,keywordCount))
                 surnames = linkToKeywordsMap[link]["surnames"]
                 cities = linkToKeywordsMap[link]["cities"]
                 if len(surnames) > 0:
                     out.write("\n\nSurnames:")
                     for word,count in surnames.iteritems():
                         out.write("\nWord: %s\t Count: %s" %(word,count))
                 if len(cities) > 0:
                     out.write("\n\nCities:")
                     for word,count in cities.iteritems():
                         out.write("\nWord: %s\t Count: %s" %(word,count))



    
def matchGivenKeywords(countDict, link): 
    global linkToKeywordsMap,keywordCountToUrlMap,surnamesList,citiesList          
    matchedSurnames = {}
    matchedCities = {} 
    for word,count in countDict.iteritems():
        try:
            if surnamesList[word]:
                matchedSurnames[word] = count
        except KeyError:
            try:
                if citiesList[word]:
                    matchedCities[word] = count
            except KeyError:
                    continue
    totalKeywords = updateRelevantLinks(link,matchedSurnames,matchedCities)
    keywordCountToUrlMap[totalKeywords].add(link)
    linkToKeywordsMap[link] = {}
    linkToKeywordsMap[link]['surnames'] = dict(matchedSurnames)
    linkToKeywordsMap[link]['cities'] = dict(matchedCities)
    
def updateRelevantLinks(link,surnames,cities):
    keywordCount = 0
    with open(currentFile+'/'+relevantLinks, 'w+') as out:
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