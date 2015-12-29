#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime, date
import time
import os
from config import output_folder, history_file, country_filter

try:
    import win32com.client
    from win32com.gen_py import *
except:
    pass


if not os.path.exists(output_folder):
    os.makedirs(output_folder)


country = "Другие"

def define_country_by_zagolovok(title_a):
    global country
    for k in country_filter.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(title_a) or p.search(title_a.lower()):
                country = k[1]
                return

def define_country_by_mtext(mtext_a):
    global country
    for k in country_filter.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(mtext_a[:350]) or p.search(mtext_a[:350].lower()):  # Поиск производится примерно в первых двух абзацах (350 знаков) осн текста
                country = k[1]
                return mtext_a
    return mtext_a

def output_or_not(datetime_format):
    str_date = str(datetime_format.date())
    today_date = str(datetime.today().date())
    if str_date != today_date:
        return False
    else:
        return True

def output_to_txt(title_a, mtext_a, date_a, time_a,rss_a):
    with open(output_folder + country + ' ' + str(date.today()) + '.txt', 'a', encoding='utf-8') as text_file:
        try:
            text_file.write('{} ({} ИА "{}")\n'.format(date_a,time_a,rss_a))
            text_file.write('{}\n'.format(title_a))
            text_file.write('{}\n\n'.format(mtext_a))
        except Exception as e:
            print(str(e) + '\n')

def output_to_word(title_a, mtext_a, date_a, time_a,rss_a):
    wordapp = win32com.client.gencache.EnsureDispatch("Word.Application") # Create new Word Object
    wordapp.Visible = 1 # Word Application should`t be visible
    out_path = output_folder + country + ' ' + str(date.today()) + ".doc"
    if not os.path.isfile(out_path):
        worddoc = wordapp.Documents.Add() # Create new Document Object
        time.sleep(0.3)
        worddoc.SaveAs(out_path)
    else:
        worddoc = wordapp.Documents.Open(out_path) # Create new Document Object
        time.sleep(0.2)
    worddoc.Content.Font.Size = 14
    worddoc.Content.Font.Name = "Times New Roman"
    worddoc.Content.ParagraphFormat.FirstLineIndent = 35
    worddoc.Paragraphs.LineSpacingRule = win32com.client.constants.wdLineSpaceSingle
    worddoc.Paragraphs.SpaceBefore = 0
    worddoc.Paragraphs.SpaceAfter = 0
    wordapp.Selection.EndKey (win32com.client.constants.wdStory)
    wordapp.Selection.ParagraphFormat.Alignment = win32com.client.constants.wdAlignParagraphRight
    wordapp.Selection.TypeText('{} ({} ИА "{}")\n'.format(date_a,time_a,rss_a))
    wordapp.Selection.ParagraphFormat.Alignment = win32com.client.constants.wdAlignParagraphJustify
    wordapp.Selection.Font.Bold = True
    wordapp.Selection.TypeText('{}\n'.format(title_a))
    wordapp.Selection.Font.Bold = False
    wordapp.Selection.TypeText('{}\n\n'.format(mtext_a))
    worddoc.Save()
    worddoc.Close()
    # wordapp.Quit()



def add_url_to_history(url):
    with open(history_file, 'a') as history_txt:
        history_txt.write(url + ' ' + str(datetime.now()) + '\n')



