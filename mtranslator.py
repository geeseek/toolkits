#!/usr/bin/python
from bs4 import BeautifulSoup
import sys
from urllib2 import urlopen,HTTPError,URLError
import time


def crawl(url):
    time.sleep(1)
    line = ""
    try:
        line = urlopen(url).read()
    except HTTPError, e:
        pass
    except URLError, e:
        pass
    return line


def bing_extractor_wrapper(info, html):
    soup = BeautifulSoup(html, 'html.parser',from_encoding="utf-8")
    body = soup.find('span',attrs={'class':'def'})
    trans_word = "" 
    if body != None:
        for text in body.stripped_strings:
            trans_word = trans_word + text.encode('utf-8')
    print info, '\t', 'network', '\t', trans_word 

def mcd8_extractor_wrapper(info, html):
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


def mcd8_url_wrapper(word):
    word = parts[1]
    word = word.replace('\'', '')
    word = word.replace(' ', '-')
    word = word.lower()
    url = "http://www.mcd8.com/w/" + word 
    return url

def bing_url_wrapper(word):
    word = parts[1]
    word = word.replace('\'', '')
    word = word.replace(' ', '+')
    word = word.lower()
    url = "http://cn.bing.com/dict/search?q=" + word 
    return url

def split_record(line):
    line = line.replace('"', '')
    line = line.replace('\n', '')
    parts = line.split(',')
    return parts




if __name__=="__main__":
    if len(sys.argv) == 2:
        dict = "default"
        file_name = sys.argv[1]
    elif len(sys.argv) == 3:
        dict = sys.argv[1]
        file_name = sys.argv[2]
    else:
        print "Wrong command: python mtranslator.py [dict_name] file"
        
    url_dict = {"default":mcd8_url_wrapper, "bing":bing_url_wrapper} 
    extractor_dict = {"default":mcd8_extractor_wrapper, "bing":bing_extractor_wrapper} 
    file = open(file_name, 'r')
    for line in file.readlines():
        parts = split_record(line) 
        if len(parts) < 2:
            continue
        id = parts[0]
        url = url_dict[dict](parts[1]) 
        print url
        info = id + '\t' + parts[1] + '\t' + url
        html = crawl(url)
        if len(html) < 1:
            continue 
        extractor_dict[dict](info, html)
