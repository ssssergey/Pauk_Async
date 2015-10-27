__author__ = 'Asus'

from bs4 import BeautifulSoup
from datetime import date, datetime,timedelta
import logging

logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='Debugging.txt')

class NEWSAGENCY():
    def __init__(self,item):
        self.vremya_class = ''
        self.zagolovok_class = item[1]
        self.main_text_class = ''
        self.soup = BeautifulSoup(item[0])
        for script in self.soup.findAll('script'):   # Delete all js scripts from soup
            script.decompose()
        for style in self.soup.findAll('style'):     # Delete all css styles from soup
            style.decompose()
        self.rss_name = item[2]

    def get_time(self):
        # raw_vremya_to_list_vremya
        self.vremya_class = self.vremya_class.replace(":", " ").replace(".", " ").replace(",","").replace("/"," ").\
            replace(" | "," ").replace(" - "," ").replace("\xa0"," ").replace("[","").replace("]","").replace("-"," ")
        self.vremya_class = [line.strip() for line in self.vremya_class.split(' ') if line.strip()]
        print (self.vremya_class)
        if not self.vremya_class:
            self.vremya_class = 'Empty'
        # list_vremya_to_datetime_format
        ddd = "00"
        mmm = "00"
        yyy = "00"
        HHH = "00"
        MMM = "00"
        if 'Empty' in self.vremya_class:
            ddd = str(date.today().day)
            mmm = str(date.today().month)
            yyy = str(date.today().year)
        else:
            month_dict = {'января':'01','февраля':'02','марта':'03','апреля':'04','мая':'05','июня':'06','июля':'07','августа':'08',
                          'сентября':'09','октября':'10','ноября':'11','декабря':'12'}
            if self.rss_name == "BlackSeaNews":
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = self.vremya_class[3]
                yyy = self.vremya_class[4]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1]
            elif self.rss_name == "News-Asia":
                if "Сегодня" in self.vremya_class:
                    ddd = str(date.today().day)
                    mmm = str(date.today().month)
                    yyy = str(date.today().year)
                    HHH = self.vremya_class[1]
                    MMM = self.vremya_class[2]
                else:
                    ddd = self.vremya_class[0].rjust(2,'0')
                    mmm = month_dict[self.vremya_class[1]]
                    yyy = self.vremya_class[2]
                    HHH = self.vremya_class[3]
                    MMM = self.vremya_class[4]
            elif self.rss_name == "Би-Би-Си":                # 11 3 2015 16 36
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Грузия-онлайн":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "ИТАР-ТАСС":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = month_dict[self.vremya_class[1]]
                yyy = str(date.today().year)
                HHH = self.vremya_class[2]
                MMM = self.vremya_class[3]
            elif self.rss_name == "Кавказский узел":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = month_dict[self.vremya_class[1]]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Коммерсант":
                ddd = self.vremya_class[0]
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Корреспондент":
                if "Сегодня" in self.vremya_class:
                    ddd = str(date.today().day)
                    mmm = str(date.today().month)
                    yyy = str(date.today().year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                elif "Вчера" in self.vremya_class:
                    yesterday = date.today() - timedelta(days=1)
                    ddd = str(yesterday.day)
                    mmm = str(yesterday.month)
                    yyy = str(yesterday.year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                else:
                    ddd = self.vremya_class[-5].rjust(2,'0')
                    mmm = month_dict[self.vremya_class[-4]]
                    yyy = self.vremya_class[-3]
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
            elif self.rss_name == "Лента.ру":                #  18:54, 11 марта 2015
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = month_dict[self.vremya_class[3]]
                yyy = self.vremya_class[4]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1]
            elif self.rss_name == "МигНьюс":             # 11.03 14:40     MIGnews.com
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = str(date.today().year)
                HHH = self.vremya_class[2]
                MMM = self.vremya_class[3]
            elif self.rss_name == "Росбалт":
                ddd = self.vremya_class[1].rjust(2,'0')
                mmm = self.vremya_class[2]
                yyy = self.vremya_class[3]
                HHH = self.vremya_class[4]
                MMM = self.vremya_class[5]
            elif self.rss_name == "РИА-Новости":
                ddd = self.vremya_class[1][2:].rjust(2,'0')
                mmm = self.vremya_class[2]
                yyy = self.vremya_class[3]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1][:2]
            elif self.rss_name == "Тренд":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = month_dict[self.vremya_class[1]]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "УНИАН":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Укринформ":
                if "сегодня" in self.vremya_class:      # сегодня 20:43
                    ddd = str(date.today().day)
                    mmm = str(date.today().month)
                    yyy = str(date.today().year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                elif "вчера" in self.vremya_class:
                    yesterday = date.today() - timedelta(days=1)
                    ddd = str(yesterday.day)
                    mmm = str(yesterday.month)
                    yyy = str(yesterday.year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                else:                                           # 13.10.2015 20:50
                    ddd = self.vremya_class[0].rjust(2,'0')
                    mmm = self.vremya_class[1]
                    yyy = self.vremya_class[2]
                    HHH = self.vremya_class[3]
                    MMM = self.vremya_class[4]
            elif self.rss_name == "ЦАМТО":
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = month_dict[self.vremya_class[3]]
                yyy = self.vremya_class[4]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1]
            elif self.rss_name == "ВПК":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = month_dict[self.vremya_class[1]]
                yyy = self.vremya_class[2]
                # HHH = self.vremya_class[0]
                # MMM = self.vremya_class[1]
            elif self.rss_name == "Фергана":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "РБК-Украина":     # 11.03.2015 - 17:32
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Ведомости":      # 2015-10-26 22:39:38 +0300
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[0]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "APA.AZ":          # 02 Октября 2015 / 20:23
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = month_dict[self.vremya_class[1].lower()]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Новости-Грузия":
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = self.vremya_class[3]
                yyy = self.vremya_class[4]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1]
            elif self.rss_name == "РБК":
                if "сегодня" in self.vremya_class:
                    ddd = str(date.today().day)
                    mmm = str(date.today().month)
                    yyy = str(date.today().year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                elif "вчера" in self.vremya_class:
                    yesterday = date.today() - timedelta(days=1)
                    ddd = str(yesterday.day)
                    mmm = str(yesterday.month)
                    yyy = str(yesterday.year)
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
                else:
                    ddd = self.vremya_class[-5].rjust(2,'0')
                    mmm = month_dict[self.vremya_class[-4]]
                    yyy = self.vremya_class[-3]
                    HHH = self.vremya_class[-2]
                    MMM = self.vremya_class[-1]
            elif self.rss_name == "ИРНА":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "RussiaToday":
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                HHH = self.vremya_class[3]
                MMM = self.vremya_class[4]
            elif self.rss_name == "Апсны-Пресс":                #  18:54, 11 марта 2015
                ddd = self.vremya_class[2].rjust(2,'0')
                mmm = month_dict[self.vremya_class[3].lower()]
                yyy = self.vremya_class[4]
                HHH = self.vremya_class[0]
                MMM = self.vremya_class[1]
            elif self.rss_name == "САНА":                #  26/08/2015
                ddd = self.vremya_class[0].rjust(2,'0')
                mmm = self.vremya_class[1]
                yyy = self.vremya_class[2]
                # HHH = self.vremya_class[0]
                # MMM = self.vremya_class[1]
        print(ddd,mmm,yyy,HHH,MMM)
        self.datetime_format = datetime(int(yyy),int(mmm),int(ddd),int(HHH),int(MMM))
        if self.rss_name == "Тренд": self.datetime_format = self.datetime_format - timedelta(hours=2)
        if self.rss_name == "APA.AZ": self.datetime_format = self.datetime_format - timedelta(hours=2)
        if self.rss_name == "ИРНА": self.datetime_format = self.datetime_format - timedelta(minutes=30)
        # final_vremya
        month_names = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
        self.month_name = month_names[self.datetime_format.month - 1]
        self.date_final = '{} {} {} г.'.format(str(self.datetime_format.day).lstrip("0"),self.month_name,str(self.datetime_format.year))
        self.time_final = self.datetime_format.strftime("%H.%M")
        return self.date_final, self.time_final
    def strip_texts(self):
        self.main_text_class = "\n".join([line.strip() for line in self.main_text_class.split('\n') if line.strip()])

    def korrespondent(self):
        try:
            self.vremya_class = self.soup.find('div', {'class':'post-item__info'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = self.soup.find('div', {'class': 'post-item__text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def unian(self):
        try:
            self.vremya_class = self.soup.find('div', {'class':'date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'article_body'}).findAll('p',recursive=False):
                if "Читайте также" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def ukrinform(self):
        try:
            self.vremya_class = self.soup.find('span',{'class':'newsDate'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'newsText'}).findAll('p',recursive=False):
                if "Читайте также:" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def rbc_ukr(self):
        try:
            self.vremya_class = self.soup.find('span',{'class':'date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = self.soup.find('div', {'class':'text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def rbc_rus(self):
        try:
            self.vremya_class = self.soup.find('span',{'class':'article__head__tabs__date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'article__text'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def bbc(self):
        self.vremya_class = 'Empty'
        if self.soup.find('p', {'class':'date date--v1'}):
            self.vremya_class = self.soup.find('p', {'class':'date date--v1'})
        elif self.soup.find('div', {'class':'date date--v2'}):
            self.vremya_class = self.soup.find('div', {'class':'date date--v2'})
        if self.vremya_class != 'Empty':
            try:
                self.vremya_class = self.vremya_class['data-seconds']
                d = datetime.fromtimestamp(int(self.vremya_class))
                self.vremya_class = d.strftime("%d.%m.%Y %H:%M")
            except Exception as e:
                logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
        main_div = self.soup.find('div', {'class': 'story-body__inner'})
        if not main_div: main_div = self.soup.find('div', {'class': 'map-body'})
        if not main_div: return
        try:
            self.main_text_class = ''
            for everyitem in main_div.findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def lenta(self):
        try:
            self.vremya_class = self.soup.find('time', {'itemprop': 'datePublished'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def rian(self):
        for everyitem in self.soup.findAll('p', {'style': 'text-align: center;'}):
            everyitem.replaceWith('')
        try:
            self.vremya_class = self.soup.find('time', {'itemprop': 'dateCreated'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def trend(self):
        try:
            self.vremya_class = self.soup.find('div', {'class': 'social-block'}).find('span', {'class': 'date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                if "@www_Trend_Az" not in everyitem.text and "agency@trend.az" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def mignews(self):
        try:
            self.vremya_class = self.soup.find('span', {'class': 'txtm'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        for everyitem in self.soup.findAll('noindex', recursive=False):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('iframe'):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'addthis_toolbox addthis_default_style pad2'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('ul'):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('h5'):
            everyitem.replaceWith('')
        if self.soup.find('div', {'class': 'textnews'}):
            self.main_text_class = self.soup.find('div', {'class': 'textnews'}).text + '\n\n'
        elif self.soup.find('div', {'id': 'leftc'}):
            self.main_text_class = self.soup.find('div', {'id': 'leftc'}).text + '\n\n'
        else:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def kavuzel(self):
        try:
            self.vremya_class = self.soup.find('p', {'class': 'time'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        for everyitem in self.soup.findAll('div', {'class': 'lt-feedback_banner pull-right hidden-phone'}):
                everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'articles-body'}).findAll('p',recursive=False):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def kommersant(self):
        try:
            self.vremya_class = self.soup.find('time', {'class': 'title__cake'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('p', {'class': 'b-article__text'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def vedomosti(self):
        try:
            # self.vremya_class = self.soup.find('span', {'class': 'b-news-item__time b-news-item__time_one'}).text
            self.vremya_class = self.soup.find('time', {'class': 'b-news-item__time b-news-item__time_one'})
            self.vremya_class = self.vremya_class['pubdate']
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-news-item__text b-news-item__text_one'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def georgiaonline(self):
        try:
            self.vremya_class = self.soup.find('div', {'class': 'time1'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('td', {'class': 'newsbody'}).findAll('div', {'class': 'txt-item-news'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def blacksea(self):
        if 'Attention Required!' in self.soup.html.head.title.text:
            return False
        # ИЗВЛЕЧЕНИЕ ВРЕМЕНИ, ЗАГОЛОВКА И ТЕКСТА ПО HTML ТЭГАМ
        for everyitem in self.soup.findAll('a', {'class': 'icon comment'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'class': ' flagLinks-moldova'}):
            everyitem.replaceWith('')
        try:
            self.vremya_class = self.soup.find('tr').text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div', {'id': 'contentText'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def camto(self):
        if '401' in self.soup.html.head.title.text:
            logging.warning('%%%%%Платная статья.\n')
            self.main_text_class = 'ПЛАТНАЯ СТАТЬЯ'
            self.vremya_class = 'Empty'
            return
        # ИЗВЛЕЧЕНИЕ ВРЕМЕНИ, ЗАГОЛОВКА И ТЕКСТА ПО HTML ТЭГАМ
        try:
            self.vremya_class = self.soup.find('div', {'class': 'beforedate'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'content'}).find('div', {'class': 'mainnews'}).findAll('div'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def itartass(self):
        try:
            self.vremya_class = self.soup.find('span', {'class': 'b-material__date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        for everyitem in self.soup.findAll('div', {'class': 'b-gallery-widget-item'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links b-links_mini b-links_right printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'target': '_blank'}):
            everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-material-text__l'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def rosbalt(self):
        try:
            self.vremya_class = self.soup.find('div', {'id': 'mat_head'}).find('div', {'style': 'float:left;'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            # mat_cont = self.soup.find('div', {'id': 'mat_cont'})
            for everyitem in self.soup.find('article').findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
            # if not self.main_text_class:
            #     print("Росбалт: Вариатн 2")
            #     self.main_text_class = mat_cont.find('article').text
            #     print(self.main_text_class)
            # else:
            #     print("Росбалт: Вариатн 1")
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def vpk(self):
        try:
            self.vremya_class = self.soup.find('h1', {'class': 'title'}).find('div', {'class': 'submitted'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'field-item even','property':'content:encoded'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
            if len(self.main_text_class) > 4000:
                logging.warning('%%%%%Скорее всего это был анализ.УДАЛЕНО.\n')
                return 'no_interest'
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def news_asia(self):
        try:
            self.vremya_class = self.soup.find('div', {'class': 'top'}).find('p', {'class': 'info'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div',{'class':'content'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def fergana(self):
        try:
            self.vremya_class = self.soup.find('div', {'id': 'authors'}).find('p').text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div',{'id':'text'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def apa_az(self):
        try:
            self.vremya_class = self.soup.find('div', {'class': 'news_date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'content'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def newsgeorgia(self):
        try:
            self.vremya_class = self.soup.find('time', {'class': 'b-article__refs-date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-article__text'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def irna(self):
        try:
            self.vremya_class = self.soup.find('span', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_NofaDateLabel2'}).text + \
                ' ' + self.soup.find('span', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_NofaDateLabel3'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            self.main_text_class = self.main_text_class + '\n' + self.soup.find('h3', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_H1'}).text
            self.main_text_class = self.main_text_class + '\n' + self.soup.find('p', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_BodyLabel'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def rustoday(self):
        try:
            self.vremya_class = self.soup.find('time', {'itemprop': 'datePublished'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('article', {'id': 'content'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def apsnypress(self):
        try:
            self.vremya_class = self.soup.find('div', {'class': 'newslist_date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = self.soup.find('div', {'class': 'detail_text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'
    def sana(self):
        try:
            self.vremya_class = self.soup.find('span', {'class': 'tie-date'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.vremya_class.\n'.format(self.rss_name))
            self.vremya_class = 'Empty'
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'entry'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n'.format(self.rss_name))
            return False
        return 'Ok'

# def error_log(new_error, file='Debugging.txt'):
#     with open(file,'a',encoding='utf-8') as f:
#         try:
#             f.write(new_error)
#         except Exception as e:
#             print(str(e))
