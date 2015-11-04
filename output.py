__author__ = 'Asus'
import re
import collections
from datetime import datetime, date
import time
import os
try:
    import win32com.client
    from win32com.gen_py import *
except:
    pass

output_folder = 'c:\\от Паука\\'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

country_dict1 = collections.OrderedDict([
    (('азербайдж','Баку(?!\s*\-\s*АПА\.)','карабах','армян','ереван','Армени','бакинск','нахчыван'),'Азербайджан'),
    (('Абхази', 'вазиани', 'Гальск', '(?!Новости\-)Грузи[а-я]', 'грузин', 'кутаиси', 'сенаки', 'сухуми', 'тбилиси[^,]',
      'цхинвали','джавахет','чахалян','Поти','\\bбатум','Аласан','Южн[а-я]{,2} Осет[а-я]{,2}','Маргвелашвили',
      'Гарибашвили','Хидашели','Усупашвили'),'Грузия'),
    (('анкар', '\\bРПК[^А-Я]', 'стамбул', 'турецк', 'турц','Аселсан','Отокар','Эрдоган'),'Турция'),
    (('беэр-шев', 'иерусалим', 'израил', 'нетаниягу', 'палестин', 'самари', 'Газа','Газы', 'тель-авив', 'хамас', 'цахал','шабак','кнессет',
     'хеврон','либерман','рахат','хайф','сектор[а-я]{,3} газа','Яалон','Ганц','Машаль','железный купол','IAI','Голанск','Голаны'),'Израиль'),
    (('Грозн', 'гудермес', 'дагестан', 'имарат', 'ингуш', 'кабард', 'КБР', 'кадыров', 'карабудах', 'карачаев', 'махачкал', 'назран',
     'нальчик', 'Северн[а-я]{,2} Осет[а-я]{,2}', 'осетия', 'чечен', 'Чечн','хасавюрт','\\bадыг','черкес','Хазбиев','Чиркейск','пятигорск',
     'ставрополь','Северн[а-я]{,3} Кавказ[а-я]{,3}','владикавказ','дербент'),'Северный Кавказ'),
    (('Иран', 'иранск','тегеран','Зариф','КСИР','\\bИРИ\\b','Роухани','\\ирано'),'Иран'),
    (('\\bливан','бейрут', 'насралла','хизбалла'),'Ливан'),(('молдав','кишенев','приднестров','тирасполь','Молдов'),'Молдавия'),
    (('Ирак[^л]','\\bиракск','багдад','мосул','Дияла','Киркук','Тикрит'),'Ирак'),
    (('афган','кандагар','кабул','кундуз'),'Афганистан'), (('пакистан','исламабад','пешавар','техрике'),'Пакистан'),
    (('Астан', 'казах', 'киргиз', 'кыргыз', 'таджик', 'туркмен', 'узбек','душанбе'),'Средняя Азия'),
    (('Сири', 'алеппо', 'дамаск', 'кобани', 'нусра', 'ракк', ' сирийск', 'Сирийск','сирия','башар','Асад','хасика','Пальмир',
      'Латакия','Кунейтр','Хомс[а-я]{,2}','Дараа','Идлеб','\\bХама\\b','\\bХасаке\\b'),'Сирия'),
    (('\\bЛивии', '\\bливию', 'алжир', '\\bливийск', '\\bливия', '\\bтунис','марокк','туарег','мавритан'),'Магриб'),
    (('египет','египт','\\bкаир','синай','синая','синае'),'Египет'),
    (('бахрейн', 'йемен', 'катар', 'кувейт', 'оаэ', 'саудовск','\\bоман'),'арабы ЗПЗ'),
    (('\\bливан','хезболла','бейрут'),'Ливан'),(('\\bинди[^авг]','Дели ','мумбаи'),'Индия'),
    (('иордан','Аман'),'Иордания'),
    (('\\bАТО\\b', 'аваков', 'авдеевк', '\\bАзов\\b', 'алчевск', 'артемовск', 'бэтмен', 'бэтмэн',
      'Верховн[а-я]{,2} Рад[а-я]{,2}', 'винниц', 'волновах', '\\bВСУ\\b', 'горловк', 'гранитно',
      'дебальце', 'днепр', 'днр', 'донбас', 'донетч','закарпат',
      'донецк', 'дружковк', 'житомир', 'за ночь боевики', 'запорож', 'киборг', 'киев', 'краснодон', 'красном луче', 'крым',
      'лнр', 'луганск', 'луганщин', 'львов', 'макеевк', 'мариупол', 'никишино', 'николаев', 'никопол','Новоросси[^й]',
      'одесс', 'одесч', 'ольховатк', 'парубий', 'полтав', 'полторак', 'порошенко', 'правого сектора', 'пушилин', 'СБУ', 'семенченко',
      'славянск', 'снбо', 'старобешево', 'стаханов', 'счасть', 'турчинов', 'тымчук', 'украин', 'укроборон', 'харьков',
      'херсон', 'чернигов', 'черновц', 'яценюк','Весело','шахтерск','захарченко','геращенко','попасн','чермалык','франковск',
      'зона боевых действий','лысенко','ополчен','Изюм','Пески','красногоровк','марьинк','луценко','тернополь','Айдар','ОУН',
      'углегорск','чернухино','лисичанск','докучаевск','Гнутово','Фащевк','краматорск','Ярош','Сартан','Широкино','Басурин',
      'ГПУ','ГПСУ','Саакашвили'),'Украина'),
    (('канад','оттав'),'Канада'),
    (('\\bавстри', '\\bалбан', '\\bангли', '\\bафин', '\\bбалтик', '\\bбелград', '\\bбельг', '\\bберлин', '\\bболгар',
      '\\bвена\\b', '\\bвенгер', '\\bвенгр', '\\bвене ', '\\bгреци', '\\bдании', '\\bдатск', '\\bес\\b', '\\bиспан',
      '\\bитали', '\\bкипр', '\\bкосов[оес]', '\\bлатви', '\\bлитв[аеуы]', '\\bмилан', '\\bнато\\b', '\\bнемец',
      '\\bницц', '\\bпольс', '\\bриг[а-я]{,2}\\b', '\\bрим\\b', '\\bрима\\b', 'soir', 'бридлав', 'британ', 'брюссел',
      'бундес', 'варшав', 'герман', 'голланд', 'греческ', 'европ[^о]', 'евросоюз', 'женев[ае]', 'ирланд', 'исланд',
      'итальян', 'копенгаген', 'лейпциг', 'литовск', 'лондон', 'мадрид', 'македони', 'марсел', 'меркель', 'нидерланд',
      'норвеги', 'норвежск', 'олланд', 'париж', 'польш', 'португал', 'расмуссен', 'румын', 'сааб', 'североатлант',
      'серби', 'скопье', 'словак', 'словен', 'талес', 'финлянд', 'финск', 'франкфурт', 'франц[а-я]{2,}', 'фрг',
      'хорват', 'цюрих', 'черногор', 'чехи', 'чешск', 'швед', 'швейцар', 'швеци', 'эстон','\\bмальт[аеуы]\\b',
      '\\bандор[аеуы]\\b'),'Европа'),
    (('американ', 'вашингтон', 'Обама', 'пентагон', 'США', 'теннесси', 'цру','маккейн','нью-йорк','техас','канзас','керри',
      'госсекретар','калифорн','nasa','огайо','фбр','флорид','АНБ','НАСА','Райс','Байден','госдеп','Lockheed',
      'Локхид Мартин','Рейтеон','Балтимор'),'США'),
    (('китай','китае','китая','китаю','пекин','гонконг','КНР','тайван'),'Китай'),
    (('Корея','Кореи','Корею','кндр','пхеньян','сеул','корейск','Ким Чен'),'Корея'),
    (('япон','токио','Абэ','Синдзо'),'Япония'),
    (('австрал','\\bсидне','мельбурн'),'Австралия'),
    (('бруней', 'вьетнам', 'индонез', 'камбодж', '\\bлаос', 'малайз', 'малазий', 'мьянм', 'сингапур', 'таиланд', '\\bтимор', 'филиппин',
      'бангкок','бангладеш',' тайск','\\bнепал'),'ЮгоВосточная Азия'),
    (('аргентин', 'болив', 'бразил', 'венесуэл', 'колумб', 'мексик', '\\bперу', 'чилий','парагва','уругва','монтевидео','сантьяго',
      ' чилийск', 'Чили','Мехико','карибск','никарагуа','\\bкубинск','Куб[а-я]\\b','эквадор'),'Латинская Америка'),
    (('боко харам', 'бурунди', 'конго', 'либери', 'могадишо', '\\bнигер', 'сомалий', '\\bсудан', 'сьерра-леоне',
      'шабаб','Мали\\b','танзан','камерун','боко-харам','замби','гвине','малийск','африк','\\bкени[яюйи]','сенегал',
      '\\bангол','ЦАР','Бенин','Габон','ЮАР','эфиоп','джибут','\\bБуркина','\\bЧаде\\b','\\bЧада\\b','Сомали'),'Африка'),
    ])

country = "Другие"

def define_country_by_zagolovok(title_a):
    global country
    for k in country_dict1.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(title_a) or p.search(title_a.lower()):
                country = k[1]
                return

def define_country_by_mtext(mtext_a):
    global country
    for k in country_dict1.items():
        for k_word in k[0]:
            p = re.compile(k_word)
            if p.search(mtext_a[:350]) or p.search(mtext_a[:350].lower()):  # Поиск производится примерно в первых двух абзацах (350 знаков) осн текста
                country = k[1]
                mtext_a = mtext_a + '\nРАСПРЕДЕЛЕНО ПО КЛЮЧЕВОМУ СЛОВУ: "{}" В ОСНОВНОМ ТЕКСТЕ.'.format(k_word)
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
    with open('history.txt', 'a') as history_txt:
        history_txt.write(url + ' ' + str(datetime.now()) + '\n')

def create_history_file():
    with open('history.txt', 'w+') as history_txt:
        history_txt.write('0b1100100\n')

