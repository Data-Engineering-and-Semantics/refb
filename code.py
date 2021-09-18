# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from Bio import Entrez
from Bio import Medline
import requests
import wikibaseintegrator
import datetime


# Logging in with Wikibase Integrator
print("Logging in with Wikibase Integrator")
login_instance = wbi_login.Login(user=USER, pwd=PASSWORD)

# Getting the current date
datestr = '+' + str(datetime.datetime.now())[0:10] + 'T00:00:00Z'

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

xt = False
while (xt == False):
    xt = True
    try:
        results = get_results(endpoint_url, query)
    except:
        xt = False
    print(xt)

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
                                statements = []
                                source = [
                                   [
                                          wbi_datatype.ItemID(value=wid, prop_nr="P248", is_reference=True, if_exists="APPEND"),
                                          wbi_datatype.Time(time=datestr, prop_nr="P813", is_reference=True, if_exists="APPEND")
                                   ]
                                ]
                                statement = wbi_datatype.ItemID(value=result["v"]["value"][31:255], prop_nr=result["property"]["value"][31:255], references=source, if_exists="APPEND")
                                statements.append(statement)
                                item = wbi_core.ItemEngine(data=statements, item_id=result["item"]["value"][31:255])
                                item.write(login_instance, edit_summary="Added from OpenCitations COCI API using [[User:OpenCitations Bot|OpenCitations Bot]]")
                         
                        
