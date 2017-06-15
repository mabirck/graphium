# Eraser

Erase the database from helper or application and files generated from those actions

### Run

`$ python Main.py [-c|-r]`

Attribute  |    Helper   | Description
---------- | ----------- | -----------
`-c`       |   Crawler   | remove all data crawled
`-r`       |   Reader    | remove all data inserted by reader OSM
`-s`       |   Swarm     | remove all sessions
`-i`       |   Scissor   | remove all cutted image

### Dependencies

If you want to install the packages manually, here's a
list:

* [pymongo](https://pypi.python.org/pypi/pymongo)
