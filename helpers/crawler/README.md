# Crawler
    
Find and crawler all imagens from repositories

#### Run

`$ python Main.py`

you can run in a silent mode
`$ nohup python Main.py -s &` 
In next line tip `disown` and press enter (if not unlock the terminal).

Attribute  | Description
---------- | -----------
`-s`       | don't ask nothing run! Run in silent mode

#### Repositories

List of repositories that you can crawl

* Flickr

### Dependencies

You can install Python dependencies using `pip install -r requirements.txt`,
and it should just work. If you want to install the packages manually, here's a
list:

* [bson](https://github.com/py-bson/bson)
* [pymongo](https://pypi.python.org/pypi/pymongo)

### Data and format

All files crawled will deposited on folder data/DATA_ORIGIN/ID.FORMAT

# Flicker API   
https://www.flickr.com/services/api/
    
## Main Gets
https://www.flickr.com/services/api/flickr.photos.search.html
https://www.flickr.com/services/api/flickr.photos.getWithGeoData.html
https://www.flickr.com/services/api/flickr.photos.getSizes.html

## Test api connection
https://api.flickr.com/services/rest/?method=flickr.test.echo&name=value&api_key=a6550e66205320e583d9bfb13a4b8634

### Search all photos
https://api.flickr.com/services/rest/?method=flickr.photos.search&tags=graffiti&api_key=a6550e66205320e583d9bfb13a4b8634&format=json

### Get information about one photo
https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id=33844414870&api_key=a6550e66205320e583d9bfb13a4b8634&format=json

### Get all sizes from photos
https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&photo_id=33844414870&api_key=a6550e66205320e583d9bfb13a4b8634&format=json