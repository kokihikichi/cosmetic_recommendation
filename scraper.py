import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_review_info(url_review, bsobj):
    global DF_REVIEWS

    reviews = bsobj.findAll("div", {"class": "review-sec"})
    for review in reviews:
        try:
            record = []
            reviewer_info = review.find("div", {"class": "reviewer-info"})
            reviewer_url = reviewer_info.find("a")["href"]

            reviewer_id = re.search('(?<=user_id/)[0-9]+', reviewer_url, re.IGNORECASE).group(0)
            product_id = re.search('(?<=product_id/)[0-9]+', url_review, re.IGNORECASE).group(0)

            reviewer_body = review.find("div", {"class": "body"})
            reviewer_foot = review.find("div", {"class": "foot clearfix"})
            reviewer_name = reviewer_info.find("span", {"class": "reviewer-name"}).get_text()
            reviewer_info = reviewer_info.find("ul").findAll("li")
            reviewer_score = reviewer_body.find("p", {"class": re.compile("reviewer-rating.*")}).get_text()
            reviewer_tags = reviewer_body.find("div", {"class": "tag-list clearfix"})
            DF_REVIEWS = DF_REVIEWS.append(pd.DataFrame([[product_id, reviewer_id, reviewer_info, reviewer_score, reviewer_tags]]))
        except:
            print('error@{0}'.format(url_review))

def create_review_data(row):
    global DF_REVIEWS
    try:
        DF_REVIEWS = pd.DataFrame()
        url_num = row[0]
        print(url_num)
        url = row[1]
        product_id = re.search('(?<=product_id/)[0-9]+', url, re.IGNORECASE).group(0)
        url_review = 'https://www.cosme.net/product/product_id/{product_id}/reviews/'.format(
            product_id=product_id)

        print(url_review)
        response = requests.get(url_review)
        bsobj = BeautifulSoup(response.content, "lxml")
        if bsobj.find("ul", {"class":"number"}):
            max_page_num = int(bsobj.find("ul", {"class":"number"}).findAll("li")[-1].get_text()) + 1
        else:
            max_page_num = 1

        for review_page in range(0, max_page_num):
            url_review = 'https://www.cosme.net/product/product_id/{product_id}/reviews/p/{rev_page}'.format(
                product_id=product_id,
                rev_page=review_page)
            response = requests.get(url_review)
            bsobj = BeautifulSoup(response.content, "lxml")
            print('-{0}'.format(url_review))
            get_review_info(url_review, bsobj)
            time.sleep(2)
        with open('reviews.csv', 'a+') as f:
            f.write(DF_REVIEWS.to_csv(sep='\t', header=False))
        with open('pointer.csv', 'w+') as f:
            f.write(str(url_num))
    except:
        print('error@{0}'.format(url_review))