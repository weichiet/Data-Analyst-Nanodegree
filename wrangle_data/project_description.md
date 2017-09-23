# Data Analyst Nanodegree
# Data Wrangling
## Project: Wrangle OpenStreetMap Data

### Introduction
Choose any area of the world in https://www.openstreetmap.org and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the OpenStreetMap data for a part of the world that you care about. Choose to learn SQL or MongoDB and apply your chosen schema to the project.

### Step One - Choose Your Map Area
Choose any area of the world from https://www.openstreetmap.org, and download a XML OSM dataset. The dataset should be at least 50MB in size (uncompressed). We recommend using one of following methods of downloading a dataset:

* Download a preselected metro area from [Map Zen](https://classroom.udacity.com/nanodegrees/nd002/parts/860b269a-d0b0-4f0c-8f3d-ab08865d43bf/modules/316820862075463/lessons/3168208620239847/concepts/77135319070923).
* Use the [Overpass API](http://overpass-api.de/query_form.html) to download a custom square area. Explanation of the syntax can found in the wiki. In general you will want to use the following query:(node(minimum_latitude, minimum_longitude, maximum_latitude, maximum_longitude);<;);out meta; e.g. (node(51.249,7.148,51.251,7.152);<;);out meta; the meta option is included so the elements contain timestamp and user information. You can use the Open Street Map Export Tool to find the coordinates of your bounding box. Note: You will not be able to use the Export Tool to actually download the data, the area required for this project is too large.

### Step Two - Process your Dataset
It is recommended that you start with the problem sets in your chosen course and modify them to suit your chosen data set. As you unravel the data, take note of problems encountered along the way as well as issues with the dataset. You are going to need these when you write your project report.

* SQL
  * Thoroughly audit and clean your dataset, converting it from XML to CSV format. Then import the cleaned .csv files into a SQL database using this schema or a [custom schema](https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f) of your choice.  


* MongoDB
  * Thoroughly audit and clean your dataset, converting it from XML to JSON format. Then import the cleaned .json file into a MongoDB database.


### Step Three - Explore your Database
After building your local database you’ll explore your data by running queries. Make sure to document these queries and their results in the submission document described below.

###  Step Four - Document your Work
Create a document (pdf, html) that directly addresses the following sections from the Project Rubric.

* Problems encountered in your map
* Overview of the Data
* Other ideas about the datasets
