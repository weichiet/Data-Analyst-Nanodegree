# Data Analyst Nanodegree
# Data Wrangling
## Wrangle OpenStreetMap Data

### [Project Description](./project_description.md)

### Code

The map that I’ve chosen for this project is Central Singapore, which can also be downloaded from [here](https://mapzen.com/data/metro-extracts/your-extracts/b64f3acb79eb). MongoDB was used as database for this project.

The `project_report.ipynb` notebook documents the data wrangling process and the analysis of the OSM map using MongoDB.   
The HTML version of the report was saved as `project_report.html`

The following Python files are also included:  
1) `create_sample.py`: Creating a sample of elements from the original OSM.  
2) `audit_map.py`: Auditing the OSM for problematic tags.   
3) `process_map.py`: Transforming the raw OSM file into a list of dictionaries and then JSON file.   

### Data
1) `central_singapore.zip`: Compressed file that contains OSM map of Central Singapore extracted from Mapzen.   
2) `sample.osm`: A sample part of the map region created by running `create_subsample.py`.
