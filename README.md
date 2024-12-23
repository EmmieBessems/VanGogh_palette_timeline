# VanGogh_palette_timeline
In this repository you can find all the code created for the interactive Van Gogh timeline tool, belonging to the Master thesis by Emmie Bessems with the title "An Interactive Timeline of Van Gogh's Palette". The Master thesis took place at Eindhoven University of Technology, and was finished in December 2024. A preview of the resulting timeline tool is hosted via a separate [GitHub pages repository](https://github.com/EmmieBessems/pigment_timeline_pages), on which a [recent build of the tool](https://emmiebessems.github.io/pigment_timeline_pages/) is deployed. Via the code in this repository you can:
1. Preprocess raw data to be suitable for the timeline tool.
2. Open the timeline tool as an Observable Framework project, and in this way further develop and build a static site to deploy the timeline tool. 

## General
The code for this project consists of two main parts: a data loading and preprocessing part written in Python, and a visualization and site building part written in Javascript. The visual below gives an idea of how the two are connected, as well as what underlying packages are used.

![technical_pipeline](https://github.com/user-attachments/assets/cd9a2411-6554-4796-90f5-ebda8c57be99)

The code in this repository mainly represents the creation of the visual tool with a subset of the Van Gogh oeuvre, namely the Van Gogh Museum collection. Through some easy file replacements the tool can also be generated for the full oeuvre, but please be aware that the loading times of the tool can become quite long in this case.

## Preprocessing
There are four types of data that need to be processed: 
1. Data coming from paintings, which are mainly images and metadata about the paintings. All images are gathered in a separate GitHub repository from which they are loaded into the tool. All metadata comes from the Van Gogh Worldwide shared Datasetregister page. The images can be found via [this link](https://github.com/EmmieBessems/vanGogh_painting_images), all raw metadata files (in the form of N-triples files, or .nt) can be found in src/data/VGW_datasets.
2. Data coming from letters, which are metadata and annotations gathered from the "Van Gogh the Letters" web-collection. The data for these letters comes in a similar format as the painting metadata and can be found in the same folder on this repository (letters.nt).
3. Additional production periods data, which represents the different era's in which Van Gogh's painting production can be divided. The data for these periods comes in a similar format as the painting metadata and can be found in the same folder on this repository (periods.nt).
4. Data coming from published pigment analysis studies, specifically from tables recording for different paintings what pigments were identified. These pigment tables can be found in src/data/pigment_data.

Within the src folder you will find the preprocessors folder, which contains all different Python files used for preprocessing the above mentioned datasets. These preprocessing files are ordered by the part of the timeline tool they provide the data for:
1. The standard timelines, which is a general overview of the production periods and a bar chart showing letter and painting counts for reference.
2. The painting timeline, which places painting thumbnail images directly on a timeline.
3. The pigment timeline, which summarizes all pigment records into yearly bins.
4. The painting details, which displays additional metadata and links for the current painting of interest.

In the sections below for each of these views the different preprocessors are described in some more detail.

### Standard timelines
1. period_loader.json.py loads the raw data from the N-triple file through SPARQL queries. Input is periods.nt, output is period_data_raw.json.
2. period_preprocessor.json.py preprocesses the period data into its final usable form. Input is period_data_raw.json, output is period_data.json.
3. letter_loader.json.py loads the raw data from the N-triple file through SPARQL queries, specifically the letter metadata used for counting the amount of letters per year. Input is letters.nt, output is letter_data.json.
4. letter_painting_counter.json.py counts the letters and paintings in the input files to generate a file with the total counts per category per year. Input is letter_data.json and painting_data_full_images.json (see painting timeline for more details), output is vgm_paintings_real_letter_counts.json.

### Painting timeline
1. blue_ntriple_loader.py loads the raw data from the N-triple files which fall in the blue category (see the table below). Input is any of the blue N-triple files, output is institutionName_data.json.
2. green_ntriple_loader.py loads the raw data from the N-triple files which fall in the green category. This includes the main data used in the tool currently; the Van Gogh Museum data. Input is any of the green N-triple files, output is institutionName_data.json.
3. vgm_painting_preprocessor.py prepares the Van Gogh Museum data specifically for later usage in the tool, but can easily be adjusted for any extracted painting metadata JSON file. It also adds the letter annotations (see painting details for more details). Input (for example) is VGW_datasets/extracted_json_files/vgm_data.json and letter_annotations_data.json, output is painting_data_full_images.

### Pigment timeline
1. pigment_loader_preprocessor.json.py loads in the separate pigment tables, combines these, and then preprocesses them for further use in the timeline tool. Input are the five pigment tables present in src/data/pigment_data, painting_data_full_images.json, and pigment_colorgroups.json (a supplementary file to match pigments to their associated color group), output is vgm_pigment_counts.json.

### Painting details
1. annotation_annotation_loader.py loads the raw data from the N-triple file through SPARQL queries, specifically the letter annotations used to match paintings to the letters they are mentioned in. Input is letters.nt, output is letter_annotation_data_raw.json.
2. annotation_preprocessor.py preprocesses the letter annotations for further matching with the painting metadata. Input is letter_annotations_data_raw.json, output is letter_annotations_data.json.

## Building the visual timeline tool
The timeline tool is created using Observable Framework as the static site generator. All necessary packages and formatting for building the tool through this framework can be found in the package-lock.json, package.json, observablehq.config.js files and in the src/observablehq folder. All the code for creating the actual visualizations and accompanying interactions can be found in the index.md file, which contains a mix of JavaScript and HTML code, as well as some formatting through MarkDown. An examplary build of the tool can be found in the dist folder.

For more information on developing and deploying through Observable Framework, please refer to [their documentation](https://observablehq.com/framework/). 




