from rdflib import Graph
import json
from datetime import datetime

g = Graph()
g.parse('src/data/VGW_datasets/letters.nt', format='nt')

letter_query = """
SELECT DISTINCT ?id ?date ?sender ?recipient
WHERE {
    ?object a <http://schema.org/Message> .
    ?object <http://schema.org/identifier> ?id .
    ?object <http://schema.org/dateSent> ?date .
    ?object <http://schema.org/sender> ?sender_uri .
    ?sender_uri <http://schema.org/name> ?sender .
    ?object <http://schema.org/recipient> ?recipient_uri .
    ?recipient_uri <http://schema.org/name> ?recipient .
    }
"""

letters = g.query(letter_query)

letter_data = []
count = 0
for row in letters:
    dt = datetime.strptime(row.date, "%Y-%m-%d")
    letter_data.append({
        "id": row.id,
        "date_sent": row.date,
        "year_sent": str(dt.year),
        "sender": row.sender,
        "recipient": row.recipient
    })
    count += 1
    print(row.id, row.date, row.sender, row.recipient)

print(count)

with open("src/data/letter_data.json", "w") as output:
    json.dump(letter_data, output)