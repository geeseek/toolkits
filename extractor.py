#!/usr/bin/python
from bs4 import BeautifulSoup
from urllib2 import urlopen,HTTPError,URLError
import sys 
import time
import re
import string

class Template:
    pattern = ''
    xpath = {} 

    def __init__(self):
        self.pattern = ''
        self.xpath = {}

    def debug(self):
        print "pattern: ", self.pattern
        for key in self.xpath.keys():
            print "[", key, "]: ", self.xpath[key]

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

def getTextOfNode(node):
    result = ''
    for text in node.stripped_strings:
            result = result + " " + text.encode('utf-8')
    return result

def getChildWithAttrsAndSeq(node, node_name, attr_name, attr_value, node_seq):
    #do not search the children of root node
    isRecursive = True

    if node.name == 'document':
        isRecursive = False

    search_node = None
    
    if attr_name != 'prefix': #normal attributes
        search_node = node.find_all(node_name, attrs={attr_name:attr_value}, recursive=isRecursive)[node_seq]
    else:  #special attribute: prefix 
        node_list = node.find_all(node_name, recursive=isRecursive) 
        for curNode in node_list:
            text = getTextOfNode(curNode).strip()
            if attr_value == text[0:len(attr_value)]:
                search_node = curNode
                break
    return search_node 
    

def getNodeByPath(node, path):
    #print "path: ", path
    curNode = node
    dirs = path.split('/')
    for dir in dirs:
        node_seq = 0
        m = re.match(r'([\w]+)(\'(.+)@(.+)\')?(\[([0-9]+)\])?', dir)
        if m != None:
            node_name = m.group(1)
            if m.group(2) != None and m.group(5) != None:
                attr_name = m.group(3)
                attr_value = m.group(4) 
                node_seq = string.atoi(m.group(6)) - 1
                curNode = getChildWithAttrsAndSeq(curNode, node_name, attr_name, attr_value, node_seq)
            elif m.group(2) == None and m.group(5) != None:
                node_seq = string.atoi(m.group(6)) - 1
                curNode = curNode.find_all(node_name, recursive=False)[node_seq]
            elif m.group(2) != None and m.group(5) == None:
                attr_name = m.group(3)
                attr_value = m.group(4) 
                curNode = getChildWithAttrsAndSeq(curNode, node_name, attr_name, attr_value, node_seq)
            else:
                curNode = curNode.find(node_name)
    return curNode;

def extract(page, template):
    soup = BeautifulSoup(page, 'html.parser',from_encoding="utf-8")
    node_dict = {}
    for name in sorted(template.xpath.keys()):
        parent_node = soup
        pos = name.find('#') 
        if pos >= 0:
            parent_node_name = name.split('#')[0]
            if len(parent_node_name) > 0:
                parent_node = node_dict[parent_node_name]
        node_dict[name] = getNodeByPath(parent_node, template.xpath[name])
        text = ''
        if node_dict[name] != None:
            text = getTextOfNode(node_dict[name])
        if pos >= 0:
            print  text.replace('\n',''),'\t',
            #print  name,'\t', text.replace('\n',''),'\t'


def loadTemplate(file):
    fileHandler = open(file, 'r')
    template_dict = {} 
    for line in fileHandler.readlines():
        parts = line.split(':', 1) 
        if len(parts) >= 2:
            if parts[0] == 'pattern':
                pattern = parts[1].strip()
                template = Template()
                template_dict[pattern] = template
                template_dict[pattern].pattern = pattern
            else:
                m = re.match(r'\[([\w#]+)\]', parts[0]) 
                if m != None:
                    field_name = m.group(1)
                    field_xpath = parts[1].strip() 
                    template_dict[pattern].xpath[field_name] = field_xpath
    return template_dict


if __name__=="__main__":
    template_dict = loadTemplate('./template.conf') 
    file = open(sys.argv[1], 'r')
    for line in file.readlines():
        #get template for this page 
        template = Template()
        for pattern in template_dict.keys():
            m = re.match(pattern, line) 
            if m != None:
                template = template_dict[pattern]
                break;

        #crawl this page
        page = crawl(line)
        print line.strip(),'\t',

        #extract
        if (len(page) > 100):
            extract(page, template)

        print ''

