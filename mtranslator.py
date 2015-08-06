#!/usr/bin/python
from bs4 import BeautifulSoup
import sys

if __name__=="__main__":
    file = open(sys.argv[1], 'r')
    for line in file.readlines():
        soup = BeautifulSoup(line, 'html.parser',from_encoding="utf-8")
        body = soup.find('div',attrs={'class':'word'})
        word_name = body.find('div', attrs={'class':'word_name'})
        block_list = body.findAll('div', attrs={'class':'block'})
        for block in block_list:
            print word_name.string,'\t',
            dict_name = block.find('div',attrs={'class':'dict'})
            print dict_name.string.encode('utf-8'), '\t',
            dict_content = block.find('div',attrs={'class':'content'})
            trans_word = "";
            for text in dict_content.stripped_strings:
                trans_word = trans_word + text.encode('utf-8')
            print(trans_word)

        
