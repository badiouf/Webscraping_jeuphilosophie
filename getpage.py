#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as soup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
import ssl
from functools import lru_cache
from urllib.parse import unquote
from collections import OrderedDict


def getJSON(page):
    params = urlencode({
      'format': 'json', 
      'action': 'parse',
      'prop': 'text', 
      'redirects': 'true',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php" 
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  
        content =parsed['parse']["text"]["*"] 
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None

@lru_cache(maxsize=None)
def getPage(page):
    if getRawPage(page)==(None,None):
        return None, []
    else:
        title=getRawPage(page)[0]
        tags= soup(getRawPage(page)[1], "html.parser").find("div", attrs={"class": "mw-parser-output"})
        liste_href=[]
        for p in tags.find_all('p',recursive=False): 
            if len(p.find_all('a')) > 0:
                
                for a in p.find_all('a'):
                    href=a['href']
                    href=unquote(href).replace("_"," ")
                    if href.find(":")!=-1:
                        pass
                    else:
                        if href[1:5]=='wiki':
                            href=href[6:]
                            c="#"
                            hashtag=[pos for pos,char in enumerate(href) if char==c]
                            if len(hashtag)>0:
                                if href[0]=="#":
                                    pass
                                else :
                                    href=href[:hashtag[0]]
                                    liste_href.append(href)
                            else:
                                liste_href.append(href)
                        else:
                            pass
            else:
                pass
          
        return title,list(OrderedDict.fromkeys(liste_href))[:10]


if __name__ == '__main__':
    print("Ça fonctionne!")
