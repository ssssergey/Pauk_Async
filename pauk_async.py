__author__ = 'Asus'

from datetime import datetime

import asyncio
import aiohttp
import rss_threading
import bs4_processing
import output
import re
import logging

logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='Debugging.txt')

@asyncio.coroutine
def download_from_inet(url,title,rss,func):
    global list_of_htmls
    print('Start downloading {}'.format(url))
    logging.info('Start downloading {}'.format(url))
    response = yield from asyncio.wait_for(aiohttp.request('GET', url), 40)  # With timeout
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


if __name__ == "__main__":
    start = datetime.now()
    # RSS threading
    pf = rss_threading.PullFeeds()
    pf.pullfeed()
    data = rss_threading.url_selected
    data_current = data[:]
    data_changable = data[:]
    # data_only_urls = [i[0] for i in data]
    list_of_htmls = []

    for i in range(3):
        print("ROUND {}".format(i))
        if data_changable:
            data_current = data_changable[:]
            loop = asyncio.get_event_loop()
            aw = asyncio.wait([download_from_inet(item[0],item[1],item[2],item[3]) for item in data_current])
            loop.run_until_complete(aw)



    for html_item in list_of_htmls:
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
    end = datetime.now()
    delta = end - start
    print('Timing: {}'.format(delta))
    logging.info('Timing: {}'.format(delta))
    print('Total: {}'.format(len(data)))
    logging.info('Total: {}'.format(len(data)))
    print('Downloaded: {}'.format(len(list_of_htmls)))
    logging.info('Downloaded: {}'.format(len(list_of_htmls)))

    print("LEFT:")
    for u in data_changable:
        print(u[0])