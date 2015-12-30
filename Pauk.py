#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: Сделать поэтапную фильтрацию как в основном пауке
# todo: Сделать удобное тестирование отдельных модулей

from datetime import datetime, date
import asyncio
import aiohttp
import shutil
import glob
import tkinter as tk
from tkinter.filedialog import *
import socket

import rss_threading
import bs4_processing
from output import output
from config import logger, expire_date, version, icon_file, country_filter, output_folder, logger_history

socket.setdefaulttimeout(30.0)

def get_rss_data():
    rss_threading.url_selected = []
    pf = rss_threading.PullFeeds()
    pf.pullfeed()

class Async():
    def __init__(self, url_selected):
        self.data_current = url_selected[:]
        self.data_changable = url_selected[:]
        self.final_list_of_articles = []

    def start_async(self):
        for i in range(3):
            print("ROUND {}".format(i))
            if self.data_changable:
                self.data_current = self.data_changable[:]
                loop = asyncio.get_event_loop()
                aw = asyncio.wait([self.download_HTMLs_to_HTMLlist(item[0],item[1],item[2],item[3],item[4])
                                   for item in self.data_current])
                loop.run_until_complete(aw)
        return self.final_list_of_articles      # body,title,rss,func,link,atime

    @asyncio.coroutine
    def download_HTMLs_to_HTMLlist(self,link,title,rss,func,atime):
        print('Start downloading {}'.format(link))
        logger.info('Start downloading {}'.format(link))
        response = yield from asyncio.wait_for(aiohttp.request('GET', link), 30)  # With timeout
        body = yield from response.read_and_close()
        try:
            if rss in ['News-Asia', 'МигНьюс', 'Коммерсант', 'Грузия-онлайн', 'ЦАМТО']:
                body = body.decode(encoding='cp1251')
            else:
                body = body.decode(encoding='utf-8')
        except Exception as e:
            logger.warning('Кодировка: {}'.format(e))
        self.final_list_of_articles.append([body,title,rss,func,link,atime])
        try:
            self.data_changable.remove((link,title,rss,func,atime))
        except:
            pass
        print('Finished {}'.format(link))
        logger.info('Finished {}'.format(link))
        app.label_status.configure(text='Осталось скачать статей: {}'.format(len(self.data_changable)), bg='#69969C')
        root.update()


def bs4_and_output(art_list_downloaded):
    count_left_art = len(art_list_downloaded)
    count_recieved = 0
    for html_item in art_list_downloaded:        # consist of body,title,rss,func,link,atime
        body,title_a,rss_a,func,link,dtformat = html_item
        count_left_art -= 1
        app.label_status.configure(text='Осталось обработать: {}'.format(count_left_art), bg='#69969C')
        root.update()
        NA_obj = bs4_processing.NEWSAGENCY(body)
        func_result = getattr(NA_obj,func)()
        if func_result == False:
            add_url_to_history(link)
            continue
        else:
            NA_obj.strip_texts()
            maintext_a = NA_obj.main_text_class
            maintext_a = maintext_a + "\n" + link
            date_a,time_a = get_str_date_time(dtformat)
            country = define_country_by_zagolovok(title_a)
            if country == "Другие":
                country = define_country_by_mtext(maintext_a)
            if output(title_a, maintext_a, dtformat, date_a, time_a, rss_a, country):
                count_recieved += 1
                add_url_to_history(link)
    return count_recieved

def define_country_by_zagolovok(title_a):
    country = "Другие"
    for k in country_filter.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(title_a) or p.search(title_a.lower()):
                country = k[1]
                return country
    return country

def define_country_by_mtext(mtext_a):
    country = "Другие"
    for k in country_filter.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(mtext_a[:350]) or p.search(mtext_a[:350].lower()):  # Поиск производится примерно в первых двух абзацах (350 знаков) осн текста
                country = k[1]
                return country
    return country

def get_str_date_time(datetime_format):
    month_names = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября',
                   'декабря']
    month_name = month_names[datetime_format.month - 1]
    date_final = '{} {} {} г.'.format(str(datetime_format.day).lstrip("0"),month_name,str(datetime_format.year))
    time_final = datetime_format.strftime("%H.%M")
    return date_final, time_final

