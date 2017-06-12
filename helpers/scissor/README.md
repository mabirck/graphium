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

* [wand](https://github.com/py-bson/bson)
* [pymongo](https://pypi.python.org/pypi/pymongo)

#### Install Dependencies on mac
`brew install imagemagick@6`
`brew unlink imagemagick`
`brew link imagemagick@6 --force`
`pip install wand`