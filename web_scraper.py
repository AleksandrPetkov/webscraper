import csv
import sys

from bs4 import BeautifulSoup
import requests

URL = 'https://bi.ua/ukr/dlya-malishey/razvivayuschie-igrushki/'
FILE = 'catalog.csv'
HOST = 'https://bi.ua'


def get_html(url, params=None):
    result = requests.get(url, params=params)

    return result


def get_last_page_num(html):
    html_code = BeautifulSoup(html.text, features='html.parser')
    last_page_req = html_code.findAll(name='a', class_="pagLast pagLink")
    last_page_number = [e.text for e in last_page_req][0]
    return last_page_number


def get_goods_href(html_code):
    goods_hrefs = []
    goods_href_data = html_code.findAll(name='a', class_="goodsItemLink")
    for h_data in goods_href_data:
        href = h_data.get('href')
        goods_hrefs.append(href)
    return goods_hrefs


def get_goods_names(html_code):
    goods_names = []
    goods_name_data = html_code.findAll(name='span', class_="itemDes")
    for n_data in goods_name_data:
        name = n_data.text
        goods_names.append(name)
    return goods_names


def get_goods_price(html_code):
    goods_price = []
    goods_price_data = html_code.findAll(name='p', class_="costIco")
    for p_data in goods_price_data:
        price = p_data.text
        goods_price.append(price)
    return goods_price


def get_goods_availability(html_code):
    goods_available = []
    goods_available_data = html_code.findAll(name='div', class_="goodsItemHover")
    for a_data in goods_available_data:
        availability = a_data.text
        goods_available.append(availability)
    return goods_available


def data_cleaning(*args):
    hrefs, prices, availability, host = args

    hrefs_c = [host + href for href in hrefs]

    prices_c = []
    price_split = ''
    for price in prices:
        if price == '':
            prices_c.append(0)
        else:
            for elem in price.split():
                if elem.isnumeric():
                    price_split += str(elem)
            if price_split == '':
                prices_c.append(0)
            else:
                prices_c.append(int(price_split))
            price_split = ''

    availability_c = [avail.strip('\n,\r, ') for avail in availability]

    return hrefs_c, prices_c, availability_c


def get_available_goods(*args):
    links, price, name, availability = args
    available_goods = []
    for item in zip(links, name, price, availability):
        if item[-1] == 'Купити':
            available_goods.append(item)
    return available_goods


def write_csv(available_goods, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Link', 'Name', 'Price', 'Avalability'])
        for item in available_goods:
            writer.writerow(item)


def get_average_price(goods_available):
    prices = [item[2] for item in goods_available]
    value_of_goods = len(prices)
    average_price = sum(prices) / value_of_goods
    return average_price


def get_cheapest_good(available_goods):
    available_goods.sort(key=lambda x: x[-2])
    result = []
    first_good_price = available_goods[0][-2]
    prices_list = [e[-2] for e in available_goods]
    while first_good_price in prices_list:
        count = 0
        result.append(available_goods[count])
        prices_list.pop(0)
        count += 1
    return result


def get_cheapest_good_view(data):
    print('2. The most cheapest goods are:\n')
    for elem in data:
        link, name, price, _ = elem
        print(f'Web-site link: {link}\n'
              f'Name: {name}\n'
              f'Price: {price} UAH\n\n')


def main():
    try:
        html = get_html(URL)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    hrefs = []
    names = []
    prices = []
    availability = []



    page_n = get_last_page_num(html)

    for page in range(1, int(page_n)+1):  # int(page_n)+1
        try:
            html_page = get_html(URL, params={'page': page})
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        html_code = BeautifulSoup(html_page.text, features='html.parser')
        hrefs += get_goods_href(html_code)
        names += get_goods_names(html_code)
        prices += get_goods_price(html_code)
        availability += get_goods_availability(html_code)

    hrefs_c, prices_c, availability_c = data_cleaning(hrefs, prices, availability, HOST)
    available_goods = get_available_goods(hrefs_c, prices_c, names, availability_c)
    average_price = get_average_price(available_goods)

    print(f'1. The average price of {len(available_goods)} goods is {round(average_price, 2)} UAH')

    cheapest_good_data = get_cheapest_good(available_goods)
    get_cheapest_good_view(cheapest_good_data)

    write_csv(available_goods, FILE)
    print(f'3. The CSV-file save successful. {len(available_goods)} goods have recorded to the file.')
    sys.exit()


if __name__ == '__main__':
    main()
