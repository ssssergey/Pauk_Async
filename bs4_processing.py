#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from config import logger


class NEWSAGENCY():
    def __init__(self, html_script):
        self.main_text_class = ''
        self.soup = BeautifulSoup(html_script, "html.parser")
        for script in self.soup.findAll('script'):   # Delete all js scripts from soup
            script.decompose()
        for style in self.soup.findAll('style'):     # Delete all css styles from soup
            style.decompose()
    def strip_texts(self):
        self.main_text_class = "\n".join([line.strip() for line in self.main_text_class.split('\n') if line.strip()])

    def korrespondent(self):
        self.main_text_class = self.soup.find('div', {'class': 'post-item__text'}).text

    def unian(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'article_body'}).findAll('p',recursive=False):
            if "Читайте также" not in everyitem.text:
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def ukrinform(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div',{'class':'newsText'}).findAll('p',recursive=False):
            if "Читайте также:" not in everyitem.text:
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def rbc_ukr(self):
        self.main_text_class = ''
        for script in self.soup.findAll('div',{'class':'editorschoice hidemobile'}):   # Delete all js scripts from soup
            script.decompose()
        for everyitem in self.soup.find('div',{'class':'text'}).findAll('p',recursive=False):
            if "Читайте также:" not in everyitem.text:
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def rbc_rus(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div',{'class':'article__text'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def bbc(self):
        main_div = self.soup.find('div', {'class': 'story-body__inner'})
        if not main_div: main_div = self.soup.find('div', {'class': 'map-body'})
        if not main_div: return
        self.main_text_class = ''
        for everyitem in main_div.findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def lenta(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def rian(self):
        for everyitem in self.soup.findAll('p', {'style': 'text-align: center;'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def trend(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
            if "@www_Trend_Az" not in everyitem.text and "agency@trend.az" not in everyitem.text:
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def mignews(self):
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
    def kavuzel(self):
        for everyitem in self.soup.findAll('div', {'class': 'lt-feedback_banner pull-right hidden-phone'}):
                everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'articles-body'}).findAll('p',recursive=False):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def kommersant(self):
        self.main_text_class = ''
        for everyitem in self.soup.findAll('p', {'class': 'b-article__text'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def vedomosti(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'b-news-item__text b-news-item__text_one'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def georgiaonline(self):
        for trash in self.soup.findAll('a'):
            trash.decompose()
        for trash in self.soup.findAll('strong'):
            trash.decompose()
        self.main_text_class = ''
        for everyitem in self.soup.find('td', {'class': 'newsbody'}).findAll('div', {'class': 'txt-item-news'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def blacksea(self):
        if 'Attention Required!' in self.soup.html.head.title.text:
            return False
        # ИЗВЛЕЧЕНИЕ ВРЕМЕНИ, ЗАГОЛОВКА И ТЕКСТА ПО HTML ТЭГАМ
        for everyitem in self.soup.findAll('a', {'class': 'icon comment'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'class': ' flagLinks-moldova'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.findAll('div', {'id': 'contentText'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def camto(self):
        if '401' in self.soup.html.head.title.text:
            # logger.warning('%%%%%Платная статья.\n')
            self.main_text_class = 'ПЛАТНАЯ СТАТЬЯ'
            self.vremya_class = 'Empty'
            return
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'content'}).find('div', {'class': 'mainnews'}).findAll('div'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def itartass(self):
        for everyitem in self.soup.findAll('div', {'class': 'b-gallery-widget-item'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links b-links_mini b-links_right printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'target': '_blank'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'b-material-text__l'}).findAll('p', recursive=False):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def rosbalt(self):
        self.main_text_class = ''
        # mat_cont = self.soup.find('div', {'id': 'mat_cont'})
        for everyitem in self.soup.find('article').findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
        if not self.main_text_class:
            self.main_text_class = self.soup.find('article').text
    def vpk(self):
        self.main_text_class = ''
        for everyitem in self.soup.findAll('div',{'class':'field-item even'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text.strip()
    def news_asia(self):
        self.main_text_class = ''
        for everyitem in self.soup.findAll('div',{'class':'content'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def fergana(self):
        self.main_text_class = ''
        for everyitem in self.soup.findAll('div',{'id':'text'}):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def apa_az(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div',{'class':'content'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def newsgeorgia(self):
        for everyitem in self.soup.findAll('div', {'class': 'b-inject'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'b-article__text'}).findAll('p', recursive=False):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def irna(self):
        self.main_text_class = ''
        self.main_text_class = self.main_text_class + '\n' + self.soup.find('h3', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_H1'}).text
        self.main_text_class = self.main_text_class + '\n' + self.soup.find('p', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_BodyLabel'}).text
    def rustoday(self):
        for everyitem in self.soup.findAll('p', {'class': 'disclaimer'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('article', {'id': 'content'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def apsnypress(self):
        self.main_text_class = self.soup.find('div', {'class': 'detail_text'}).text
    def sana(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'entry'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def rianovosti(self):
        for everyitem in self.soup.findAll('div', {'class': 'inject_type2'}):
            everyitem.replaceWith('')
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'id': 'article_full_text'}).findAll('p'):
            if "Читайте также:" not in everyitem.text:
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def dan(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'entry'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def anadolu(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('div', {'class': 'article-post-content'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text
    def armenpress(self):
        self.main_text_class = ''
        for everyitem in self.soup.find('span', {'itemprop': 'articleBody'}).findAll('p'):
            self.main_text_class = self.main_text_class + '\n' + everyitem.text

if __name__ == '__main__':
    import requests
    html_code = requests.get("http://ria.ru/world/20160220/1378032785.html")
    # html_code.encoding = 'cp1251'
    plain_text = html_code.text
    obj = NEWSAGENCY(plain_text)
    obj.rianovosti()
    print(obj.main_text_class)