import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re
from datetime import datetime

antwerp_table = pd.read_csv("src/data/pigment_data/Antwerp_Pigments.csv")
astra_table = pd.read_csv("src/data/pigment_data/AStRA_Pigments.csv")
dutch_table = pd.read_csv("src/data/pigment_data/Dutch_Pigments.csv")
olive_table = pd.read_csv("src/data/pigment_data/OliveGrove_Pigments.csv", encoding='unicode_escape')
paris_table = pd.read_csv("src/data/pigment_data/Paris_Pigments.csv", encoding='unicode_escape')

# Preprocess Antwerp table: 
# add F before each De la Faille number, change column names and make all lower case, throw away unncessesary data
for row in antwerp_table.index:
    antwerp_table.loc[row, "De la Faille number"] = "F" + str(antwerp_table.loc[row, "De la Faille number"])

antwerp_table.drop(columns=["Catalogue Number", "Title", "Date", "Area"], inplace=True)
antwerp_table.rename(columns={"De la Faille number": "fnumber", 
                              "BaSO4 sulphate": "barium sulphate", 
                              "CaCO3": "calcium carbonate",
                              "Gypsum": "calcium sulphate", 
                              "French ultramarine": "ultramarine blue", 
                              "Cobalt": "cobalt blue",
                              "Minium": "red lead"}, inplace=True)
antwerp_table.columns = map(str.lower, antwerp_table.columns)
antwerp_table["source"] = "antwerp_table"

# Preprocess Dutch table: 
# add F before each De la Faille number, change column names, throw away unncessesary data
for row in dutch_table.index:
    dutch_table.loc[row, "F no."] = "F" + str(dutch_table.loc[row, "F no."])

dutch_table.drop(columns=["Title", "JH no.", "Period", "Area"], inplace=True)
dutch_table.rename(columns={"F no.": "fnumber", 
                            "(aluminium) silicates": "silicates",
                            "yellow ochre": "yellow ochre/sienna", 
                            "red ochre": "orange/red ochre", 
                            "carbon black": "unspecified carbon black/brown"}, inplace=True)
dutch_table.columns = map(str.lower, dutch_table.columns)
dutch_table["source"] = "dutch_table"

# Preprocess olive table: 
# add F before each De la Faille number and convert to string, change column names, throw away unncessesary data
olive_table["F-no"] = olive_table["F-no"].apply(str)
for row in olive_table.index:
    olive_table.loc[row, "F-no"] = "F" + str(olive_table.loc[row, "F-no"])

olive_table.drop(columns=["Title", "Collection", "Date"], inplace=True)
olive_table.rename(columns={"F-no": "fnumber", 
                            "Red ochre": "orange/red ochre"}, inplace=True)
olive_table.columns = map(str.lower, olive_table.columns)
olive_table["source"] = "olive_table"

# Preprocess Paris table: 
# add F before each De la Faille number, change column names, throw away unncessesary data
for row in paris_table.index:
    paris_table.loc[row, "De la Faille number"] = "F" + str(paris_table.loc[row, "De la Faille number"])

paris_table.drop(columns=["Catalogue Number", "Title", "Date", "Area"], inplace=True)
paris_table.rename(columns={"De la Faille number": "fnumber", 
                            "BaSO4": "barium sulphate", 
                            "CaCO3": "calcium carbonate", 
                            "Gypsum": "calcium sulphate", 
                            "French ultramarine": "ultramarine blue", 
                            "Cobalt": "cobalt blue",
                            "Minium": "red lead", 
                            "Carbon black/brown": "unspecified carbon black/brown"}, inplace=True)
paris_table.columns = map(str.lower, paris_table.columns)
paris_table["source"] = "paris_table"

# Discard the last row of the astra table, change column names, throw away unnessecary data
astra_table = astra_table[:-1]
astra_table.drop(columns=["Title", "Period", "Area"], inplace=True)
astra_table.rename(columns={"F no.": "fnumber", 
                            "yellow ochre": "yellow ochre/sienna", 
                            "eosin": "eosin lake", 
                            "carbon black": "unspecified carbon black/brown"}, inplace=True)
