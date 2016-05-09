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
        try:
            if self.weights[actualTag]:
                if tagType is "surname":
                    self.weights[actualTag]["surname"] = weight
                elif tagType is "cities":
                    self.weights[actualTag]["cities"] = weight
        except KeyError:
            self.weights[actualTag] = {}
            if tagType is "surname":
                self.weights[actualTag]["surname"] = weight
            elif tagType is "cities":
                self.weights[actualTag]["cities"] = weight
                

    def path_score(tag,method,tagType): # given a tag this function gives the path score till html(max/add method)
        score = 0
        if(method == 'max'):
            for parent in tag.parents:
                if score < get_weight(parent.name,tagType):
                    score = get_weight(parent.name,tagType)
        else:
            k = 0.1
            for parent in tag.parents:
                score += get_weight(parent.name,tagType) * k
                k = k+0.1
        return score

    def get_weight(self,html_tag,tagType): #incase we have some html tags not covered 
        try:
            if(self.weights[html_tag]):
                if(self.weights[html_tag][tagType]):
                    return self.weights[html_tag][tagType]
        except keyError:
            return 0.27 #defualt_weight

    def get_score(self,soup):
        # print url,score,matched_words 
        page_score = 0
        text_nodes = soup.findAll(text = True)
        for text_node in text_nodes:
            for word in text_node.split():
                try:
                    if self.surnamesList[word.strip().lower()]:
                        page_score += path_score(tag,'max',"surname")
			print('found'+word)
                except KeyError:
                    try:
                    	if self.citiesList[word.strip().lower()]:
                            page_score += path_score(tag,'max',"cities")
			    print('found'+word)
                    except KeyError:
                        continue
        return page_score
                    

    
