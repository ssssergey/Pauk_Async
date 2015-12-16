#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Asus'
# TODO: Вынести фильтрацию по ключемым словам в файл Pauk
from datetime import datetime, date, timedelta
import asyncio
import aiohttp
import logging
import shutil
import glob
import tkinter as tk
from tkinter.filedialog import *
import socket

import rss_threading
import bs4_processing
import output


expire_date = date(2016,2,1) # Date of the program license expiration

logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='Debugging.txt')

socket.setdefaulttimeout(30.0)
def get_rss_data():
    # RSS threading
    rss_threading.url_selected = []
    pf = rss_threading.PullFeeds()
    pf.pullfeed()

def today_filter(url_selected):
    today_url_selected = []
    for i in url_selected:
        old_time = i[4]
        new_time = datetime(old_time.tm_year, old_time.tm_mon, old_time.tm_mday, old_time.tm_hour,old_time.tm_min,
                            old_time.tm_sec)
        if i[2] == 'ИРНА':
            new_time = new_time - timedelta(hours=0.5)
        elif i[2] == 'Спутник':
            new_time = new_time + timedelta(hours=2)
        else:
            new_time = new_time + timedelta(hours=3)
        if new_time.day == date.today().day:
            today_url_selected.append((i[0],i[1],i[2],i[3],new_time))
        else:
            output.add_url_to_history(i[0])
    print("Было: {}, Стало: {}".format(len(url_selected), len(today_url_selected)))
    return today_url_selected

class Async():
    def __init__(self, url_selected):
        self.data_current = url_selected[:]
        self.data_changable = url_selected[:]
        self.final_list_of_articles = []

    @asyncio.coroutine
    def download_HTMLs_to_HTMLlist(self,url,title,rss,func,atime):
        print('Start downloading {}'.format(url))
        logging.info('Start downloading {}'.format(url))
        response = yield from asyncio.wait_for(aiohttp.request('GET', url),30)  # With timeout
        body = yield from response.read_and_close()
        try:
            if rss in ['News-Asia', 'МигНьюс', 'Коммерсант', 'Грузия-онлайн', 'ЦАМТО']:
                body = body.decode(encoding='cp1251')
            else:
                body = body.decode(encoding='utf-8')
        except Exception as e:
            logging.info('Кодировка: {}'.format(e))
        self.final_list_of_articles.append([body,title,rss,func,url,atime])
        try:
            self.data_changable.remove((url,title,rss,func,atime))
        except:
            pass
        print('Finished {}'.format(url))
        logging.info('Finished {}'.format(url))
        app.label_status.configure(text='Осталось скачать статей: {}'.format(len(self.data_changable)), bg='#69969C')
        root.update()

    def start_async(self):
        for i in range(3):
            print("ROUND {}".format(i))
            if self.data_changable:
                self.data_current = self.data_changable[:]
                loop = asyncio.get_event_loop()
                aw = asyncio.wait([self.download_HTMLs_to_HTMLlist(item[0],item[1],item[2],item[3],item[4])
                                   for item in self.data_current])
                loop.run_until_complete(aw)
        return self.final_list_of_articles      # body,title,rss,func,url,atime

def bs4_and_output(final_list_of_articles):
    count = len(final_list_of_articles)
    recieved = 0
    for html_item in final_list_of_articles:        # consist of body,title,rss,func,url,atime
        count -= 1
        app.label_status.configure(text='Осталось обработать: {}'.format(count), bg='#69969C')
        root.update()
        NA_obj = bs4_processing.NEWSAGENCY(html_item)
        func_result = getattr(NA_obj,html_item[3])()
        if func_result != False:       # Parse by IA name
            output.add_url_to_history(html_item[4])
            if func_result != 'no_interest':
                NA_obj.strip_texts()
                rss_a = html_item[2]
                title_a = html_item[1]
                date_a,time_a = NA_obj.get_time(html_item[5])
                maintext_a = NA_obj.main_text_class

                output.country = "Другие"
                output.define_country_by_zagolovok(title_a)
                if output.country == "Другие":
                    maintext_a = output.define_country_by_mtext(maintext_a)
                # if output.output_or_not(html_item[5]) == True:              # Передаем аргументом datetime_format
                recieved += 1
                if output.country == 'Украина' and (rss_a == 'УНИАН' or rss_a == 'Корреспондент' or
                                                    rss_a == 'РБК-Украина' or rss_a == 'Укринформ' or
                                                    rss_a == 'BlackSeaNews'):
                    patterns = ("[\w-]*террорист[а-я]*","боевик[а-я]*","сепаратист[а-я]*","самопровозглаш[а-я]*","оккупант[а-я]*","бандформирован[а-я]*")
                    for p in patterns:
                        p = "({})".format(p)
                        maintext_a = re.sub(p,r'"\1"',maintext_a,flags=re.IGNORECASE)
                try:
                    output.output_to_word(title_a, maintext_a, date_a, time_a,rss_a)
                except Exception as e:
                    output.output_to_txt(title_a, maintext_a, date_a, time_a,rss_a)
    return recieved

