#!/usr/bin/python
from bs4 import BeautifulSoup
import sys
from urllib2 import urlopen,HTTPError
import time


def crawl(url):
    time.sleep(2)
    line = ""
    try:
        line = urlopen(url).read()
    except HTTPError, e:
        pass
    return line


def extract(info, html):
    soup = BeautifulSoup(html, 'html.parser',from_encoding="utf-8")
    body = soup.find('div',attrs={'class':'word'})
    word_name = body.find('div', attrs={'class':'word_name'})
    block_list = body.findAll('div', attrs={'class':'block'})
    for block in block_list:
        dict_name = block.find('div',attrs={'class':'dict'})
        dict_content = block.find('div',attrs={'class':'content'})
        trans_word = "";
        for text in dict_content.stripped_strings:
            trans_word = trans_word + text.encode('utf-8')
        print info, '\t', dict_name.string.encode('utf-8'), '\t', trans_word 


if __name__=="__main__":
    file = open(sys.argv[1], 'r')
    for line in file.readlines():
        line = line.replace('"', '')
        line = line.replace('\n', '')
        parts = line.split(',')
        if len(parts) < 2:
            continue
        id = parts[0]
        word = parts[1]
        word = word.replace('\'', '')
        word = word.replace(' ', '-')
        word = word.lower()
        url = "http://www.mcd8.com/w/" + word 
        info = id + '\t' + parts[1] + '\t' + url
        html = crawl(url)
        if len(html) < 1:
            continue 
        extract(info, html)
