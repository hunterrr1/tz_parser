base_ozon_url = 'https://www.ozon.ru/category/obuv-dlya-malchikov-7685/?page='
base_wb_url = 'https://www.wildberries.ru/catalog/obuv/detskaya/dlya-malchikov?sort=popular&page='
base_auchan_url = 'https://www.auchan.ru/catalog/syry/syry-ashan/?page='
tasks = []
for num in range(1, 4):
    tasks.append(base_auchan_url + str(num))
    tasks.append(base_ozon_url + str(num))
    tasks.append(base_wb_url + str(num))
print(tasks)
