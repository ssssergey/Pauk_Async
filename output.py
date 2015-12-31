#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime, date
import time
import os
import sqlite3
from config import output_folder, os_current, text_size_limit, db_file, logger_bucket, logger
try:
    import win32com.client
    from win32com.gen_py import *
except:
    pass


def output_to_txt(title_a, mtext_a, date_a, time_a, rss_a, country):
    with open(output_folder + country + ' ' + str(date.today()) + '.txt', 'a', encoding='utf-8') as text_file:
        try:
            text_file.write('{} ({} ИА "{}")\n'.format(date_a,time_a,rss_a))
            text_file.write('{}\n'.format(title_a))
            text_file.write('{}\n\n'.format(mtext_a))
            return True
        except Exception as e:
            logger.warning(str(e))
            print(str(e) + '\n')

def output_to_word(title_a, mtext_a, date_a, time_a, rss_a, country):
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
    return True
    # wordapp.Quit()

def output_to_sql(title_a, mtext_a, dtformat, rss_a, country):
    try:
        current_time = datetime.now()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS main(rss_source TEXT, article_title TEXT, article_text TEXT, article_time TEXT,
                    extraction_time TEXT, country TEXT, id INTEGER PRIMARY KEY)''')
        cur.execute('''INSERT INTO main (rss_source, article_title, article_text, article_time, extraction_time, country) VALUES (
            ?,?,?,?,?,?)''',(rss_a,title_a,mtext_a,dtformat,current_time,country))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.warning(str(e))


def output(title_a, maintext_a, dtformat, date_a, time_a, rss_a, country):
    # if output.country == 'Украина' and (rss_a == 'УНИАН' or rss_a == 'Корреспондент' or
    #                                     rss_a == 'РБК-Украина' or rss_a == 'Укринформ' or
    #                                     rss_a == 'BlackSeaNews'):
    #     patterns = ("[\w-]*террорист[а-я]*","боевик[а-я]*","сепаратист[а-я]*","самопровозглаш[а-я]*","оккупант[а-я]*","бандформирован[а-я]*")
    #     for p in patterns:
    #         p = "({})".format(p)
    #         maintext_a = re.sub(p,r'"\1"',maintext_a,flags=re.IGNORECASE)

    if len(maintext_a) > text_size_limit:
        logger_bucket.warning(title_a + " - СЛИШКОМ БОЛЬШОЙ ТЕКСТ")
        return False
    if os_current == 'Windows':
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        try:
            if output_to_word(title_a, maintext_a, date_a, time_a, rss_a, country):
                return True
            else:
                return False
        except Exception as e:
            if output_to_txt(title_a, maintext_a, date_a, time_a, rss_a, country):
                return True
            else:
                return False
    elif os_current == 'Linux':
        if country != 'Другие':
            if output_to_sql(title_a, maintext_a, dtformat, rss_a, country):
                return True
            else:
                return False
