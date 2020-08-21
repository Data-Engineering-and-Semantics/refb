# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from Bio import Entrez
from Bio import Medline
import requests

Entrez.email = "turkiabdelwaheb@hotmail.fr"     #Identification
endpoint_url = "https://query.wikidata.org/sparql"

query = """#by Csisc, 2020-05-28
SELECT DISTINCT ?item ?property ?v ?itemLabel ?pLabel ?vLabel 
WITH {
  SELECT DISTINCT ?item ?prop1 ?v ?itemLabel ?vLabel WHERE {
    ?item ?prop ?statement .
    ?item ?prop [?p ?v] .
    ?item wdt:P2892 [].
    ?v wdt:P2892 [].
    FILTER(!(regex(str(?prop), "http://www.wikidata.org/prop/direct/" ) ))
    FILTER(regex(str(?prop), "http://www.wikidata.org/prop/" ) )
    FILTER NOT EXISTS {
               ?item ?prop ?statement .
               ?statement prov:wasDerivedFrom ?derivedFrom  .}
    ?item rdfs:label ?itemLabel.
    ?item ?prop1 ?v.
    ?v rdfs:label ?vLabel.
    FILTER(LANG(?itemLabel)="en")
    FILTER(LANG(?vLabel)="en")
    }
  }
AS %statements
WITH {
  SELECT * WHERE {
  ?property wikibase:directClaim ?prop1.
  ?property rdfs:label ?pLabel.
  FILTER(LANG(?pLabel)="en")
    }
}
AS %labels
WHERE {
  INCLUDE %statements.
  INCLUDE %labels
    }"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

g = open("output.csv", "w")
results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)
    search = '"'+result["itemLabel"]["value"]+'" OR "'+result["pLabel"]["value"]+'" OR "'+'"'+result["vLabel"]["value"]+'" OR "'+result["itemLabel"]["value"]+'" OR "'+'"'+result["vLabel"]["value"]+'"'
    handle = Entrez.esearch(db="pmc", term=search, retmax="3", sort="relevance" )
    record = Entrez.read(handle)
    print(record["IdList"])


    for ss in record["IdList"]:
        handle1 = Entrez.efetch(db="pmc", id=ss, rettype="medline", retmode="text")
        records = Medline.parse(handle1)
        for r in records:
            if (r.get("RIN", "?")=="?"):
                if (r.get("PRIN", "?")=="?"):
                    print("Title:", r.get("TI", "?")) #Getting Title
                    print("")
                    print("Authors:", r.get("FAU", "?")) #Getting Authors
                    print("")
                    print("Affiliation:", r.get("AD", "?")) #Getting Affiliation
                    print("")
                    print("Date:", r.get("DEP", "?")) #Getting Publication Date
                    print("")
                    print("Journal Title:", r.get("JT", "?")) #Getting Journal Title
                    print("")
                    print("Abstract:", r.get("AB", "?")) #Getting Abstract
                    print("")
                    ws = ss
                    print("PMCID: ", ws)
                    print("_______________________________________")
                    if (r.get("AB", "?").find(result["itemLabel"]["value"])!=-1):
                        if (r.get("AB", "?").find(result["vLabel"]["value"])!=-1):
                            idurl = "https://hub.toolforge.org/P932:"+ws+"?format=json"
                            idget = requests.get(idurl)
                            idjson = idget.json()
                            try:
                                wid = idjson["origin"]["qid"]
                            except KeyError:
                                wid = ""
                            if (wid != ""):
                                ux = result["item"]["value"][31:255]+"%09"+result["property"]["value"][31:255]+"%09"+result["v"]["value"][31:255]+"%09S248%09"+wid
                                urlgbase = "https://quickstatements.toolforge.org/api.php?action=import&submit=1&username={{username}}&token={{token}}&format=v1&data="
                                urlg = urlgbase + ux
                                xf = requests.post(urlg)
                                g.write(ux+"\n")
                                g.flush()
g.close()                           
                        
