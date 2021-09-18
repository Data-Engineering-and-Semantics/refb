# RefB
A bot to add reference support to Wikidata statements

## Context
This is a bot created by Houcemeddine Turki, member of Data Engineering and Semantics Research Team in University of Sfax, Tunisia. This bot was developed following WikiCred Grant Initiative that supports research, software projects and Wikimedia events that explore information reliability and credibility and its main purpose is to add references from PubMed Central to unsupported biomedical statements in Wikidata.

## Description
This bot recognizes Wikidata statements not supported by references using a SPARQL query (https://w.wiki/ZYm). Then, it uses PubMed Central search engine to find scholarly references for these statements. This is made possible using NCBI Entrez API (https://www.ncbi.nlm.nih.gov/books/NBK25499/) and Biopython (https://biopython.org/wiki/Documentation). Finally, the bot adds the found references to statements using Wikibase Integrator (https://github.com/LeMyst/WikibaseIntegrator).

## License
The source code is made available under GPL-3.0 License that allows the free sharing and reuse of its parts.

## Further reading
* Blog Post on Misinfocon: https://misinfocon.com/refdata-adding-trustworthiness-to-wikidata-d3cc68c21a6f
* Application of bot flag in Wikidata: https://www.wikidata.org/wiki/Wikidata:Requests_for_permissions/Bot/RefB_(WikiCred)
