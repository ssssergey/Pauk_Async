#!/usr/bin/python3
# -*- coding: utf-8 -*-
import collections
from datetime import date
import os
import time

os_all = ['Windows','Linux']
os_current = os_all[0]

# paths
log_file = 'Debugging.log'
keyword_file = 'keywords_militar.txt'
history_file = 'history.txt'
bucket_file = 'bucket.txt'
icon_file = 'Icon.ico'
db_file = 'pauk_db.db'
if os_current == 'Linux':
    basedir = os.path.abspath(os.path.dirname(__file__))
    log_file = os.path.join(basedir,'Debugging.log')
    keyword_file = os.path.join(basedir,'keywords_militar.txt')
    history_file = os.path.join(basedir,'history.txt')
    bucket_file = os.path.join(basedir,'bucket.txt')
    icon_file = os.path.join(basedir,'Icon.ico')
    db_file = os.path.join(basedir,'pauk_db.db')

output_folder = 'c:\\от Паука\\'

text_size_limit = 5000

expire_date = date(2016,2,1) # Date of the program license expiration

version = '3.4'

import logging
if os_current == 'Linux':
    logging.Formatter.converter = time.gmtime

logger = logging.getLogger('logger')
handler = logging.FileHandler(log_file, encoding='utf8')
handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger_bucket = logging.getLogger('logger_bucket')
handler1 = logging.FileHandler(bucket_file, encoding='utf8')
handler1.setLevel(logging.INFO)
formatter1 = logging.Formatter('[%(asctime)s] | %(message)s')
handler1.setFormatter(formatter1)
logger_bucket.addHandler(handler1)

logger_history = logging.getLogger('logger_history')
handler2 = logging.FileHandler(history_file, encoding='utf8')
handler2.setLevel(logging.INFO)
formatter2 = logging.Formatter('[%(asctime)s] | %(message)s')
handler2.setFormatter(formatter2)
logger_history.addHandler(handler2)

rss_dict = {'http://www.vedomosti.ru/newsline/out/rss.xml':'Ведомости',
        'http://apsny.ge/RSS.xml':'Грузия-онлайн',
        'http://itar-tass.com/rss/v2.xml':'ИТАР-ТАСС',
        'http://www.kavkaz-uzel.ru/articles.rss/':'Кавказский узел',
        'http://www.kommersant.ru/RSS/news.xml':'Коммерсант',
        'http://lenta.ru/rss':'Лента.ру',
        'http://www.mignews.com/export/mig_export3.html':'МигНьюс',
        'http://www.blackseanews.net/allnews/georgia.rss':'BlackSeaNews',
        'http://feeds.feedburner.com/rosbalt?format=xml':'Росбалт',
        'http://www.trend.az/feeds/index.rss':'Тренд',
        'http://www.armstrade.org/export/news.xml':'ЦАМТО',
        'http://www.bbc.co.uk/russian/index.xml':'Би-Би-Си',
        'http://www.rbc.ua/static/rss/newsline.rus.rss.xml':'РБК-Украина',
        'http://www.ukrinform.ru/rss/':'Укринформ',
        'http://rian.com.ua/export/rss2/politics/index.xml':'РИА-Новости',
        'http://rss.unian.net/site/news_rus.rss':'УНИАН',
        'http://k.img.com.ua/rss/ru/ukraine.xml':'Корреспондент',
        'http://vpk-news.ru/feed':'ВПК',
        'http://www.news-asia.ru/rss/all':'News-Asia',
        'http://www.fergananews.com/rss.php':'Фергана',
        'http://ru.apa.az/rss':'APA.AZ',
        'http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss':'РБК',
        'http://newsgeorgia.ru/export/rss2/index.xml':'Спутник',
        'http://irna.ir//ru/rss.aspx?kind=701':'ИРНА',
        'http://russian.rt.com/rss/':'RussiaToday',
        'http://www.apsnypress.info/news/rss/':'Апсны-Пресс',
        'http://sana.sy/ru/?feed=rss2':'САНА',
        'http://ria.ru/export/rss2/world/index.xml':'РИА Новости',
        'http://dan-news.info/feed':'ДАН',
        }

rss_func_dict = {'Лента.ру':'lenta', 'Кавказский узел':'kavuzel', 'Тренд':'trend', 'ВПК':'vpk', 'News-Asia':'news_asia',
                 'МигНьюс':'mignews', 'Коммерсант':'kommersant', 'Ведомости':'vedomosti', 'Фергана':'fergana',
                 'Грузия-онлайн':'georgiaonline', 'BlackSeaNews':'blacksea', 'ЦАМТО':'camto', 'ИТАР-ТАСС':'itartass',
                 'Росбалт':'rosbalt', 'Би-Би-Си':'bbc', 'РБК-Украина':'rbc_ukr', 'Укринформ':'ukrinform', 'РИА-Новости':'rian',
                 'УНИАН':'unian', 'Корреспондент':'korrespondent','РБК':'rbc_rus','APA.AZ':'apa_az','Спутник':'newsgeorgia',
                 'ИРНА':'irna','RussiaToday':'rustoday','Апсны-Пресс':'apsnypress','САНА':'sana','РИА Новости':'rianovosti',
                 'ДАН':'dan'}

stop_words = ['бокс[её]р','хоккеист','Бессмертн','зв[её]здны[а-я]{,2} войн','\\bВойнов','\\bПутин',
              'велик[а-я]{2} отечествен','втор[а-я]{2} миров','Война и мир','Лавров','Песков','Захарова','МО РФ:',
              'Минобороны РФ:','МИД РФ']

