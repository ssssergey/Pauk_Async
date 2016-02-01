#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime, date
import asyncio
import aiohttp
import shutil
import glob
import tkinter as tk
from tkinter.filedialog import *
import socket
import re
import os

import rss_downloader
import bs4_processing
from output import output
from config import logger, expire_date, version, icon_file, country_filter, output_folder, logger_history, rss_dict
from api_interaction import Api_inter


socket.setdefaulttimeout(10.0)

def get_rss_data():
    rss_downloader.url_selected = []
    rss_title_list = [rss_title for rss_title in rss_dict.values()]
    for rss_url in rss_dict:
        left_list = '\n'.join([str(len(rss_title_list)-i) + ". " + item for i,item in enumerate(rss_title_list)][:12])
        left_list = '|--ОСТАЛОСЬ СКАЧАТЬ RSS--|\n' + left_list
        app.label_status.configure(text=left_list, bg='#69969C')
        app.label_status.update()
        rssdownloader = rss_downloader.RssDownloader(rss_url)
        if rssdownloader.start():
            rss_title_list.remove(rss_dict[rss_url])
    return rss_title_list

#-------------------Async-------------------------#

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
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                aw = asyncio.wait([self.download_HTMLs_to_HTMLlist(item[0],item[1],item[2],item[3],item[4])
                                   for item in self.data_current])
                loop.run_until_complete(aw)
        return self.final_list_of_articles      # body,title,rss,func,link,atime

    @asyncio.coroutine
    def download_HTMLs_to_HTMLlist(self,link,title,rss,func,atime):
        print('Start downloading {}'.format(link))
        logger.info('Start downloading {}'.format(link))
        response = yield from asyncio.wait_for(aiohttp.request('GET', link), 20)  # With timeout
        body = yield from response.read()
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
        app.label_status.update()

def bs4_and_output(art_list_downloaded):
    count_left_art = len(art_list_downloaded)
    count_recieved = 0
    for html_item in art_list_downloaded:        # consist of body,title,rss,func,link,atime
        body,title_a,rss_a,func,link,dtformat = html_item
        count_left_art -= 1
        app.label_status.configure(text='Осталось обработать: {}'.format(count_left_art), bg='#69969C')
        app.label_status.update()
        NA_obj = bs4_processing.NEWSAGENCY(body)
        try:
            getattr(NA_obj,func)()
        except Exception as e:
            logger.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(link, e))
            logger_history.warning(link)
            continue
        NA_obj.strip_texts()
        maintext_a = NA_obj.main_text_class
        maintext_a = maintext_a + "\n" + link
        date_a,time_a = get_str_date_time(dtformat)
        country = define_country_by_zagolovok(title_a)
        if country == "Другие":
            country = define_country_by_mtext(maintext_a)
        if output(title_a, maintext_a, dtformat, date_a, time_a, rss_a, country,link):
            count_recieved += 1
            logger_history.warning(link)
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
    app.label_status.configure(text='Начал скачивать RSS.\nОЖИДАЙТЕ...', bg='#69969C')
    app.giffile = "spider_move2.gif"
    root.update()
    start = datetime.now()                              # START TIME
    undownloaded_rss = get_rss_data()
    total_count = len(rss_downloader.url_selected)
    app.label_status.configure(text='Начал скачивать СТАТЬИ.\nОЖИДАЙТЕ...')
    root.update()
    async_instance = Async(rss_downloader.url_selected)
    art_list_downloaded = async_instance.start_async()           # body,title,rss,func,link,atime
    downloaded_count = len(async_instance.final_list_of_articles)
    app.label_status.configure(text='Начал обработку СТАТЕЙ.\nОЖИДАЙТЕ...')
    app.label_status.update()
    recieved_count = bs4_and_output(art_list_downloaded)
    print('Total: {}'.format(total_count))
    logger.info('Total: {}'.format(total_count))
    print('Downloaded: {}'.format(downloaded_count))
    logger.info('Downloaded: {}'.format(downloaded_count))
    bad_url = ""
    if async_instance.data_changable:
        for u in async_instance.data_changable:
            bad_url += '\n' + u[0]
        logger.warning('Не скачаны следующие статьи:{}'.format(bad_url))

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
        summary_text += '\nЗатрачено времени: {}'.format(delta)
        color = '#c1ffac'
    elif len(undownloaded_rss) > 20:
        summary_text = 'ПРОВЕРЬТЕ ИНТЕРНЕТ СОЕДИНЕНИЕ!!!'
        color = '#9c699c'
    else:
        summary_text = 'Статей, представляющих интерес, не отмечено.'
        color = '#e3ebe0'
    if undownloaded_rss and recieved_count:
        failed_rss = '\n'.join(undownloaded_rss)
        summary_text += '\nНе получены новости от: \n{}'.format(failed_rss)
    app.label_status.configure(text=summary_text, bg=color, justify=LEFT)
    app.label_status.update()
    app.giffile = "spider_move.gif"

from threading import Thread
import time

def main_threading():
    try:
        api = Api_inter()
        api.start_main()
    except Exception as e:
        app.label_status.configure(text=str(e))
        app.label_status.update()
    Thread(target=main).start()

class GUI():
    def __init__(self, root):
        root.title("ПАУК " + version)
        root.iconbitmap(icon_file)
        # All Frames
        frame1 = tk.Frame(root, bg='#69969C')
        frame1.pack(fill=X)
        frame2 = tk.Frame(root, bg='#69969C')
        frame2.pack(fill=X)
        self.button_start = tk.Button(frame1, text="ПУСК", width=15, font=("Arial 15 bold"), bg='#012E34', fg='white',
                                      command=main_threading)
        self.button_start.pack(pady=5)
        self.giffile = "spider_move.gif"
        gif = tk.PhotoImage(file = self.giffile, format="gif -index 1")
        self.Artwork = Label(frame1, height=200, width=300, image=gif)
        self.Artwork.photo = gif
        self.Artwork.pack(padx=1)
        self.label_status = tk.Label(frame2, text="Нажмите ПУСК", justify=LEFT, font=("Arial 12"), bg='#69969C')
        self.label_status.pack(fill=X)
        separator1 = tk.Frame(root, height=5, bg='#0E464E', bd=3)
        separator1.pack(fill=X)
        self.label_author = tk.Label(root, text='Версия: {} - 2016 г.\nРазработчик: Ли С.Е.'.format(version), bg='#69969C')
        self.label_author.pack(fill=X, side=BOTTOM)

        self.num = 0

        Thread(target=self.animate).start()

    def animate(self):
        while True:
            try:
                time.sleep(0.1)
                gif = PhotoImage(file=self.giffile, format="gif -index {}".format(self.num))

                self.Artwork.config(image=gif)
                self.Artwork.photo=gif

                self.num += 1
            except:
                self.num = 0

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('+1+10')
    root.configure(background='#69969C')
    app = GUI(root)
    root.mainloop()
