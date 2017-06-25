# Crawler
    
Scissor find and cut and all imagens from path on system/Configuration.py

#### Run

`$ python Main.py`

you can run in a silent mode `$ nohup python Main.py &` 
In next line tip `disown` and press enter (if not unlock the terminal).


#### Repositories

List of images that you can cut

* PNG
* JPEG
* GIF

### Dependencies

You can install Python dependencies using `pip install -r requirements.txt`,
and it should just work. If you want to install the packages manually, here's a
list:

* [wand](https://github.com/py-bson/bson)


## imageMagick Error
The image magic create files on temp folder and not remove. You can implement your own delete way. To solve this try this CRON that remove files each 5 minutes

`crontab -e`

append at end of file the code below

`MAILTO=YOUR@EMAIL.com #to maile you if has a error`

`*/5 * * * * sudo find /tmp/ -name "magick-*" -type f -delete`

and restart the service

`$ sudo service cron restart`

#### Install Dependencies on mac

`$ brew install imagemagick@6`

`$ brew unlink imagemagick`

`$ brew link imagemagick@6 --force`

`$ pip install wand`