# GRAPHIUM

## **Let me try pimp any city with amazing graffitis[^1]**


Find a class of imagens on ``Flickr`` and use the ``ImageNet`` to find those images on ``Google Street View`` and show this as a layout on ``Google Maps``.

## Structure
Bellow you can look how We slice the problem. In first row the 4 steps to show until show imagens under the map. The first column you can't se the packages (folders). The interception between they  is the applications that you can run. 

| Step/Packages | Extractor and Converter<br>``Flickr`` | Fine-tuning<br>``Imagenet`` | Searcher<br>``M.A.S``[^2] |Visualizator<br>``Ruby on Rails``|
| :-- | :-: | :-: | :-: | :-: | :-: | :-:
| `Helper` |  [Crawler](#crawler) [Scissor](#scissor) [Transfer](#transfer) | [Extractor](#extractor) | [Read_osm](#read_osm) |
| `Anima` | |  [Sun](#sun) [Nemesis](#nemesis) | |
| `Swarm` |  |   | [Swarm](#swarm) |
| `WebServer` | | |  | [WebApp](#webserver)
Read more about [**how to run**](#how_to) or [the packages](#package).

## Requirements

Make sure that you have a properly OS and Hardware to run this project

| Operation System | GPU | Storage
| :-: | :-: | :-:
| ![Ubuntu](https://img.shields.io/badge/platform-Ubuntu%20%7C%20macOS%20Sierra%20-lightgrey.svg) | ![Cuda](https://img.shields.io/badge/architecture-Cuda-green.svg) | ![HD](https://img.shields.io/badge/HD%20Available-≥%20300GB-orange.svg)


### Linguages and Libraries
Bellow you can see languages and libraries that you need on you OS system[^3]. Without they you can't run the project properly

| | Helper | Anima | Swarm | Webserver 
| :-- | :-: | :-: | :-: | :-: 
| **Linguages<br>& Libraries**| ![Python 2.7](https://img.shields.io/badge/Python-2.7-brightgreen.svg)![MongoDB](https://img.shields.io/badge/MongoDB-3.4-brightgreen.svg)<BR>![GDAL 1.11.5](https://img.shields.io/badge/Gdal-1.11.5-brightgreen.svg)<BR>![Wand 0.4.4](https://img.shields.io/badge/Wand-0.4.4-brightgreen.svg)<br>![osmread 0.1](https://img.shields.io/badge/Osmred-0.1-brightgreen.svg) | ![Python 2.7](https://img.shields.io/badge/Python-2.7-brightgreen.svg) ![keras 2.0.1](https://img.shields.io/badge/Keras-2.0.1-brightgreen.svg)<br> ![TensorFlow 2.0.1](https://img.shields.io/badge/TensorFlow-1.0.1-brightgreen.svg)<br>![imagenet 2016](https://img.shields.io/badge/Imagenet-2016-brightgreen.svg) | ![Python 2.7](https://img.shields.io/badge/Python-2.7-brightgreen.svg)![MongoDB](https://img.shields.io/badge/MongoDB-3.4-brightgreen.svg) | ![Ruby on Rails 4.1](https://img.shields.io/badge/Ruby%20on%20Rails-4.1-brightgreen.svg)<br> ![Ruby on Rails 4.1](https://img.shields.io/badge/Ruby-2.3.3-brightgreen.svg)<br>![Mysql  5.6](https://img.shields.io/badge/MySQL-5.6-brightgreen.svg)![MongoDB](https://img.shields.io/badge/MongoDB-3.4-brightgreen.svg)

<a name="how_to"></a>
# HOW TO RUN

To run you first need choose the label of imagens on flicker to used in [`Crawler`](#crawler). After choosed you need wait the set of images be download. You can config the labels, date initial and finish from images. What is the best label? Choose white wisdom :wink:. Doubt? Read more in your paper.

After, you will be allowed to cut with the [`Scissor`](#scissor) this imagens, that step is important but you can jump if the size of imagens crawled is similar to used in Anima. The cut process of images create a new repository (folder) and give you a way to separete the originals images from the used on trainning or classification.

The thrid step: Use [`Sun`](#sun) and view the classes that best activate your set of images[^4]. Now you need extract the originals files from imageNet. This action is important to execute the finetune.  After you can use the [`Transfer`](# transfer) to send a random subset of images from the repository to Synset choosed after analyse the sun executation.

The fourth step you use the [`Nemesis`](#nemesis) to realizing a fine tuning to allow the (old) Synset understand the new concept extracted in your subset of images.


<a name="package"></a>
## The Helpers

Helpers it's a set of scripts used to extract and manipulate files. See under each of those scripts and you description.


<a name="crawler"></a>
### Crawler
> Get a set of imagens from Flickr to sent at ``Scissor``. [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/crawler)

<a name="scissor"></a>
### Scissor
> Cut the imagens from ``Crawler`` to after send a set to ImageNet. [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/scissor)

<a name="extractor"></a>
### Extractor
> Unpack ``imagenet`` folders and images after be used to ``Keras`` in ``Anima``. [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/extractor)

<a name="transfer"></a>
### Transfer
> Set imagens cuted by ``Scissor`` to a new repository (Opcional). [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/transfer)

<a name="read_osm"></a>
### Read OSM
> Allow to read file ``Open Street Map`` file to feed the ``Swarm`` application. [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/read_osm)

<a name="eraser"></a>
### Eraser
> Allow to remove all information executed on ``Helpers``, ``Anima`` e ``Webserver`` to start again. [See more](https://github.com/glaucomunsberg/graphium/tree/master/helpers/eraser)

<a name="anima"></a>
## The Anima
Anima it's the brain of action, the nemesis.py file, for exemple, train the ImageNet to understand the images collected by extractor script file.

<a name="sun"></a>
### Sun
Sun has design to you show your imagens to imagenet and after these action see the set of classes actived. [See more](https://github.com/glaucomunsberg/graphium/blob/master/anima/)

<a name="anima"></a>
### Nemesis
Nemesis has build to finetune the images on ImageNet to understande these new classe to be searched after on Google Maps for example. [See more](https://github.com/glaucomunsberg/graphium/blob/master/anima/)
 
<a name="swarm"></a>
## Swarm
Swarm it's is the way that many agents surf under the web of streets (from google street view images) of each city searching the elements learned on Anima. [See more](https://github.com/glaucomunsberg/graphium/tree/master/swarm)

<a name="webserver"></a>
## Webserver
Allow to access by website each image extracted on google maps has a layout of information. [See more](https://github.com/glaucomunsberg/graphium/tree/master/webserver)

[^1]: Choose your label in Flickr do download and try you owner classe of images to be found in street view.
[^2]: Multi Agent Systems
[^3]: Maybe you need adapt to your OS :warning:
[^4]: Use the services script to transform the output of Sun to csv file to generate charts 