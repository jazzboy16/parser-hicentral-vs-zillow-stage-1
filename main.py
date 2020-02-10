# -*- coding: utf-8 -*-
import json
import random
import time

import requests
from bs4 import BeautifulSoup


def parse_hicentral(dump_filename='dump_hicentral.json'):
    """
    Парсер сайта propertysearch.hicentral.com
    Обходит все страницы по очереди с объявлениями,
    затем обходит все объявления и забирает с каждого следующие значения (в скобках указан соответствующий ключ):

    - адрес (address);
    - цена (price);
    - тип недвижимости (property_type);
    - ссылка на объявление (url);
    - List Date (list_date).

    :return: список всех объявлений, каждое объявление - словарь.
    """
    domain = 'https://propertysearch.hicentral.com'
    ad_urls = []

    url = '{}/HBR/ForSale/?/Results/HotSheet//1//'.format(domain)

    page_n = 1
    while True:
        delay = random.uniform(1.0, 3.0)
        print('Задержка: {:.2f} сек.'.format(delay))
        time.sleep(delay)

        print('Парсинг страницы: {}'.format(page_n))
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="html.parser")

        # Собираем ссылки на объявления.
        anchors = soup.select('div.P-Results1 > span > a')
        ad_urls.extend(
            ['{}/HBR/ForSale/{}'.format(domain, a.attrs['href']) for a in anchors]
        )

        # Если есть кнопка «next», то переходим к следующей странице.
        next_btn = soup.find('a', {'id': 'ctl00_main_ctl00_haNextTop'})
        if next_btn:
            url = '{}{}'.format(domain, next_btn.attrs['href'])
            page_n += 1
        # Если нет, то завершаем цикл.
        else:
            break

    print('Парсинг страниц с объявлениями завершен, всего ссылок: {}'.format(len(ad_urls)))
    with open(dump_filename, 'w') as f:
        json.dump(ad_urls, f, ensure_ascii=False, indent=2)
    print('Ссылки сохранены в файл: {}'.format(dump_filename))

    return ad_urls


def main():
    parse_hicentral()


if __name__ == '__main__':
    main()
