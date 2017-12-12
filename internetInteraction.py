import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import re


def getWords(n):
	words = []
	words = getCities()
	words = list(words)
	return words

def getCities():
	res_arr = set()
	try:
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
			PREFIX  dbpedia-owl:  <http://dbpedia.org/ontology/>
PREFIX dbpedia: <http://dbpedia.org/resource>
PREFIX dbpprop: <http://dbpedia.org/property>
SELECT DISTINCT ?label ?pop
WHERE {
   ?city rdf:type ?ccs.
   ?city rdfs:label ?label.
   ?city dbpedia-owl:populationTotal ?pop .
   FILTER ( lang(?label) = 'ru' and ?pop>10000 and ?ccs IN (dbpedia-owl:City, dbpedia-owl:Town))
}
Order by DESC(?pop)
LIMIT 100
		""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		for result in results["results"]["bindings"]:
			res_name = result["label"]["value"]
			res_arr.add(re.split("[,\(]",res_name)[0])

	except Exception as e:
		print("ERRR in 1")
		print(e)
	return res_arr