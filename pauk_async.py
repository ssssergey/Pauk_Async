__author__ = 'Asus'

from bs4 import BeautifulSoup

import asyncio
import aiohttp
import rss_threading
import bs4_processing


list_of_htmls = []


@asyncio.coroutine
def download_from_inet(url,title,rss,func):
    global list_of_htmls
    # response = yield from aiohttp.request('GET', url)
    print('Start downloading {}'.format(url))
    response = yield from asyncio.wait_for(aiohttp.request('GET', url), 10)  # With timeout
    body = yield from response.read_and_close()
    try:
        if rss in ['News-Asia', 'МигНьюс', 'Коммерсант', 'Грузия-онлайн', 'ЦАМТО']:
            body = body.decode(encoding='cp1251')
        else:
            body = body.decode(encoding='utf-8')
    except Exception as e:
        print(rss,e,'\n', file=open('errors.txt','a',encoding='utf-8'))
    list_of_htmls.append([body,title,rss,func])
    print('Finished {}'.format(url))


    # return (yield from response.read_and_close())
    # rus_body = lenta(body)

def lenta(html_text):
    soup = BeautifulSoup(html_text)
    try:
        vremya_class = soup.find('time', {'itemprop': 'datePublished'}).text
    except Exception as e:
        vremya_class = 'Empty'
    try:
        main_text_class = ''
        for everyitem in soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
            main_text_class = main_text_class + '\n' + everyitem.text
    except Exception as e:
        main_text_class = 'Empty'
    result = vremya_class + '\n' + main_text_class + '\n'
    print(result,file=open("result.txt",'a',encoding='utf-8'))




if __name__ == "__main__":

    pf = rss_threading.PullFeeds()
    pf.pullfeed()
    data = rss_threading.url_selected
    print(len(data))
    print(data[0])
    unique_ia = list(set(v[3] for v in data))
    print(unique_ia)
    for func_name in unique_ia:
        selected_by_ia_list = [item for item in data if item[3] == func_name]
        loop = asyncio.get_event_loop()
        aw = asyncio.wait([download_from_inet(item[0],item[1],item[2],item[3]) for item in selected_by_ia_list])
        loop.run_until_complete(aw)

        for html_item in list_of_htmls:
            # if html_item[3] == 'lenta':
            #     lenta(html_item[0])
            NA_obj = bs4_processing.NEWSAGENCY(html_item)
            if getattr(NA_obj,func_name)() != False:       # Parse by IA name
                NA_obj.strip_texts()
                print('{}\n{}\n{}\n{}\n\n'.format(html_item[2],NA_obj.zagolovok_class, NA_obj.get_time(),NA_obj.main_text_class),
                      file=open("result.txt",'a',encoding='utf-8'))
    #             if rss_name == 'Грузия-онлайн':
    #                 NA_obj.encoding_texts(encoding1='cp1252')
    #             else:
    #                 NA_obj.encoding_texts()
    #             NA_obj.strip_texts()
    #             NA_obj.raw_vremya_to_list_vremya()
    #             NA_obj.list_vremya_to_datetime_format()
    #             NA_obj.final_vremya()
    #             NA_obj.define_country_by_zagolovok()
    #             if NA_obj.country == "Другие":
    #                 NA_obj.define_country_by_mtext()
    #             if not os.path.exists(output_folder):
    #                 os.makedirs(output_folder)
    #             try:
    #                 NA_obj.output_to_sql()
    #             except Exception as e:
    #                 error_log(str(e) + '\n')
    #             if NA_obj.output_or_not() == True:
    #                 if NA_obj.country == 'Украина' and (rss_name == 'УНИАН' or rss_name == 'Корреспондент' or rss_name == 'РБК-Украина'
    #                                                     or rss_name == 'Укринформ' or rss_name == 'BlackSeaNews'):
    #                     patterns = ("[\w-]*террорист[а-я]*","боевик[а-я]*","сепаратист[а-я]*","самопровозглаш[а-я]*","оккупант[а-я]*","бандформирован[а-я]*")
    #                     # p = re.compile('([\w-]*террорист\w*|боевик\w*|сепаратист\w*|самопровозглаш\w*|оккупант\w*|бандформирован\w*)', re.IGNORECASE)
    #                     # NA_obj.main_text_class = p.sub('"\\1"',NA_obj.main_text_class, flags=re.IGNORECASE)
    #                     for p in patterns:
    #                         p = "({})".format(p)
    #                         NA_obj.main_text_class = re.sub(p,r'"\1"',NA_obj.main_text_class,flags=re.IGNORECASE)
    #                 try:
    #                     NA_obj.output_to_word()
    #                 except Exception as e:
    #                     NA_obj.output_to_txt()
    #                     error_log(str(e))
    #         else:
    #             return False
    #
        #
        #
        list_of_htmls = []