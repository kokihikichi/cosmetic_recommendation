import sys
sys.path.append('../')
from scraper import *

with open('./pointer.csv', 'r') as f:
    pointer = int(f.readline())

DF_REVIEWS = pd.DataFrame()
df_product_links = pd.read_csv('./product_links.csv', sep=',', names = ["0", "1"])
df_product_links[df_product_links['0'] > pointer].apply(lambda x: create_review_data(x), axis=1)
