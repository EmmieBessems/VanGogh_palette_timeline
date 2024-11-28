from rdflib import Graph
import json

g = Graph()
g.parse('src/data/VGW_datasets/periods.nt', format="nt")

period_query = """
SELECT DISTINCT ?period ?start ?end ?locations
WHERE {
    ?object <http://www.w3.org/2000/01/rdf-schema#label> "Period in the life of Vincent van Gogh" .
    
    ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode1 .
    ?bnode1 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?period .
    
    ?object <http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span> ?bnode2 .
    ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin> ?start .
    ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end> ?end .
    
    ?object <http://www.cidoc-crm.org/cidoc-crm/P7_took_place_at> ?locationURIs .
    ?locationURIs <http://www.w3.org/2000/01/rdf-schema#label> ?locations .
    }
"""

periods = g.query(period_query)

period_data = []
count = 0
for row in periods:
    period_data.append({
        "period": row.period,
        "start": row.start,
        "end": row.end,
        "locations": row.locations
    })
    count += 1
    print(row.period, row.start, row.end, row.locations)

print(count)

with open("src/data/VGW_datasets/extracted_json_files/period_data_raw.json", "w") as output:
    json.dump(period_data, output)