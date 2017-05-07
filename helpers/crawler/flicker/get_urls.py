import flickr
import urllib, urlparse
import os
import sys
import time
import datetime
from timeit import default_timer as timer

if __name__ == "__main__":

    tag = 'graffiti'
    #1.500 imagens por hora
    #date = datetime.datetime(2013,8,1,0,0,0)
    date1 = datetime.datetime(1980,1,15,22,0,0)
    date2 = datetime.datetime(2107,1,15,23,0,0)
    # print date2
    #X Adicionar, nao parar com exceptions 
    hits = 0
    time1 = timer()
    while True:
        print 'date: '+str(date1),
        #Salvar data em arquivo
        file = open("last_date.txt", "w")
        file.write(str(date1))
        file.close()
        try:
            f = flickr.photos_search(tags=tag, min_taken_date=str(date1), max_taken_date=str(date2), per_page="500")
            hits += 1
        except:
            print 'Could not search'
            date1 += datetime.timedelta(hours=1)
            date2 += datetime.timedelta(hours=1)
            continue
        print ', len: '+str(len(f))
        urllist = []
        os.chdir('images/')
        for k in f:
            try:
                url = k.getURL(size='Large', urlType='source')
                hits += 1
            except:
                print 'Could not get url'
                continue
            urllist.append(url) 
            image = urllib.URLopener()
            if not(os.path.isfile(os.path.basename(urlparse.urlparse(url).path))):
                try:
                    image.retrieve(url, os.path.basename(urlparse.urlparse(url).path)) 
                    hits += 1
                except:
                    print 'Could not retrieve image'
                    continue
                print 'retrieved:', os.path.basename(urlparse.urlparse(url).path)
            else:
                print 'already exists:', os.path.basename(urlparse.urlparse(url).path)
        date1 += datetime.timedelta(hours=1)
        date2 += datetime.timedelta(hours=1)
        #Adicionar hits, depois de 3000, tem que esperar completar 1 hora. 
        if hits >= 3000:
            t = timer() - time1
            if t < 60*60:
                s = 60*60 - t
                print 'sleeping for '+str(s/60)+' minutes'
                time.sleep(s)
            else:
                print 'made 3000 hits in '+str(t/60)+' minutes'
            hits = 0
            time1 = timer()