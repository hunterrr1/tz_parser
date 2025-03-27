import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
import logging
import xmltodict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
soup = BeautifulSoup(html, 'html.parser')


async def main():
    base_ozon_url = 'https://www.ozon.ru/category/obuv-dlya-malchikov-7685/?page='
    base_wb_url = 'https://www.wildberries.ru/catalog/obuv/detskaya/dlya-malchikov?sort=popular&page='
    base_auchan_url = 'https://www.auchan.ru/catalog/syry/syry-ashan/?page='
    price_auchan = {'div': 'styles_price__U1y_f typography_h3__AujKn styles_productCardContentPanel_price__MqlWB'}
    old_price_auchan = {'div': 'styles_price__U1y_f styles_price__oldPrice__VsVTT styles_productCardContentPanel_oldPrice__TYk2W'}
    atributes_auchan = {'a': 'styles_productCardContentPanel_link__6vQup styles_link__VBOJI typography_body__83w8q',
                        'p': 'styles_productCardContentPanel_name__072Y7'}
    atributes_wb = {'a': 'product-card__link j-card-link j-open-full-product-card', 'name': 'aria-label'}
    price_wb = soup.select_one('ins.price__lower-price')
    old_price_wb = soup.find('del')
    price_wb_f = re.sub(r'\D', '', price_wb.text) if price_wb else None
    old_price_wb_f = re.sub(r'\D', '', old_price_wb.text) if old_price_wb else None
    ostatok_ozon = div_tag = soup.find('div', class_='b223-b0 tsBodyControl400Small')
    ozon_price = soup.find('span', class_='c3025-a1 tsHeadline500Medium c3025-b1 c3025-a6')
    old_ozon_price = soup.find('span', class_='c3025-a1 tsBodyControl400Small c3025-b c3025-a6')
    ozon_price_f = re.sub(r'\D', '', ozon_price.text) if ozon_price else None
    old_ozon_price_f = re.sub(r'\D', '', old_ozon_price.text) if old_ozon_price else None
    ozon = soup.select_one('a.q4b011-a.tile-clickable-element.jn3_25')
    url_ozon_product = ozon['href']
    ozon_name_tag = ozon.select_one('span.tsBody500Medium')
    name_ozon_product = ozon_name_tag.text
    tasks = []
    for num in range(1, 4):
        tasks.append(base_auchan_url + str(num))
        tasks.append(base_ozon_url + str(num))
        tasks.append(base_wb_url + str(num))


