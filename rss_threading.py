#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import feedparser
import socket
import re
import os
from datetime import datetime, date, timedelta

from config import logger, rss_dict, rss_func_dict, keyword_file, history_file, bucket_file, stop_words

socket.setdefaulttimeout(8.0)
url_selected = []
rss_current_rest = []


class PullFeeds:
    def __init__(self):
        self.rss_urls_list = [rss_url for rss_url in rss_dict.keys()]
    def pullfeed(self):
        global rss_current_rest
        rss_current_rest = []
        threads = []
        for i in range(2):
            for url in self.rss_urls_list:
                 t = RssParser(url)
                 threads.append(t)
            for thread in threads:
                 thread.start()
            for thread in threads:
                 thread.join()
            if not rss_current_rest:
                break
            self.rss_urls_list = rss_current_rest
            if i == 0:
                rss_current_rest = []
            threads = []
            logger.info('!!!RSS second ROUND!!!')
        if rss_current_rest:
            msg = "FAILED RSS:\n"
            for r in rss_current_rest:
                msg += rss_dict[r] + '\n'
            logger.info(msg)

class RssParser(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.rss_title = rss_dict[url]
        self.entry_time = None
    def run(self):
        global url_selected
        global rss_current_rest
        print ("Starting: ", self.name, self.rss_title)
        rss_current_rest.append(self.url)
        count = 0
        logger.info("Starting: {} {}".format(self.name, self.rss_title))
        rss_data = feedparser.parse(self.url)
        if len(rss_data['entries']):
            logger.info("{}: TOTAL - {}".format(self.rss_title,len(rss_data['entries'])))
            for entry in rss_data.get('entries'):
                self.entry_time = None
                if self.add_to_selected_or_not(entry):
                    print(entry.title)
                    print(entry.link)
                    print (entry.published_parsed)
                    url_selected.append((entry.link,                        # link
                                        entry.title,                        # title of article
                                        self.rss_title,                     # IA title
                                        rss_func_dict[self.rss_title],      # func name
                                        self.entry_time                       # time
                                         ))
                    count += 1
            print ("Exiting: ", self.name, self.rss_title)
            rss_current_rest.remove(self.url)
            print ("Осталось: {}".format(len(rss_current_rest)))
            logger.info("{}: Selected - {}".format(self.rss_title, count))
        else:
            logger.info("{}: FAILED!!!".format(self.rss_title))

    def add_to_selected_or_not(self, rss_item):
        rss_item.link = rss_item.link.replace('http://az.apa','http://ru.apa')
        if is_in_history(rss_item.link) == True:
            return False
        for word in stop_words:
            p = re.compile(word)
            if p.search(rss_item.title.lower()) or p.search(rss_item.title):
                print(rss_item.title, file=open(bucket_file,'a',encoding='utf-8'))
                print("Stopword")
                return False
        if not self.time_filter(rss_item.published_parsed):
            print("Time")
            return False
        keywords_text = keywords_extract()
        for word in keywords_text:  # перебираем ключевые слова
            p = re.compile(word)
            if p.search(rss_item.title.lower()) or p.search(rss_item.title):
                return True
        print("No keyword")
        return False

    def time_filter(self, entry_time):
        old_time = entry_time
        new_time = datetime(old_time.tm_year, old_time.tm_mon, old_time.tm_mday, old_time.tm_hour,old_time.tm_min,
                            old_time.tm_sec)
        if self.rss_title == 'ИРНА':
            new_time = new_time - timedelta(hours=0.5)
        elif self.rss_title == 'Спутник':
            new_time = new_time + timedelta(hours=2)
        else:
            new_time = new_time + timedelta(hours=3)
        if new_time.day == date.today().day:
            self.entry_time = new_time
            return True
        else:
            return False

def keywords_extract():
    with open(keyword_file,'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    return lines

def is_in_history(link):
    if not os.path.isfile(history_file): create_history_file() # если файла нет, добавляем его и вписываем лимит-счетчик
    with open(history_file, 'r') as history_txt: # открываем файл с уникальными url
        history_txt.seek(0)                     # переводим курсор в начало файла
        history_list = history_txt.readlines()  # копируем оттуда весь текст
    if any(link in line for line in history_list):  #преверяем наличие текущей статьи в файле history.txt. Если есть то пропускаем.
        return True
    try:
        if 'http://www.blackseanews.net/read/' + link.split('/')[8] + '\n' in history_list: # отдельно проверяется для blackseanews, возможна ошибка в rss_item.link.split('/')[8]
            return True
    except IndexError:
        pass
    return False

def create_history_file():
    with open(history_file, 'w+') as history_txt:
        history_txt.write('0b1100100\n')

if __name__ == '__main__':
    pf = PullFeeds()
    pf.pullfeed()
    print(len(url_selected))