import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

url = 'https://yandex.ru/news/export'
r = requests.get(url)
city_list = []
if r.status_code == 200:
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
        city_list.append(out)
        print('Добавлен ', out)
        driver.close()

print(city_list)