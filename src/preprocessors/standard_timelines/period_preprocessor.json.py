import pandas as pd

period_df = pd.read_json("src/data/VGW_datasets/extracted_json_files/period_data_raw.json")

# Aggregated rows on period/start/end to get a list of possible locations per row
aggregated_df = period_df.groupby(["period", "start", "end"]).agg(tuple).map(list).reset_index()

# Remove periods that have no paintings (early period, Borinage/Brussels, Etten)
sorted_df = aggregated_df.sort_values(by="start")
final_df = sorted_df.iloc[3:].reset_index(drop=True)

# Remove the date between brackets for the period name
# Also add an image URL for the background (for display in Observable Plot)
period_names = []
background_URLs = []
for i in range(len(final_df)):
    split = final_df.loc[i, "period"].split("(")
    period_names.append(split[0].strip())

    if i % 2 == 0:
        background_URLs.append("https://cdn.jsdelivr.net/gh/EmmieBessems/vanGogh_painting_images/period_background1.jpg")
    else: 
        background_URLs.append("https://cdn.jsdelivr.net/gh/EmmieBessems/vanGogh_painting_images/period_background2.jpg")

final_df["period"] = period_names
final_df["background"] = background_URLs

# Add Saint-Rémy-de-Provence and The Hague as locations in the associated periods
final_df.at[0, "locations"] = ["Den Haag", "The Hague"]
final_df.at[5, "locations"] = ["Saint-Rémy", "Saint-Rémy-de-Provence"]

# Save the resulting dataframe as a JSON
final_df.to_json(r"src/data/period_data.json", orient="records")