def check_license():
    if date.today() > expire_date:
        return False
    return True

def main():
    if check_license() == False:        # Check license
        app.label_status.configure(text="Обновите программу!", bg='red')
        return
    start = datetime.now()      # START TIME
    total_len = 0

    # global final_list_of_articles
    # final_list_of_articles = []
    app.label_status.configure(text='Начал скачивать RSS.\nОЖИДАЙТЕ...', bg='#69969C')
    root.update()
    get_rss_data()
    today_urls = today_filter(rss_threading.url_selected)
    app.label_status.configure(text='Начал скачивать СТАТЬИ.\nОЖИДАЙТЕ...')
    root.update()
    async_instance = Async(today_urls)
    final_list = async_instance.start_async()
    app.label_status.configure(text='Начал обработку СТАТЕЙ.\nОЖИДАЙТЕ...')
    root.update()
    recieved = bs4_and_output(final_list)       # body,title,rss,func,url,atime
    total = len(today_urls)
    downloaded = len(async_instance.final_list_of_articles)
    total_len += downloaded
    print('Total: {}'.format(total))
    logging.info('Total: {}'.format(total))
    print('Downloaded: {}'.format(downloaded))
    logging.info('Downloaded: {}'.format(downloaded))
    print("LEFT:")
    bad_url = ""
    for u in async_instance.data_changable:
        bad_url += '\n' + u[0]
    logging.info('Не скачаны следующие статьи:{}'.format(bad_url))

    end = datetime.now()        # STOP TIME
    delta = end - start
    delta = '{} сек.'.format(delta.seconds)

    print('Timing: {}'.format(delta))
    logging.info('Timing: {}'.format(delta))

    if recieved:
        otsechka()
        summary_text = 'Готово! Забирайте папку!\nc:\\от Паука\\'
        summary_text += '\nОтобрано: {}'.format(total)
        summary_text += '\nCкачано: {}'.format(total_len)
        summary_text += '\nИспользовано: {}'.format(recieved)
        color = 'yellow'
    elif len(rss_threading.rss_current_rest) > 20:
        summary_text = 'ПРОВЕРЬТЕ ИНТЕРНЕТ СОЕДИНЕНИЕ!!!'
        color = 'red'
    else:
        summary_text = 'Статей, представляющих интерес, не отмечено.'
        color = 'gray'
    summary_text += '\nЗатрачено времени: {}'.format(delta)
    if rss_threading.rss_current_rest and recieved:
        failed_rss = '\n'.join(rss_threading.rss_current_rest)
        summary_text += '\nНе получены новости от: \n{}'.format(failed_rss)
    app.label_status.configure(text=summary_text, bg=color, justify=LEFT)
    root.update()

def otsechka():
    second_path = output.output_folder + "от_Паука_на_" + str(datetime.now().strftime("%H.%M %d.%m.%Y")) + "\\"
    os.makedirs(second_path)
    try:
        for filename in glob.glob(os.path.join(output.output_folder, '*.doc')):
            shutil.move(filename, second_path)
        for filename in glob.glob(os.path.join(output.output_folder, '*.txt')):
            shutil.move(filename, second_path)
    except PermissionError as e:
        pass
    app.label_status.configure(text="Нажмите ПУСК", bg='#69969C')


class GUI():
    def __init__(self, root):
        root.title("ПАУК " + version)
        # root.iconbitmap("Icon.ico")
        # All Frames
        self.button_start = tk.Button(root, text="ПУСК", font=("Arial 15 bold"), bg='#012E34', fg='white',
                                      command=main)
        self.button_start.pack(fill=X)
        self.label_status = tk.Label(root, text="Нажмите ПУСК", font=("Arial 12"), bg='#69969C')
        self.label_status.pack(fill=X)
        # self.button_otsechka = tk.Button(root, text="ОТСЕЧКА", font=("Arial 12 bold"), bg='#427A82', command=otsechka)
        # self.button_otsechka.pack(fill=X)
        separator1 = tk.Frame(root, height=5, bg='#0E464E', bd=3)
        separator1.pack(fill=X)
        self.label_author = tk.Label(root, text='Версия: {} - 2015 г.\nРазработчик: Ли С.Е.'.format(version), bg='#69969C')
        self.label_author.pack(fill=X)

if __name__ == "__main__":

    version = '3.3'
    root = tk.Tk()
    app = GUI(root)

    root.mainloop()
