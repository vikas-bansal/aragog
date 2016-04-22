import urllib
import json as m_json



"""
list of optional parameters
https://developers.google.com/custom-search/json-api/v1/reference/cse/list
"""

class google:
	"advanced search google"
	def __init__(self,apiKey,cx):
		self.apiKey = apiKey
		self.cx = cx
	
	def apisearch(self,query):
		#maximum 10 results in one call
		query = urllib.urlencode ( { 'q' : query } )
		response = urllib.urlopen ( "https://www.googleapis.com/customsearch/v1?key="+self.apiKey+"&cx="+self.cx+"&q="+query).read()
		json = m_json.loads ( response )
		results = []
		for r in json['items']:
			results.append(r['link'])
		return results

	def ajaxsearch(self,query):
		#maximum 4 results in one call
		query = urllib.urlencode ( { 'q' : query } )
		response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
		json = m_json.loads ( response )
		arr = json [ 'responseData' ] [ 'results' ]
		results = []
		for r in arr:
			results.append(r['url'])
		return results

'''
#test
domain = "mit.edu"
keyword = "faculty"
apiKey = "AIzaSyCO-m_ZU8Z2HKw4xbW1LegZjvAsOABXGL0"
cx  = "016070814652324639602:ajhiexm-yfe" #engine ID


gobj = google(apiKey,cx)
arr = gobj.apisearch(keyword+"site:"+ domain)
for link in arr:
	print link'''
