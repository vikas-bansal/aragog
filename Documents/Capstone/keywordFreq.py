from collections import Counter
from re import split

comOccKeywords =["the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
"it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
"this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
"or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
"so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
"when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
"person", "into", "year", "your", "good", "some", "could", "them", "see", "other",
"than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
"back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
"even", "new", "want", "because", "any", "these", "give", "day", "most", "us"]

def countWords(filename):
    counter = Counter()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip().lower()
            if not line:
                continue
            counter.update(x for x in split("[^a-zA-Z]+", line) if x and x not in comOccKeywords)
    f.close()
    return counter
 

