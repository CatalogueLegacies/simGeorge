#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from os import path
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()

headers = \
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

for pageno in range(1, 192, 1):
    print 'Loading page ' + str(pageno) + ' of 191...'
    page_url = \
        'https://www.britishmuseum.org/collection/search?object=satirical%20print&school_style=British&dateFrom=1770&eraFrom=ad&dateTo=1830&eraTo=ad&page=' \
        + str(pageno)
    print 'Retrieving ' + page_url
    browser.get(page_url)
    sleep(1)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)'
                           )
    page = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(page, 'html.parser')
    result_array = soup.find_all('a', {'class': 'teaser__link'})

    for result in result_array:

        try:
            photo_test = result.findAll('img', {'class': 'teaser__image'
                    })[0]
            permalink_url = result['href']
            print 'Permalink is ' + permalink_url
            unique_id = permalink_url.split('/')[-1]
            print 'Unique ID is ' + unique_id
            photo_link = result.findAll('img', {'class': 'teaser__image'
                    })[0]
            if not path.exists('britishmuseum/' + unique_id + '.jpg'):
                savedphoto = open('britishmuseum/' + unique_id + '.jpg'
                                  , 'wb')
                pic_to_dl = photo_link['data-src'].replace('https',
                        'http')
                print 'Trying to retrieve ' + pic_to_dl
                savedphoto.write(requests.get(pic_to_dl).content)
                savedphoto.close()
                print 'Downloaded and saved ' + unique_id
            else:
                print unique_id + ' already downloaded.'
        except:
            print 'No image available; skipping'
            continue
