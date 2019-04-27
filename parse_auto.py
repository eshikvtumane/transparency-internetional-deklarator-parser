# -*- encoding: utf-8 -*-
import re

from bs4 import BeautifulSoup as BS
import urllib2

if __name__ == '__main__':
    with open('auto.html', 'rb') as f:
        content = f.read()
    # soup = BS(urllib2.urlopen("./auto.html").read())
    soup = BS(content, features="html")
    scriptTags = soup.find(id='marki').find_all('option')
    for script in scriptTags[1:]:
        result = re.search(r'[A-Za-zА-Яа-я]+', script.text)
        if result:
            result = result.group()
        print("'%s'," % (script.text))
    # contents = [str(x.text) for x in soup.find(id='marki').find_all('option')]
    # print(contents)
