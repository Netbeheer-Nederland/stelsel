import json
from rdflib import Graph, SKOS

# Instellingen
TTL_URL = "https://netbeheer-nederland.github.io/energiesysteembeheer/begrippenkader.ttl"
OUTPUT_JSON = "_data/begrippen.json"
BASE_URI = "https://begrippen.netbeheernederland.nl/id/"

g = Graph()
try:
    g.parse(TTL_URL, format="turtle") 
except Exception as e:
    print(f"Error loading TTL: {e}")
    exit(1)

# Dictionary: { "mer53": { "label": "laagtelwerk", "uri": "..." } }
lookup = {}

for s, p, o in g.triples((None, SKOS.prefLabel, None)):
    s_str = str(s)
    if s_str.startswith(BASE_URI):
        local_id = s_str.replace(BASE_URI, "")
        lookup[local_id] = {
            "label": str(o),
            "uri": s_str
        }

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(lookup, f, ensure_ascii=False, indent=2)

print(f"Generated: {OUTPUT_JSON} with {len(lookup)} concepts.")
