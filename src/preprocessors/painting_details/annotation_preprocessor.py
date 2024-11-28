import pandas as pd

annotation_df = pd.read_json("src/data/VGW_datasets/extracted_json_files/letter_annotations_data_raw.json")

# Extract the letter ID from the letter URL and the painting ID from the mentions
letterID_list = []
paintingID_list = []
for i in range(len(annotation_df)):
    let_ID = annotation_df.loc[i, "letterURL"].split("/")[-2]
    letterID_list.append(let_ID[3:])

    painting_ID = annotation_df.loc[i, "paintingMentions"].split("/")[-1]
    paintingID_list.append(painting_ID)

annotation_df["letterID"] = letterID_list
annotation_df["fnumber"] = paintingID_list

# Drop the paintingsMentions column since it is not necessary for further processing
final_df = annotation_df.drop("paintingMentions", axis="columns")

final_df.to_json(r"src/data/letter_annotations_data.json", orient="records")