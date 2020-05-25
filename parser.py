import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.avito.ru/novorossiysk?q=листовки'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.2.201 Yowser/2.5 Yptp/1.23 Safari/537.36'}
HOST = 'https://www.avito.ru'
FILE = 'works.csv'


def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('span', class_ = 'pagination-item-1WyVp')
    return len(pages) // 2

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div',  class_ = 'item_table-wrapper')

    
    works = []
    for item in items:
        works.append({
            'title' : item.find('div', class_= 'snippet-title-row').get_text(strip = True),
            'link' : HOST + item.find('a', class_= 'snippet-link').get('href'),
            'price' : item.find('div', class_= 'snippet-price-row').get_text(strip = True),
        })

    return works

def save_file(items, path):
    with open(path, 'w', newline = '', encoding = 'utf8') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Вакансия', 'Ссылка', 'З/п'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])
        

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        works = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}')
            html = get_html(URL, params = {'page' : page})
            works.extend(get_content(html.text))
        save_file(works, FILE)

        print(f'Полученно {len(works)} различных вакансий.')
    
    else:
        print('Error')



parse()
