import threading
import logging
import urllib
from urllib import request
import os
import sys
import json
import time
import random
from Img import Image


def init_logger(writeFile):
    if writeFile is True:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', filename='log',
                filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S')


def get_page(url):
    page = None
    i = 1
    while(True):
        try:
            req = request.Request(url)
            with request.urlopen(req) as response:
                page = response.read()
                break

        except urllib.error.HTTPError as e:
            if i >= 3:
                logging.warning('retry more than 3 times, give up')
                break
            logging.error('%s\n retrying...' % e)
            i += 1

    return page.decode('utf-8', 'ignore')


def save(img_url, path):
    #logging.info('start thread %s' % threading)
        if os.path.exists(path):
            logging.info('file already exist, pass ....')
            return
        request.urlretrieve(img_url, path, reporthook=callbackfunc)


def callbackfunc(block_num, block_size, total_size):
    width = 20
    percent = 100.0 * block_num * block_size / total_size
    if percent >= 100:
        sys.stdout.write("[%s] %d%%" % (('%%-%ds' % width) % (width * '='), 100))
    else:
        sys.stdout.write("[%s] %d%%\r" % (('%%-%ds' % width) % (int(width * percent / 100) * '='), percent))


def down(json_url, page=1, tags=''):
    time.sleep(random.randint(2,4))
    if tags == None:
        tags = ''
    param = urllib.parse.urlencode({'page': page, 'tags': tags})
    json_page = get_page('%s?%s' % (json_url, param))

    if json_page is '[]':
        return None

    for img in json.loads(json_page):
        a_img = Image(tags,
        img['id'],
        img['tags'],
        img['sample_url'],
        img['sample_width'],
        img['sample_height'],
        img['jpeg_url'],
        img['jpeg_width'],
        img['jpeg_height'])

        th = threading.Thread(target=save
                                  , args=(a_img.get_img_url(), a_img.get_local_path())
                                  , name='DownloadImg_Thread: %s' % a_img.img_id)
        th.start()
        #th.join()
    return 1


def start(page, tag):
    logging.info('start with page %s, tag %s' % ('(ALL)' if page is 0 else page, tag))

    if page == 0:
        logging.info('now will get ALL pages of this TAG')
        i = 0
        for i in range(1, 20000):
            logging.info('page %s %s' % (i, tag))
            status = down('https://yande.re/post.json?', page=i, tags=tag)
            if status == None:
                break

    else:
        down('https://yande.re/post.json?', page=page, tags = tag)



if __name__ == '__main__':
    #init_logger(False)
    logging.info('Logger init...')
    if len(sys.argv) == 1:
        logging.warning('no param getted, use the default one')
        mypage = 1
        mytag = ''
    elif len(sys.argv) > 1 and len(sys.argv) < 4:
        mypage = sys.argv[1]
        mytag = sys.argv[2]
    else:
        raise Exception('missing or too much params')

    start(int(mypage), mytag)



