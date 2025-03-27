import asyncio
import re
import aiohttp
from bs4 import BeautifulSoup
import logging
import xmltodict

from parser.src.celery_app import celery

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

data = {}


async def wb(session, url):
    response = await session.get(url)
    result = await response.text()
    soup = BeautifulSoup(result, 'html.parser')
    atributes_wb = soup.find('a', class_='product-card__link j-card-link j-open-full-product-card')
    wb_url = atributes_wb['href']
    product_wb = atributes_wb['aria-label']
    price_wb_html = soup.select_one('ins.price__lower-price')
    old_price_wb_html = soup.find('del')
    price_wb = re.sub(r'\D', '', price_wb_html.text) if price_wb_html else None
    old_price_wb = re.sub(r'\D', '', old_price_wb_html.text) if old_price_wb_html else price_wb
    data['wb'][f'{product_wb}'] = {
        'price': price_wb,
        'old_price': old_price_wb,
        'name': product_wb,
        'link': wb_url
    }

async def ozon(session, url):
    response = await session.get(url)
    result = await response.text()
    soup = BeautifulSoup(result, 'html.parser')
    remaining_ozon = soup.find('div', class_='b223-b0 tsBodyControl400Small')
    ozon_price_html = soup.find('span', class_='c3025-a1 tsHeadline500Medium c3025-b1 c3025-a6')
    old_ozon_price_html = soup.find('span', class_='c3025-a1 tsBodyControl400Small c3025-b c3025-a6')
    ozon_price = re.sub(r'\D', '', ozon_price_html.text) if ozon_price_html else None
    old_ozon_price = re.sub(r'\D', '', old_ozon_price_html.text) if old_ozon_price_html else ozon_price
    atributes_ozon = soup.select_one('a.q4b011-a.tile-clickable-element.jn3_25')
    ozon_url = atributes_ozon['href']
    ozon_name_tag = atributes_ozon.select_one('span.tsBody500Medium')
    product_ozon = ozon_name_tag.text
    data['ozon'][f'{product_ozon}'] = {
        'price': ozon_price,
        'old_price': old_ozon_price,
        'name': product_ozon,
        'link': ozon_url,
        'remaining': remaining_ozon if remaining_ozon else None
    }

async def auchan(session, url):
    response = await session.get(url)
    result = await response.text()
    soup = BeautifulSoup(result, 'html.parser')
    price_auchan = soup.find('div', class_='styles_price__U1y_f typography_h3__AujKn styles_productCardContentPanel_price__MqlWB')
    old_price_auchan = soup.find('div', class_='styles_price__U1y_f styles_price__oldPrice__VsVTT styles_productCardContentPanel_oldPrice__TYk2W')
    atributes_auchan = soup.find('a', class_='styles_productCardContentPanel_link__6vQup styles_link__VBOJI typography_body__83w8q')
    auchan_url = atributes_auchan['href']
    product_auchan = atributes_auchan['title']
    data['auchan'][f'{product_auchan}'] = {
        'price': price_auchan,
        'old_price': old_price_auchan if old_price_auchan else price_auchan,
        'name': product_auchan,
        'link': auchan_url
    }


@celery.task(name='main.get_data')
async def get_data():
    base_ozon_url = 'https://www.ozon.ru/category/obuv-dlya-malchikov-7685/?page='
    base_wb_url = 'https://www.wildberries.ru/catalog/obuv/detskaya/dlya-malchikov?sort=popular&page='
    base_auchan_url = 'https://www.auchan.ru/catalog/syry/syry-ashan/?page='
    tasks = []
    async with aiohttp.ClientSession as session:
        for num in range(1, 4):
            tasks.append(auchan(session, base_auchan_url + str(num)))
            tasks.append(ozon(session, base_ozon_url + str(num)))
            tasks.append(wb(session, base_wb_url + str(num)))
    await asyncio.gather(*tasks)

