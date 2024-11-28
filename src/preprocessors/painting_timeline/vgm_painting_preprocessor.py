import json
import pandas as pd

vgm_df = pd.read_json('src/data/VGW_datasets/extracted_json_files/vgm_data.json')
annotation_df = pd.read_json('src/data/letter_annotations_data.json')

# Code to replace unprocessed uri's with human readable strings (for production location and current owner)
# print(paintings_df.location.unique())
locationuri_dict = {
    "http://vocab.getty.edu/tgn/7006835": "Nuenen",
    "http://vocab.getty.edu/tgn/7008038": "Paris",
    "http://vocab.getty.edu/tgn/7008775": "Arles",
    "http://vocab.getty.edu/tgn/7008030": "Auvers-sur-Oise",
    "http://vocab.getty.edu/tgn/7003614": "Drenthe",
    "http://vocab.getty.edu/tgn/7009654": "Saint-Rémy-de-Provence",
    "http://vocab.getty.edu/tgn/7006810": "The Hague",
    "http://vocab.getty.edu/tgn/7007856": "Antwerp",
    "http://vocab.getty.edu/tgn/7008792": "Saintes-Maries-de-la-Mer",
    "http://vocab.getty.edu/tgn/7006824": "Etten",
    "http://vocab.getty.edu/tgn/7006952": "Amsterdam",
    "http://vocab.getty.edu/tgn/1047973": "Nieuw-Amsterdam"
}

owneruri_dict = {
    "http://vocab.getty.edu/ulan/500275558": "Van Gogh Museum",
    "http://vocab.getty.edu/ulan/500235923": "Kröller-Müller Museum",
    "http://vocab.getty.edu/ulan/500246547": "Rijksmuseum"
}

def uri_replacer(df, column_name: str, uri_dict: dict):

    replacement_list = []

    for i in range(len(df)):
        for key in uri_dict:
            if df[column_name][i] == key:
                replacement_list.append(uri_dict[key])

    return replacement_list

vgm_df["location"] = uri_replacer(vgm_df, "location", locationuri_dict)
vgm_df["current_owner"] = uri_replacer(vgm_df, "current_owner", owneruri_dict)

# Code to add image url's and edit the VGWw url's in the extracted data
def url_generator(df):

    image_url_list = []
    vgww_url_list = []

    for i in range(len(df)):
        image_url = "https://cdn.jsdelivr.net/gh/EmmieBessems/vanGogh_painting_images/" + str(df["fnumber"][i]) + ".jpg"
        image_url_list.append(image_url)

        # We also edit the "link" property to ensure we have the correct VGWw link
        vgww_url = df["link"][i]
        vgww_url_list.append(vgww_url.replace("/data", ""))

    return image_url_list, vgww_url_list

image_urls, vgww_urls = url_generator(vgm_df)
vgm_df["Image"] = image_urls
vgm_df["link"] = vgww_urls

# Code to check whether a painting appears in the pigments dataset, and add a feature accordingly
vgm_pigments_df = pd.read_json("src/data/vgm_pigment_counts.json")

analyzed = vgm_pigments_df["painting"].unique()
analyzed_log = []
for i in range(len(vgm_df)):
    if vgm_df["fnumber"][i] in analyzed:         
        analyzed_log.append("Yes")
    else:
        analyzed_log.append("No")

vgm_df["analyzed"] = analyzed_log

# Code to ensure every display date starts with a capital letter (for niceness when displaying the dates :p)
vgm_df.display = vgm_df.display.str.title()

# Code to add a list of associated letters to each painting in the df
merged_df = vgm_df.merge(annotation_df, how="left", on="fnumber")
aggregated_df = merged_df.groupby(["fnumber", "jhnumber", "museumid", "title", "start", "end", "display", "location", "current_owner", "link", "Image", "analyzed"]).agg(tuple).map(list).reset_index()

# For some reason there is some data loss when aggregating, so the missing rows are appended to the dataframe
missing_list = list(vgm_df[~vgm_df[['fnumber']].astype(str). apply(tuple, 1).isin(aggregated_df[['fnumber']].astype(str).apply(tuple, 1))]["fnumber"])
for fnumber in missing_list:
    missing_row = merged_df[merged_df["fnumber"] == fnumber].reset_index()
    missing_row["letterID"] = [[missing_row.loc[0, "letterID"]]]
    missing_row["letterURL"] = [[missing_row.loc[0, "letterURL"]]]
    aggregated_df = aggregated_df._append(missing_row, ignore_index=True)

# Remove additional index column to get the final result
final_df = aggregated_df.drop("index", axis="columns")

# Save the preprocessed dataframe to a new JSON
final_df.to_json(r"src/data/painting_data_full_images.json", orient="records")
