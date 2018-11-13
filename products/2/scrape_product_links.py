import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

with open('./start_page.csv', 'r') as f:
    start_page = int(f.readline())

batch_size=160

product_page_links = []
for i in range(start_page, start_page+batch_size):
    url = "https://cosmeet.cosme.net/product/search/page/{0}/srt/4/itm/1003".format(i)
    response = requests.get(url)
    bsobj = BeautifulSoup(response.content, "lxml")
    product_list = bsobj.find("div", {"id":"cnt-list"})
    for product in product_list.findAll("div", {"class", "info"}):
        product_page_links.append(product.find("a")['href'])
    time.sleep(2)


pd.DataFrame(product_page_links).to_csv('./product_links.csv')
