class RelevanceCalculator:
    """Class to calculate score of downloaded webpage."""    
    def __init__(self,surnames_file,cities_file,tags_file):
        self.surnamesList = {}
        self.citiesList = {}
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
            for word in f:
                self.weights[word.rstrip().lower()] = 1

    def path_score(tag,method): # given a tag this function gives the path score till html(max/add method)
        score = 0
        if(method == 'max'):
            for parent in tag.parents:
                if score < get_weight(parent.name):
                    score = get_weight(parent.name)
        else:
            k = 0.1
            for parent in tag.parents:
                score += get_weight(parent.name) * k
                k = k+0.1
        return score

    def get_weight(html_tag): #incase we have some html tags not covered 
        try:
            if(weights[html_tag]):
                return weights[html_tag]
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
                        page_score += path_score(tag,'max')
                except KeyError:
                    print('keyError')

                try:
                    if self.citiessList[word.strip().lower()]:
                    page_score += path_score(tag,'max')
                except KeyError:
                    print('keyError')
        return page_score
                    

    