class RelevanceCalculator:
    """Class to calculate score of downloaded webpage."""    
    def __init__(self,surnames_file,cities_file,tags_file):
        self.surnamesList = {}
        self.citiesList = {}
        self.weights = {}
        #SurnamesDict
        with open(surnames_file,'r') as f:
            for word in f:
                self.surnamesList[word.rstrip().lower()]=1
        #CitiesDict
        with open(cities_file,'r') as f:
            for word in f:
                self.citiesList[word.rstrip().lower()]=1

        #html tags weights
        with open(tags_file,'r') as f:
            for tagInfo in f:
                tagInfo = tagInfo.split()
                tag = tagInfo[0]
                weight = tagInfo[1]
                tag = tag.split("-")
                actualTag = tag[0]
                tagType = tag[1]
                if actualTag not in self.weights:
                    self.weights[actualTag] = {}
                if tagType == "surname":
                    self.weights[actualTag]["surname"] = weight
                elif tagType == "cities":
                    self.weights[actualTag]["cities"] = weight
            #print self.weights
        
                

    def path_score(self,tag,tagType): # given a tag this function gives the path score till html(max/add method)
        score = 0
        mscore = 0
        for parent in tag.parents:
            if mscore < self.get_weight(parent.name,tagType):
                mscore = self.get_weight(parent.name,tagType)
        k = 0.1
        for parent in tag.parents:
            score += self.get_weight(parent.name,tagType) * k
            k = k+0.1
        return mscore,score

    def get_weight(self,html_tag,tagType): #incase we have some html tags not covered
        if(html_tag in self.weights and tagType in self.weights[html_tag]):
            return float(self.weights[html_tag][tagType])
        else:
            #print ""+html_tag+tagType
            return 0.27 #defualt_weight

    def get_score(self,soup):
        # print url,score,matched_words 
        page_score1 = 0
        page_score2 = 0
        text_nodes = soup.findAll(text = True)
        foundList = []
        for text_node in text_nodes:
            for word in text_node.split():
                try:
                    if self.surnamesList[word.strip().lower()]:
                        mscore,score = self.path_score(text_node,"surname")
                        page_score1 += mscore
                        page_score2 += score
                        foundList.append(word)
                except KeyError:
                    try:
                        if self.citiesList[word.strip().lower()]:
                            mscore,score = self.path_score(text_node,"surname")
                            page_score1 += mscore
                            page_score2 += score
                            foundList.append(word)
                    except KeyError:
                        continue
        return page_score1,page_score2,foundList
                    

    