astra_table.columns = map(str.lower, astra_table.columns)
astra_table["source"] = "astra_table"

def pigment_occurrence(pigment_table, painting_table, pigment_base_table): 

    # Empty dataframe that we will fill continuously per row
    result = pd.DataFrame()

    for row in range(len(pigment_table)): 

        # Extract row, transpose
        pigment_table_row = pigment_table.iloc[row].T

        # Throw out NaNs, add a column where fnumbers and table names get repeated (remove fnumber row), reset indices
        pigment_table_row.dropna(inplace=True)
        pigment_table_row = pigment_table_row.reset_index()  
        pigment_table_row["painting"] = pigment_table_row.loc[0].iloc[1]
        pigment_table_row["source"] = pigment_table_row.loc[np.where(pigment_table_row == "source")[0][0]].iloc[1]
        pigment_table_row.columns.values[0] = "pigment"
        pigment_table_row.columns.values[1] = "details"
        pigment_table_row.drop(index=0, inplace=True)

        # Set an excemption: if no pigments are found in the painting, skip that row (don't add to result df!)
        if len(pigment_table_row) == 0:
            continue

        pigment_table_row = pigment_table_row.reset_index()
        pigment_table_row.drop(columns=["index"], inplace=True)

        # Add year based on f-number
        f_row = painting_table[painting_table["fnumber"] == pigment_table_row.loc[0, "painting"]]
        start = f_row["start"].iloc[0]
        end = f_row["end"].iloc[0]
        # For now we choose the year based on the start of the range, but this can also be middle, end,
        # or we can even add multiple years if the range crosses through multiple years
        pigment_table_row["year"] = str(datetime.strptime(start, "%Y-%m-%d").year)
        
        # Add colorgroup based on the pigment base table
        color_df = pigment_base_table[pigment_base_table["pigment"].isin(list(pigment_table_row["pigment"]))]
        pigment_table_row = pd.merge(pigment_table_row, color_df, on="pigment")

        # Remove leading and trailing end spaces from any entries in the "details" column
        pigment_table_row["details"] = pigment_table_row["details"].apply(lambda x: x.strip())
        # Replace "X" markers with "-" markers and "o" markers with "x" markers to ensure technique is processed correctly
        pigment_table_row["details"] = pigment_table_row["details"].replace("X", "-")
        pigment_table_row["details"] = pigment_table_row["details"].replace("o", "x")

        # Add empty columns for uncertainty, technique, and elements/notes to fill up later on the go
        pigment_table_row["uncertainty"] = None
        pigment_table_row["technique"] = None
        pigment_table_row["notes"] = None
        # pigment_table_row["element"] = None

        # Iteratively alter the pigment rows based on the given details
        for i in range(len(pigment_table_row)):
            
            # Since multiple techniques or elements/notes can be attributed, create lists to add entries to
            technique_list = []
            notes_list = []

            # Add technique based on main cell entry ("x" = xrf, starts with "o" specifically for olive table)
            if (pigment_table_row["details"][i] == "x") or (pigment_table_row["details"][i].startswith("o")):
                technique_list.append("XRF")
                pigment_table_row.at[i, "technique"] = technique_list
            if (pigment_table_row["details"][i] == "s"):
                technique_list.append("OM and SEM-EDX")
                pigment_table_row.at[i, "technique"] = technique_list
            if (len(pigment_table_row["details"][i]) != 1):

                # Case 1 for paris table
                if pigment_table_row["details"][i].startswith("X"):
                    split = pigment_table_row["details"][i].split()
                    notes_list.append(" ".join(split[1:])) 
                    pigment_table_row.at[i, "notes"] = notes_list
                
                # Case 2 for olive table
                elif pigment_table_row["details"][i].startswith("o"):
                    split = pigment_table_row["details"][i].split("o")
                    for element in split:
                        element = element.strip()
                        if element == "?":
                            pigment_table_row.loc[i, "uncertainty"] = "Possibly"
                        elif element.startswith("("):
                            notes_list.append(element.strip("()"))
                            pigment_table_row.at[i, "notes"] = notes_list

                # Case 3 for Astra table
                elif pigment_table_row["source"][i] == "astra_table":
                    techniques = {"x": "XRF", "d": "XRD", "s": "OM and SEM-EDX", "r": "μ-raman", "p": "PIXE", "h": "HPLC"}
                    notes = {"1": "1 = possibly also other chromium-containing yellow pigments present",
                             "2": "2 = possibly also another copper-containing green pigment present",
                             "3": "3 = possibly chrome green, a commercial mixture of Prussian blue and chrome yellow",
                             "4": "4 = a yellow dye was also detected",
                             "5": "5 = mixed with calcium sulphate", 
                             "6": "6 = mixed with calcium carbonate", 
                             "7": "7 = as charcoal, probably used for the underdrawing",
                             "8": "8 = possibly not original paint"}
                    split = pigment_table_row["details"][i].split(",")
                    for element in split:
                        element = element.strip()
                        if (element == "s") or (element == "x") or (element == "h"):
                            technique_list.append(techniques[element])
                        elif len(element) == 2:
                            technique_list.append(techniques[element[0]])
                            if element[1] == "?": 
                                pigment_table_row.loc[i, "uncertainty"] = "Possibly"
                            elif element[1].isnumeric():
                                notes_list.append(notes[element[1]])
                                # pigment_table_row.loc[i, "notes"] = notes[element[1]]
                        # Just in case any comma's within brackets were not removed
                        elif element.startswith("starch"):
                            continue
                        elif element.endswith("(?)"):
                            pigment_table_row.loc[i, "uncertainty"] = "Probably"
                        else:
                            technique_list.append(techniques[element[0]]) # Will not work for s? (for example)
                            if element[1] == "?": # Solution for s?
                                pigment_table_row.loc[i, "uncertainty"] = "Possibly"
                            if (element.endswith(")")) and (element[3] != "y"):
                                notes_list.append(element[element.find("(") + 1: -1])
                            elif (element.endswith(")")) and (element[3] == "y"):
                                if element[element.find("(") + 1: -1] == "y":
                                    pigment_split = pigment_table_row["pigment"][i].split()
                                    pigment_table_row.loc[i, "pigment"] = " ".join([pigment_split[0], pigment_split[1]])
                                else:
                                    if any(chr.isdigit() for chr in element):
                                        note_nr = [i for i in element if i.isdigit()]
                                        notes_list.append(notes[note_nr[0]])
                                        # pigment_table_row.loc[i, "notes"] = notes[note_nr[0]]
                            else: # This is now all elements that do not end in a bracket, but in a note nr
                                # Add note to the notes list
                                notes_list.append(notes[element[-1]])
                                # pigment_table_row.loc[i, "notes"] = notes[element[-1]]
                                # Add either an element or change the pigment name depending on the content between brackets
                                between_brackets = element[element.find("(") + 1: element.find(")")]
                                if (between_brackets[0] == "y") and (len(between_brackets) == 1):
                                    pigment_split = pigment_table_row["pigment"][i].split()
                                    pigment_table_row.loc[i, "pigment"] = " ".join([pigment_split[0], pigment_split[1]])
                                elif (between_brackets[0] == "y") and (len(between_brackets) > 1):
                                    continue
                                else:
                                    notes_list.append(between_brackets)

                    pigment_table_row.at[i, "technique"] = technique_list
                    pigment_table_row.at[i, "notes"] = notes_list

                # Case 4 for the Dutch table
                elif pigment_table_row["source"][i] == "dutch_table":
                    techniques = {"x": "XRF", "s": "OM and SEM-EDX"}
                    notes = {"1": "1 = as chrome green", 
                             "2": "2 = probably as chrome green", 
                             "3": "3 = probably also chrome green",
                             "4": "4 = as chrome green + barium sulphate",
                             "5": "5 = probably also as chrome green + barium sulphate",
                             "6": "6 = as chrome green, probably also Prussian blue",
                             "7": "7 = probably chrome green + barium sulphate, probably also Prussian blue",
                             "8": "8 = only in green underlayer",
                             "9": "9 = only in green",
                             "10": "10 = only in bright green",
                             "11": "11 = iron oxide",
                             "12": "12 = ochre and iron oxide",
                             "13": "13 = probably cochineal, aluminium/calcium substrate",
                             "14": "14 = aluminium/sulphur (?) substrate, shows orange-pink UV-fluorescence",
                             "15": "15 = shows orange-pink UV-fluorescence",
                             "16": "16 = madder, aluminium/sulphur/potassium substrate"}
                    element = pigment_table_row["details"][i]
                    if element.startswith("s"):
                        technique_list.append("OM and SEM-EDX")
                        if element[1] == "?":
                            pigment_table_row.loc[i, "uncertainty"] = "Possibly"
                        elif element[2].isnumeric():
                            note_nr = element[2:]
                            notes_list.append(notes[note_nr])
                            # pigment_table_row.loc[i, "notes"] = notes[note_nr]
                        elif element[2] == "(":
                            between_brackets = element[element.find("(") + 1: element.find(")")]
                            notes_list.append(between_brackets)
                    else:
                        notes_list.append(element)
                    
                    pigment_table_row.at[i, "technique"] = technique_list
                    pigment_table_row.at[i, "notes"] = notes_list

            # Change pigment entries based on marked letters in the cells (i.e. chrome yellow or orange becomes chrome orange with "O" entry)
            if pigment_table_row["details"][i] == "O":
                split = pigment_table_row["pigment"][i].split()
                pigment_table_row.loc[i, "pigment"] = " ".join([split[0], split[-1]])
                pigment_table_row.loc[i, "colorgroup"] = "orange"
            if (pigment_table_row["details"][i] == "Y") or (pigment_table_row["details"][i] == "yellow"):
                split = pigment_table_row["pigment"][i].split()
                pigment_table_row.loc[i, "pigment"] = " ".join([split[0], split[1]])

            # Add "possibly" and "probably" markers to the uncertainty column based on marked cells
            if pigment_table_row["details"][i] == "?":
                pigment_table_row.loc[i, "uncertainty"] = "Possibly"

            # # Separate note addition for olive table for viridian pigment
            # if (pigment_table_row["pigment"][i] == "viridian") and (pigment_table_row["source"][i] == "olive_table"):
            #     pigment_table_row.loc[i, "notes"] = "By XRF no differentiation can be made between opaque and transparent chromium oxide green (viridian)"

        result = result._append(pigment_table_row)

    # Final index reset
    result = result.reset_index()
    result.drop(columns=["index"], inplace=True)

    return result

# Combine all datasets into one
# pigment_table = pd.concat([antwerp_table, paris_table, olive_table, dutch_table, astra_table], axis=0, ignore_index=True)
pigment_table = pd.concat([antwerp_table, dutch_table, olive_table, paris_table, astra_table], axis=0, ignore_index=True)
# print(pigment_table["source"].unique())

# Load the pigment names and colorgroups json and the VGM paintings to compare
pigment_base_table = pd.read_json("src/data/pigment_colorgroups.json")
painting_table = pd.read_json("src/data/vgm_data_full_images.json")

# Filter pigment table based on F-numbers present in the paintings set
vgm_pigment_table = pigment_table[pigment_table["fnumber"].isin(list(painting_table["fnumber"]))]
print(vgm_pigment_table[["fnumber", "lead white", "chrome yellow or orange", "eosin lake", "source"]].to_string())

# pigment_occurrence(vgm_pigment_table, painting_table, pigment_base_table)
# print(pigment_occurrence(vgm_pigment_table, painting_table, pigment_base_table).to_string())

# result_table = pigment_occurrence(vgm_pigment_table, painting_table, pigment_base_table)
# result_table.to_json(r"./src/data/vgm_pigment_counts.json", orient="records")


