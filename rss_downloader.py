
import feedparser
import socket
import re
import os
from datetime import datetime, date, timedelta

from config import logger, logger_history, logger_bucket, rss_dict, rss_func_dict, keyword_file, history_file, stop_words, os_current


socket.setdefaulttimeout(6.0)

url_selected = []

class RssDownloader:
	def __init__(self, url):
		self.url = url
		self.rss_title = rss_dict[url]
		self.entry_time = None
	def start(self):
		global url_selected
		print ("Starting: ", self.rss_title)
		count = 0
		logger.info("Starting: {}".format(self.rss_title))
		rss_data = feedparser.parse(self.url)
		if len(rss_data['entries']):
			logger.info("{}: TOTAL - {}".format(self.rss_title,len(rss_data['entries'])))
			for entry in rss_data.get('entries'):
				try:
					self.time_handler(entry.published_parsed)
				except Exception:
					logger.warning("{}: FAILED TimeHandler!!!".format(entry.link))
					print("{}: FAILED TimeHandler!!!".format(entry.link))
					continue
				if self.add_to_selected_or_not(entry):
					print(entry.title)
					print(entry.link)
					# print (entry.published_parsed)
					url_selected.append((entry.link,                        # link
										entry.title,                        # title of article
										self.rss_title,                     # IA title
										rss_func_dict[self.rss_title],      # func name
										self.entry_time                       # time
										 ))
					count += 1
			print ("Exiting: ", self.rss_title)
			logger.info("{}: Selected - {}".format(self.rss_title, count))
			return True
		else:
			logger.info("{}: FAILED!!!".format(self.rss_title))
			return False

	def add_to_selected_or_not(self, rss_item):
		rss_item.link = rss_item.link.replace('http://az.apa','http://ru.apa')
		if is_in_history(rss_item.link) == True:
			return False
		if os_current == 'Windows':
			if not self.time_filter():
				return False
		keywords_text = keywords_extract()
		for word in keywords_text:  # перебираем ключевые слова
			p = re.compile(word)
			if p.search(rss_item.title.lower()) or p.search(rss_item.title):
				for word1 in stop_words:
					p1 = re.compile(word1)
					if p1.search(rss_item.title.lower()) or p1.search(rss_item.title):
						logger_bucket.warning(rss_item.title)
						logger_history.warning(rss_item.link)
						return False
				return True
		return False

	def time_handler(self, entry_time):
		old_time = entry_time
		new_time = datetime(old_time.tm_year, old_time.tm_mon, old_time.tm_mday, old_time.tm_hour,old_time.tm_min,
							old_time.tm_sec)
		if self.rss_title == 'ИРНА':
			new_time = new_time - timedelta(hours=0.5)
		elif self.rss_title == 'Спутник':
			new_time = new_time + timedelta(hours=2)
		else:
			new_time = new_time + timedelta(hours=3)
		self.entry_time = new_time

	def time_filter(self):
		if self.entry_time.day == date.today().day:
			return True
		else:
			return False


def keywords_extract():
	with open(keyword_file,'r',encoding='utf-8-sig') as f:
		lines = f.readlines()
		lines = [l.strip() for l in lines[1:]]
	return lines

def is_in_history(link):
	if not os.path.isfile(history_file): create_history_file() # если файла нет, добавляем его и вписываем лимит-счетчик
	with open(history_file, 'r', encoding='utf-8-sig') as history_txt: # открываем файл с уникальными url
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
	with open(history_file, 'w+', encoding='utf-8-sig') as history_txt:
		history_txt.write('0b1100100\n')