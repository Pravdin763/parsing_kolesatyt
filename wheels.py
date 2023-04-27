import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import json
from downloadimage import downloadim

for count in range(1, 64):
    print(f'парвинг {count} страницы')
    url = f'https://tolyatti.kolesatyt.ru/podbor/shiny/?PAGEN_1={count}'
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')


    r = soup.find_all('a', class_="txt-big link-dark font-weight-bold stretched-link")
    r1 = soup.find_all('div', class_="cat-item-img mb-4 pos-rel")
    r2 = soup.find_all('div', class_="txt-bigger w-100 price")

    def price_funk():       # выводит прайс
        for j in r2:
            sleep(1)
            price = j.text
            yield price

    def images_razmer():        # выводит картинку и размерность шин
        for i in r1:
            sleep(1)
            images = 'https:' + i.find(class_="d-block mx-auto product-list-image").get('src')
            razmer = ' '.join(i.find(class_="d-block mx-auto product-list-image").get('alt').split()[2:-3])
            yield  images, razmer

    def name_url():     # название и сама ссылка на карту, стоило брать инфу оттуда....
        for ii in r:
            sleep(random.randint(1, 2))
            name = ' '.join(ii.find('span').text.split()[1:])          # список названий
            url_card = 'https://tolyatti.kolesatyt.ru' + ii.get('href')      # ссылка на каталог
            yield  name, url_card


    def description(x):     # описание из карточки товара
        sleep(1)
        req = requests.get(x, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        res = soup.find(class_="table table-bordered table-striped")
        description = res.text.split()
        yield from description

    res = {}        #   Итоговый словарь, он будет записан в json

    for i, j, u in zip(name_url(), price_funk(), images_razmer()):  # общая функция, итерация по 3 генераторам
        sleep(random.randint(1, 2))
        d = {
            'url_card': i[1],
            'price': j,
            'images': u[0],
            'размерность': u[1],
            'discription': list(description(i[1]))
        }
        downloadim(u[0])            #   вызывает функцию скачивания картинок ! из файла downloadimage
        res[i[0]] = d           # ключ - имя, значение - словарь d (все остальное)
        with open('all_file.json', 'w', encoding='utf-8') as file:      #   запись в json
            json.dump(res, file, ensure_ascii=False, indent=4)


    print(f'парсинг завершен, осталось {63-count} страниц')





