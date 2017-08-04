
# OpenStreetMap Wrangling with MongoDB

### Justin Rogers

Map Area: Boulder CO, United States  
[Boulder on OpenStreetMaps](http://www.openstreetmap.org/relation/112298)  
[Overpass API Link for Boulder](http://overpass-api.de/api/map?bbox=-105.4142,39.9490,-105.0653,40.1099)

### [1. Problems Encountered in the Map](#section1)
[Street Type Inconsistencies](#section1_1)  
[City Name Differences](#section1_2)  
[Postal Code Problems](#section1_3)  
### [2. Data Overview](#section2)
### [3. Additional Ideas](#section3)
[Basic Field Validations on Data Entry](#section3_1)  
[Conclusion](#section3_2)  

##  <a id='section1'>1. Problems Encountered in the Map</a>

Several problems/inconsistencies were identified in the data:
* Street Type Inconsistencies (Avenue, ave, Ave)
* City Name Differences (Boulder, Boulder, CO, u'Boulder, CO \u200e')
* Postal Code Problems (80026, 80026-2872, CO 80027)

###  <a id='section1_1'>Street Type Inconsistencies</a>
Many of the street names had inconsistencies with the street type naming conventions. Before export to JSON, the ends of the street names were remapped for conistency. Ex. St., st, and St. were all changed to Street

###  <a id='section1_2'>City Name Differences</a>
13 different city names were present in the data, but several were just inconsistent capitilizations or extra data in the field. These fields were mapped to consistent names before conversion to JSON. Ex. Boulder, Co converted to Boulder. Unfortunately, one city name, CO, was not changed as this would require looking up the individual entries to decide in which city the place actually was.

###  <a id='section1_3'>Postal Code Problems</a>
20 different postal codes were indentified in the data. Several had the additional four digits attached to the end with a dash. These extra digits were removed before conversion to JSON. In addition, two entries were prefixed with "CO " which was also removed. Unfortunately, one item was simply "CO" which was left in for the same reason as under City Name Differences above.

## <a id='section2'>2. Data Overview</a>

### Section showing basic dataset statistics and MongoDB queries used
#### File sizes


```python
import os
print "The boulder.osm file is %.1fMB" % (float(os.path.getsize('boulder.osm'))/1000000)
print "The boulderimport.json file is %.1fMB" % (float(os.path.getsize('boulderimport.json'))/1000000)
```

    The boulder.osm file is 91.5MB
    The boulderimport.json file is 101.6MB



```python
from pymongo import MongoClient
import pprint
client = MongoClient("mongodb://localhost:27017")
db = client.map
```

**Number of documents:**


```python
db.boul.find().count()                                                
```




    454451



**Number of nodes:**


```python
db.boul.find({"type":"node"}).count()
```




    406583



**Number of ways:**


```python
db.boul.find({"type":"way"}).count()
```




    47868



**Number of unique users:**


```python
len(db.boul.find().distinct("created.user"))
```




    657



**Number of Top Contributor:**


```python
top = db.boul.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}])
print list(top)
```

    [{u'count': 78482, u'_id': u'Berjoh'}]


**Top Ten Amenities:**


```python
amenity = db.boul.aggregate([{"$match": {"amenity": {"$exists": True}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])
for i in list(amenity):
    print i
```

    {u'count': 1161, u'_id': u'parking'}
    {u'count': 648, u'_id': u'bicycle_parking'}
    {u'count': 223, u'_id': u'restaurant'}
    {u'count': 174, u'_id': u'bench'}
    {u'count': 104, u'_id': u'fast_food'}
    {u'count': 99, u'_id': u'cafe'}
    {u'count': 99, u'_id': u'school'}
    {u'count': 74, u'_id': u'place_of_worship'}
    {u'count': 56, u'_id': u'bank'}
    {u'count': 48, u'_id': u'fuel'}


## <a id='section3'>3. Additional Ideas</a>

### <a id='section3_1'>Basic Field Validation on Data Entry</a>  
Most programs have basic field validations to improve the quality of data being input into the system. Some of the problems in the data could be fixed during entry just by having formatting masks (e.g only allowing five integers in zip codes) and performing check routines (e.g. are those gps coordinates in or near the zip code being tagged).
* **Benefits**  
As common errors on certain field types are identified, these new checks can be put in place. These field validations and check routines will provide better data on initial input which will ultimately lesson the burden of manually/programmically cleaning the data.
* **Anticipated Issues**  
The world is a big place and different locations have different conventions for place names, street names, postal codes, etc. Coming up with common validations and using traditional programming routines to check for this variety (i.e. long if/else statements) can be problematic to build and will never capture the infinite variety of these errors. Also adding to the complexity are the myriad of languages around the world. Deep learning could be used to review datasets with correct and incorrect tags. This could correct entries to a certain probabilty threshold while flaging others for review, however the constant server burden could be cost prohibitive for an open source project.

### <a id='section3_2'>Conclusion</a>  
While a remarkable amount of data gets entered into OpenStreetMap, programmatic and manual cleaning after the data has been entered should be secondary to robust data validation upon entry. The data reviewed was fairly clean, but there appears to be a number of small anomalies (e.g. 'CO' being entered as a postcode, Unicode characters being added to fields). While looking at a small set of data these problems are easily identified, as the dataset reviewed grows manual corrections and small cleaning routines are not able to keep up with the lack of consistency. 
