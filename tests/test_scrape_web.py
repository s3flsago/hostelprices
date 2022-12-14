import unittest

import sys
import git
import os
import json

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from hostelprices.utils import Utils

from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np



class Test(unittest.TestCase):

    def test_load_soup(self):
        url = 'http://www.google.com/'
        soup = ScrapeWeb.loadSoup(url)

        string = soup.find('html').get_text()
        assert('Google' in string)
    
    
    def test_create_url(sef):
        from datetime import datetime

        city = 'Lisbon'
        date_from = datetime(2023, 1, 5)
        duration = 2
        page = 1

        url = ScrapeWeb.createUrl(city=city, date_from=date_from, duration=duration, page=page)

        soup = ScrapeWeb.loadSoup(url)

        string = soup.find('html').get_text()
        assert('hostel' in string)


    def test_extract_data(self):
        city = 'Lisbon'
        date_from = datetime(2023, 1, 5)
        duration = 2
        page = 1

        url = ScrapeWeb.createUrl(city=city, date_from=date_from, duration=duration, page=page)
        soup = ScrapeWeb.loadSoup(url)
        df = ScrapeWeb.extractData(soup)

        assert(list(df.columns)==['price (EUR)', 'rating', 'distance (km)'])
        assert(len(df)>3)
        assert(np.median(df["price (EUR)"])>10)
        assert(np.median(df["rating"])>4)
        assert(np.median(df["rating"])>4)
        
    
    def test_loop(self):
        city_list = ['Lisbon', 'Seville']
        date_from_list = [datetime(2023, 1, 5), datetime(2023, 4, 1)]
        duration_list = [2, 5]
        max_pages = 2

        df = ScrapeWeb.loop(
            city_list=city_list, date_from_list=date_from_list, duration_list=duration_list, 
            max_pages=max_pages
            )
        
        assert(
            list(df.columns)==[
                'price (EUR)', 'rating', 'distance (km)', 'city', 'date_from', 'duration (days)',
                'request_time'
                ]
                )
        assert len(df)>3
        assert np.median(df["price (EUR)"])>10
        assert np.median(df["rating"])>4
        assert np.median(df["rating"])>4
        

    def test_check_price_eur(self):

        usd_card_split_path = os.path.join(Utils.testFixturesPath(), 'card_split_usd.json')
        with open(usd_card_split_path) as fp:
            card_split_dict = json.load(fp)

        card_split_usd = card_split_dict["card_split"] 
        price_usd = card_split_dict["price_usd"]

        price_eur_true = ScrapeWeb.euro(price_usd)
        price_eur = ScrapeWeb.priceEur(card_split_usd)

        assert(price_eur_true==price_eur)

        
        

if __name__ == '__main__':

    unittest.main(price_eur_true, price_eur)