def add_url_to_history(link):
    logger_history.warning(link)
    # with open(history_file, 'a') as history_txt:
    #     history_txt.write(url + ' ' + str(datetime.now()) + '\n')

def check_license():
    if date.today() > expire_date:
        return False
    return True

def otsechka():
    second_path = output_folder + "от_Паука_на_" + str(datetime.now().strftime("%H.%M %d.%m.%Y")) + "\\"
    os.makedirs(second_path)
    try:
        for filename in glob.glob(os.path.join(output_folder, '*.doc')):
            shutil.move(filename, second_path)
        for filename in glob.glob(os.path.join(output_folder, '*.txt')):
            shutil.move(filename, second_path)
    except PermissionError as e:
        pass
    app.label_status.configure(text="Нажмите ПУСК", bg='#69969C')

def main():
    if check_license() == False:                        # Check license
        app.label_status.configure(text="Обновите программу!\nwww.pauk-press.ru", bg='red')
        return
    start = datetime.now()                              # START TIME
    app.label_status.configure(text='Начал скачивать RSS.\nОЖИДАЙТЕ...', bg='#69969C')
    root.update()
    get_rss_data()
    url_selected = rss_threading.url_selected         # link,title,rss,func,atime
    total_count = len(url_selected)
    app.label_status.configure(text='Начал скачивать СТАТЬИ.\nОЖИДАЙТЕ...')
    root.update()
    async_instance = Async(url_selected)
    art_list_downloaded = async_instance.start_async()           # body,title,rss,func,atime
    downloaded_count = len(async_instance.final_list_of_articles)
    app.label_status.configure(text='Начал обработку СТАТЕЙ.\nОЖИДАЙТЕ...')
    root.update()
    recieved_count = bs4_and_output(art_list_downloaded)
    print('Total: {}'.format(total_count))
    logger.info('Total: {}'.format(total_count))
    print('Downloaded: {}'.format(downloaded_count))
    logger.info('Downloaded: {}'.format(downloaded_count))
    bad_url = ""
    for u in async_instance.data_changable:
        bad_url += '\n' + u[0]
    logger.info('Не скачаны следующие статьи:{}'.format(bad_url))
    end = datetime.now()                                # STOP TIME
    delta = end - start
    delta = '{} сек.'.format(delta.seconds)
    logger.info('Timing: {}'.format(delta))

    if recieved_count:
        otsechka()
        summary_text = 'Готово! Забирайте папку!\nc:\\от Паука\\'
        summary_text += '\nОтобрано: {}'.format(total_count)
        summary_text += '\nCкачано: {}'.format(downloaded_count)
        summary_text += '\nИспользовано: {}'.format(recieved_count)
        color = 'yellow'
    elif len(rss_threading.rss_current_rest) > 20:
        summary_text = 'ПРОВЕРЬТЕ ИНТЕРНЕТ СОЕДИНЕНИЕ!!!'
        color = 'red'
    else:
        summary_text = 'Статей, представляющих интерес, не отмечено.'
        color = 'gray'
    summary_text += '\nЗатрачено времени: {}'.format(delta)
    if rss_threading.rss_current_rest and recieved_count:
        failed_rss = '\n'.join(rss_threading.rss_current_rest)
        summary_text += '\nНе получены новости от: \n{}'.format(failed_rss)
    app.label_status.configure(text=summary_text, bg=color, justify=LEFT)
    root.update()

class GUI():
    def __init__(self, root):
        root.title("ПАУК " + version)
        root.iconbitmap(icon_file)
        # All Frames
        self.button_start = tk.Button(root, text="ПУСК", font=("Arial 15 bold"), bg='#012E34', fg='white',
                                      command=main)
        self.button_start.pack(fill=X)
        self.label_status = tk.Label(root, text="Нажмите ПУСК", font=("Arial 12"), bg='#69969C')
        self.label_status.pack(fill=X)
        separator1 = tk.Frame(root, height=5, bg='#0E464E', bd=3)
        separator1.pack(fill=X)
        self.label_author = tk.Label(root, text='Версия: {} - 2015 г.\nРазработчик: Ли С.Е.'.format(version), bg='#69969C')
        self.label_author.pack(fill=X)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
