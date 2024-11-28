from rdflib import Graph
import json
import datetime as dt

g = Graph()
g.parse('src/data/VGW_datasets/vgm_amsterdam.nt', format='nt')
# g.parse('src/data/VGW_datasets/kroller_muller.nt', format='nt')
# g.parse("src/data/VGW_datasets/centraalmuseum_utrecht.nt", format='nt')
# g.parse("src/data/VGW_datasets/rijksmuseum_amsterdam.nt", format="nt")

# Query checks for the following
# Line 21 --> select all distinct titles, begintimes, endtimes, and locations
# Line 23 --> object has type painting
# Line 24 --> object is identified by a bnode
# Line 25 --> bnode has type 'preferred title' (signals it contains the object's title)
# Line 26 --> bnode has language 'english' to ensure we extract the english title
# Line 27 --> extract the filtered bnode's symbolic content as the title feature
# Line 28 --> object has a production node that I name production
# Line 29 --> production has a time span node that I name period
# Line 30 --> period has a begin of the begin node that I name begintime
# Line 31 --> period has an end of the end node that I name endtime
# Line 32 --> production has a took place at node that I name locationuri
# Line 33 --> locationuri has a preferred label that I name location
# Line 34 --> only select the locations that have language 'en' (english)
painting_query = """
SELECT DISTINCT ?fnumber ?title ?museumid ?jhnumber ?begintime ?endtime ?displaytime ?location ?currentowner ?link
WHERE {
    ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode1 .
    ?bnode1 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?fnumber .
    { SELECT DISTINCT ?fnumber
    WHERE {
        { ?object <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vangoghmuseum.nl/data/term/4200> . }
        UNION
        { ?object <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vocab.getty.edu/aat/300033618> . } 
        UNION
        { ?object <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <https://id.rijksmuseum.nl/22016> . }
        ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode . 
        ?bnode <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <https://vangoghworldwide.org/data/concept/f_number> .
        ?bnode <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?fnumber .
        }
    }

    ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode2 .
    { ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vocab.getty.edu/aat/300404670> .
    ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P72_has_language> <http://vocab.getty.edu/aat/300388277> .
    ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?title . }
    UNION
    { ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vocab.getty.edu/aat/300417193> .
    ?bnode2 <http://www.cidoc-crm.org/cidoc-crm/P73_has_translation> ?titlenode . 
    ?titlenode <http://www.cidoc-crm.org/cidoc-crm/P72_has_language> <http://vocab.getty.edu/aat/300388277> .
    ?titlenode <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?title . }

    OPTIONAL { ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode3 .
    ?bnode3 <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <http://vocab.getty.edu/aat/300312355> .
    ?bnode3 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?museumid . }

    OPTIONAL { ?object <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode4 .
    ?bnode4 <http://www.cidoc-crm.org/cidoc-crm/P2_has_type> <https://vangoghworldwide.org/data/concept/jh_number> .
    ?bnode4 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?jhnumber. }

    ?object <http://www.cidoc-crm.org/cidoc-crm/P108i_was_produced_by> ?production .
    ?production <http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span> ?period .
    ?period <http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin> ?begintime .
    ?period <http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end> ?endtime .
    
    OPTIONAL { ?period <http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by> ?bnode5 .
    ?bnode5 <http://www.cidoc-crm.org/cidoc-crm/P190_has_symbolic_content> ?displaytime . }

    OPTIONAL { ?production <http://www.cidoc-crm.org/cidoc-crm/P7_took_place_at> ?location . }

    ?object <http://www.cidoc-crm.org/cidoc-crm/P52_has_current_owner> ?currentowner . 
    ?object <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?link .
    }
"""

paintings = g.query(painting_query)

vgm_data = []
count = 0
for row in paintings:
    vgm_data.append({
        "fnumber": row.fnumber,
        "jhnumber": row.jhnumber,
        "museumid": row.museumid,
        "title": row.title,  
        "start": row.begintime,
        "end": row.endtime,
        "display": row.displaytime,
        "location": row.location, 
        "current_owner": row.currentowner,
        "link": row.link
        })
    count += 1
    print(row.fnumber, row.jhnumber, row.museumid, row.title, row.begintime, row.endtime, row.displaytime, row.location, row.currentowner, row.link)

print(count)  
# with open("src/data/VGW_datasets/extracted_json_files/vgm_data.json", "w") as output:
#     json.dump(vgm_data, output)
