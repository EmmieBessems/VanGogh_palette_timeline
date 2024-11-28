import pandas as pd
import json
from datetime import datetime

letters_df = pd.read_json('src/data/letter_data.json')
letters_after_1880 = letters_df[letters_df["year_sent"] > 1880]
letter_counts = letters_after_1880.groupby("year_sent").count().reset_index()

letter_counts_list = []
for row in letter_counts.index:
    letter_counts_list.append({
        "year": str(letter_counts['year_sent'][row]),
        "key": "Letters",
        "count": int(letter_counts['id'][row])
    })

# Merge with the VGM painting data (so not yet all painting data!)
paintings_df = pd.read_json('src/data/vgm_data_full_images.json')

paintings_year_list = []
for i in range(len(paintings_df)):
    dt = datetime.strptime(paintings_df['start'][i], "%Y-%m-%d")
    paintings_year_list.append(str(dt.year))

paintings_df["year_start"] = paintings_year_list
painting_counts = paintings_df.groupby("year_start").count().reset_index()

painting_counts_list = []
for row in painting_counts.index:
    painting_counts_list.append({
        "year": str(painting_counts['year_start'][row]),
        "key": "Paintings",
        "count": int(painting_counts['fnumber'][row])
    })

painting_letter_counts = letter_counts_list + painting_counts_list

with open("src/data/vgm_paintings_real_letter_counts.json", "w") as output:
    json.dump(painting_letter_counts, output)