country_filter = collections.OrderedDict([
    (('азербайдж','Баку(?!\s*\-\s*АПА\.)','карабах','армян','ереван','Армени','бакинск','нахчыван','Агдаш','\\bНардаран'),'Азербайджан'),
    (('Абхази', 'вазиани', 'Гальск', '(?!Новости\-)Грузи[а-я]', 'грузин', 'кутаиси', 'сенаки', 'сухуми', 'тбилиси[^,]',
      'цхинвали','джавахет','чахалян','Поти','\\bбатум','Аласан','Южн[а-я]{,2} Осет[а-я]{,2}','Маргвелашвили',
      'Гарибашвили','Хидашели','Усупашвили'),'Грузия'),
    (('анкар', '\\bРПК[^А-Я]', 'стамбул', 'турецк', 'турц','Аселсан','Отокар','Эрдоган'),'Турция'),
    (('IAI', '\\bГаз[аы]\\b', 'Ганц', 'Голанах', 'Голанск', 'Голаны', 'Гуш-Эцион', 'Машаль', 'Халхуль',
      'Яалон', 'беэр-шев', 'железный купол', 'иерусалим', 'израил', 'иуде[яи]', 'кнессет', 'либерман', 'магав',
      'нетаниягу', 'палестин', 'рахат', 'самари', 'сектор[а-я]{,3} газа', 'тель-авив', 'хайф', 'хамас', 'хеврон',
      'цахал', 'шабак'),'Израиль'),
    (('Грозн', 'гудермес', 'дагестан', 'имарат', 'ингуш', 'кабард', 'КБР', 'кадыров', 'карабудах', 'карачаев', 'махачкал', 'назран',
     'нальчик', 'Северн[а-я]{,2} Осет[а-я]{,2}', 'осетия', 'чечен', 'Чечн','хасавюрт','\\bадыг','черкес','Хазбиев','Чиркейск','пятигорск',
     'ставрополь','Северн[а-я]{,3} Кавказ[а-я]{,3}','владикавказ','дербент'),'Северный Кавказ'),
    (('Иран', 'иранск','тегеран','Зариф','КСИР','\\bИРИ\\b','Роухани','\\ирано'),'Иран'),
    (('\\bливан','бейрут', 'насралла','хизбалла'),'Ливан'),(('молдав','кишенев','приднестров','тирасполь','Молдов'),'Молдавия'),
    (('Ирак[^л]','\\bиракск','багдад','мосул','Дияла','Киркук','Тикрит','Рамади\\b','\\bАнбар\\b'),'Ирак'),
    (('афган','кандагар','кабул','кундуз'),'Афганистан'), (('пакистан','исламабад','пешавар','техрике'),'Пакистан'),
    (('Астан', '\\bказах', 'киргиз', 'кыргыз', 'таджик', 'туркмен', 'узбек','душанбе'),'Средняя Азия'),
    (('\\bсири', 'алеппо', 'дамаск', 'кобани', 'нусра', 'ракк', 'башар','Асад','хасика','Пальмир','Дейр[ -]эз-Зор',
      'Латаки','Кунейтр','Хомс[а-я]{,2}','Дараа','Идлеб','\\bХама\\b','\\bХасаке\\b','Хмеймим','\\bСАР\\b','Камышли'),'Сирия'),
    (('\\bЛивии', '\\bливию', 'алжир', '\\bливийск', '\\bливия', '\\bтунис','марокк','туарег','мавритан'),'Магриб'),
    (('египет','египт','\\bкаир','синай','синая','синае','Шарм-эль-Шейх'),'Египет'),
    (('бахрейн', 'йемен', 'катар', 'кувейт', 'оаэ', 'саудовск','\\bоман','эр-рияд'),'арабы ЗПЗ'),
    (('\\bливан','хезболла','бейрут'),'Ливан'),(('\\bинди[^авг]','Дели ','мумбаи'),'Индия'),
    (('иордан','\\bАмман'),'Иордания'),
    (('\\bАТО\\b', 'аваков', 'авдеевк', '\\bАзов\\b', 'алчевск', 'артемовск', 'бэтмен', 'бэтмэн',
      'Верховн[а-я]{,2} Рад[а-я]{,2}', 'винниц', 'волновах', '\\bВСУ\\b', 'горловк', 'гранитно',
      'дебальце', 'днепр', 'днр', 'донбас', 'донетч','закарпат',
      'донецк', 'дружковк', 'житомир', 'за ночь боевики', 'запорож', 'киборг', 'киев', 'краснодон', 'красном луче', 'крым',
      'лнр', 'луганск', 'луганщин', 'львов', 'макеевк', 'мариупол', 'никишино', 'николаев', 'никопол','Новоросси[^й]',
      'одесс', 'одесч', 'ольховатк', 'парубий', 'полтав', 'полторак', 'порошенко', 'правого сектора', 'пушилин', 'СБУ', 'семенченко',
      'славянск', 'снбо', 'старобешево', 'стаханов', 'счасть', 'турчинов', 'тымчук', 'украин', 'укроборон', 'харьков',
      'херсон', 'чернигов', 'черновц', 'яценюк','Весело','шахтерск','захарченко','геращенко','попасн','чермалык','франковск',
      'зона боевых действий','лысенко','Изюм','Пески','красногоровк','марьинк','луценко','тернополь','Айдар','ОУН',
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
      'серби', 'скопье', 'словак', 'словен', 'стокгольм', 'талес', 'финлянд', 'финск', 'франкфурт', 'франц[а-я]{2,}', 'фрг',
      'хорват', 'цюрих', 'черногор', 'чехи', 'чешск', 'швед', 'швейцар', 'швеци', 'эстон','\\bмальт[аеуы]\\b',
      '\\bандор[аеуы]\\b','Кэмерон'),'Европа'),
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