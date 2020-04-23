# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import json


url = 'https://yandex.ru/news/export'
r = requests.get(url)
city_list = []
dict_rss = {}
choice = True
if r.status_code == 200 and choice == True:
    soup = BeautifulSoup(r.text, 'html.parser')
    page = soup.find('div', class_='tabs-panes__pane tabs-panes__pane_name_regions-russia '
                                   'tabs-panes__pane_active_yes export__select-pane')
    a = page.find_all('a', class_='link link_theme_normal i-bem')
    for i in a:
        href = i.get('href')
        title_region = i.text
        cities_translit = href[23:-10]
        path_to_gecko = os.getcwd() + '/geckodriver'
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(executable_path=path_to_gecko, firefox_options=options)
        driver.get('http://translit-online.ru/perevod-s-translita-na-russkij.html')
        input_words = driver.find_element_by_name("in")
        input_words.clear()
        input_words.send_keys(cities_translit)
        click_button = driver.find_element_by_name('translate').click()
        out = driver.find_element_by_id('out').text
        try:
            y_speller = 'https://speller.yandex.net/services/spellservice.json/checkText?text=' + out
            r2 = requests.get(y_speller).text
            normal_city = json.loads(r2)[0]['s'][0]
            if normal_city == []:
                dict_rss.fromkeys([out])
                dict_rss[out] = href
                city_list.append(out)
            elif normal_city == 'Саинт-ПетерсбургандЛенинградОбласт':
                normal_city = 'Санкт-Петербург и Ленинградская область'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Мосцов':
                normal_city = 'Москва'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'МосцовандМосцовОбласт':
                normal_city = 'Москва и Московская область'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Горно-Алтаыск':
                normal_city = 'Горно-Алтайск'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Улан-Уде':
                normal_city = 'Улан-Удэ'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'РепублицофИнгушетиа':
                normal_city = 'Республика Ингушетия'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'РепублицофЦримеа':
                normal_city = 'Республика Крым'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Ёшкар-Ола':
                normal_city = 'Йошкар-Ола'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Казан':
                normal_city = 'Казань'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'СаинтПетерсбург':
                normal_city = 'Санкт-Петербург'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Твер':
                normal_city = 'Тверь'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            elif normal_city == 'Ханты-Мансиыск':
                normal_city = 'Ханты-Мансийск'
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
            else:
                dict_rss.fromkeys([normal_city])
                dict_rss[normal_city] = href
                city_list.append(normal_city)
        except:
            pass
        driver.close()

with open('dict_rss.txt', 'w') as file:
    file.write(dict_rss)

with open('city_list.txt', 'w') as file:
    file.write(city_list)