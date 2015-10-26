__author__ = 'Asus'

from datetime import datetime, date
import asyncio
import aiohttp
import logging
import shutil
import glob
import tkinter as tk
from tkinter.filedialog import *

import rss_threading
import bs4_processing
import output


expire_date = date(2015,12,1) # Date of the program license expiration

logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='Debugging.txt')
data_changable = []
list_of_htmls = []

def get_rss_data():
    # RSS threading
    rss_threading.url_selected = []
    pf = rss_threading.PullFeeds()
    pf.pullfeed()

@asyncio.coroutine
def download_HTMLs_to_HTMLlist(url,title,rss,func):
    global list_of_htmls
    global data_changable
    print('Start downloading {}'.format(url))
    logging.info('Start downloading {}'.format(url))
    response = yield from asyncio.wait_for(aiohttp.request('GET', url), 30)  # With timeout
    body = yield from response.read_and_close()
    try:
        if rss in ['News-Asia', 'МигНьюс', 'Коммерсант', 'Грузия-онлайн', 'ЦАМТО']:
            body = body.decode(encoding='cp1251')
        else:
            body = body.decode(encoding='utf-8')
    except Exception as e:
        print(rss,e,'\n', file=open('errors.txt','a',encoding='utf-8'))
    list_of_htmls.append([body,title,rss,func,url])
    try:
        data_changable.remove((url,title,rss,func))
    except:
        pass
    print('Finished {}'.format(url))
    logging.info('Finished {}'.format(url))
    app.label_status.configure(text='Осталось скачать статей: {}'.format(len(data_changable)), bg='#69969C')
    root.update()

def start_async():
    global data_changable
    data_current = rss_threading.url_selected[:]
    data_changable = rss_threading.url_selected[:]
    for i in range(3):
        print("ROUND {}".format(i))
        if data_changable:
            data_current = data_changable[:]
            loop = asyncio.get_event_loop()
            aw = asyncio.wait([download_HTMLs_to_HTMLlist(item[0],item[1],item[2],item[3]) for item in data_current])
            loop.run_until_complete(aw)

def bs4_and_output():
    count = len(list_of_htmls)
    for html_item in list_of_htmls:
        count -= 1
        app.label_status.configure(text='Осталось обработать: {}'.format(count), bg='#69969C')
        root.update()
        NA_obj = bs4_processing.NEWSAGENCY(html_item)
        if getattr(NA_obj,html_item[3])() != False:       # Parse by IA name
            output.add_url_to_history(html_item[4])
            NA_obj.strip_texts()
            rss_a = html_item[2]
            title_a = NA_obj.zagolovok_class
            date_a,time_a = NA_obj.get_time()
            maintext_a = NA_obj.main_text_class

            output.country = "Другие"
            output.define_country_by_zagolovok(title_a)
            if output.country == "Другие":
                maintext_a = output.define_country_by_mtext(maintext_a)
            if output.output_or_not(NA_obj.datetime_format) == True:
                if output.country == 'Украина' and (rss_a == 'УНИАН' or rss_a == 'Корреспондент' or
                                                    rss_a == 'РБК-Украина' or rss_a == 'Укринформ' or
                                                    rss_a == 'BlackSeaNews'):
                    patterns = ("[\w-]*террорист[а-я]*","боевик[а-я]*","сепаратист[а-я]*","самопровозглаш[а-я]*","оккупант[а-я]*","бандформирован[а-я]*")
                    for p in patterns:
                        p = "({})".format(p)
                        maintext_a = re.sub(p,r'"\1"',maintext_a,flags=re.IGNORECASE)
                output.output_to_txt(title_a, maintext_a, date_a, time_a,rss_a)

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
    for i in range(2):
        global list_of_htmls
        list_of_htmls = []
        app.label_status.configure(text='Начал скачивать RSS.\nОЖИДАЙТЕ...', bg='#69969C')
        root.update()
        get_rss_data()
        app.label_status.configure(text='Начал скачивать СТАТЬИ.\nОЖИДАЙТЕ...')
        root.update()
        start_async()
        app.label_status.configure(text='Начал обработку СТАТЕЙ.\nОЖИДАЙТЕ...')
        root.update()
        bs4_and_output()
        total = len(rss_threading.url_selected)
        downloaded = len(list_of_htmls)
        total_len += downloaded
        print('Total: {}'.format(total))
        logging.info('Total: {}'.format(total))
        print('Downloaded: {}'.format(downloaded))
        logging.info('Downloaded: {}'.format(downloaded))
        print("LEFT:")
        bad_url = ""
        for u in data_changable:
            bad_url += '\n' + u[0]
            print(u[0])
        logging.info('Не скачаны следующие статьи:{}'.format(bad_url))
        if not rss_threading.rss_current:
            break
    end = datetime.now()        # STOP TIME
    delta = end - start
    delta = '{} сек.'.format(delta.seconds)

    print('Timing: {}'.format(delta))
    logging.info('Timing: {}'.format(delta))

    if total_len:
        otsechka()
        summary_text = 'Готово! Забирайте папку!'
        summary_text += '\nCкачано статей: {}'.format(total_len)
        color = 'yellow'
    else:
        summary_text = 'Статей, представляющих интерес, не добыто.'
        color = 'gray'
    summary_text += '\nЗатрачено времени: {}'.format(delta)
    app.label_status.configure(text=summary_text, bg=color)
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
        root.title("ПАУК Next " + version)
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

    # Tkinter
    version = '1.0'
    root = tk.Tk()
    app = GUI(root)

    root.mainloop()