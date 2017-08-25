# OpenStreetMap Wrangling with MongoDB Project

[OpenStreetMap+Data+Wrangling+with+MongoDB.md](https://github.com/yaskyj/data-wrangling/blob/master/OpenStreetMap%2BData%2BWrangling%2Bwith%2BMongoDB.md)  
The project's Jupyter Notebook downloaded as Markdown. The Markdown preserves the inner document links for navigation.  

[OpenStreetMap Data Wrangling with MongoDB.ipynb](https://github.com/yaskyj/data-wrangling/blob/master/OpenStreetMap%20Data%20Wrangling%20with%20MongoDB.ipynb)  
The project's Juptyer Notebook file containing all explanations of data cleansing, queries, and conclusions. Queries were executed with pymongo within the notebook itself.  

[audit_street_names.py](https://github.com/yaskyj/data-wrangling/blob/master/audit_street_names.py)  
Python script to look up street names in order to see which abbreviations needed to be converted.  

[explore_tag_types.py](https://github.com/yaskyj/data-wrangling/blob/master/explore_tag_types.py)  
Python script to collect and print out different types of tags for review.  

[convert_to_json.py](https://github.com/yaskyj/data-wrangling/blob/master/convert_to_json.py)  
Python script which iterates through the complete osm file and converts it into JSON for upload into MongoDB.  

[boulderimport.json](https://github.com/yaskyj/data-wrangling/blob/master/boulderimport.json)  
JSON file created by convert_to_json.py for upload into MongoDB.  

[sample_extraction.py](https://github.com/yaskyj/data-wrangling/blob/master/sample_extraction.py)  
Python script which creates a file containing a sample of the entire osm for easier processing and review.  

[sample.osm](https://github.com/yaskyj/data-wrangling/blob/master/sample.osm)  
OSM file created by the sample_extraction.py script.  

[boulder.osm](https://github.com/yaskyj/data-wrangling/blob/master/boulder.osm)  
Original OSM file dowload containing all Boulder information.