#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

class Api_inter():
    def __init__(self):
        self.hashed_uid = None
        self.payload = None
        self.link = 'https://paukapi-1207.appspot.com'
        # self.link = 'http://localhost:14081'
        if not os.path.isfile('uid'):
            self.create_file()

    def create_file(self):
        r = urllib.request.urlopen(self.link+'/newuid')
        self.hashed_uid = r.headers['uid']
        with open('uid', 'w', encoding='utf-8-sig') as uidfile:
            uidfile.write(self.hashed_uid)

    def uid_from_file(self):
        with open('uid', 'r', encoding='utf-8-sig') as uidfile:
            self.hashed_uid = uidfile.readline().strip()
            if len(self.hashed_uid) < 3:
                self.create_file()

    def start_main(self):
        req  = urllib.request.Request('http://www.hostip.info/', headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req)
        r = r.read()
        soup = BeautifulSoup(r, "html.parser")
        info = soup.find('div',{'class':'info'}).find('p')
        items = [a.get_text() for a in info.find_all('b')]
        items = items[1:3]
        self.uid_from_file()
        self.payload = {'ip':items[0],
                   'location':items[1],
                   'hashed_uid':self.hashed_uid
                   }
        data = urllib.parse.urlencode(self.payload)
        print(data)
        binary_data = data.encode("utf8")
        req = urllib.request.Request(self.link, binary_data)
        r = urllib.request.urlopen(req)
        print(r)

if __name__ == '__main__':
    api = Api_inter()
    api.start_main()