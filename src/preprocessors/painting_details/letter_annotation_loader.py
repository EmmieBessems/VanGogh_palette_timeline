from rdflib import Graph
import json

g = Graph()
g.parse('src/data/VGW_datasets/letters.nt', format='nt')

annotation_query = """
SELECT DISTINCT ?url ?mentions
WHERE {
    ?object a <http://www.w3.org/ns/oa#Annotation> .
    ?object <http://schema.org/url> ?url .

    ?object <http://www.w3.org/ns/oa#body> ?body .
    ?body <http://schema.org/mentions> ?mentions .
}
"""

annotations = g.query(annotation_query)

annotation_data = []
count = 0
for row in annotations:
    annotation_data.append({
        "letterURL": row.url,
        "paintingMentions": row.mentions,
    })
    count += 1
    print(row.url, row.mentions)

print(count)
with open("src/data/VGW_datasets/extracted_json_files/letter_annotations_data_raw.json", "w") as output:
    json.dump(annotation_data, output)