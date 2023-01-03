import os

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import logging

from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from hostelprices.utils import Utils, Defs

class SearchParameters():

    def __init__(
        self, mode='custom',
        city_list=None, date_from_list=None, duration_list=None, max_pages=None
        ):

        self.mode = mode

        if mode=='custom':
            self.city_list = city_list
            self.date_from_list = date_from_list
            self.duration_list = duration_list
            self.max_pages = max_pages

        elif mode=='debug':
            self.city_list = ['Lisbon']
            self.date_from_list = [datetime(2023, 2, 13)]
            self.duration_list = [2]
            self.max_pages = 1
        
        elif mode=='op':
            self.city_list = ['Lisbon', 'Seville']
            self.date_from_list = [datetime(2023, 1, 13), datetime(2023, 1, 17)]
            self.duration_list = [1, 5]
            self.max_pages = 3
        
        elif mode=='longterm':
            self.city_list = ['Lisbon', 'Seville']
            self.date_from_list = [datetime.today() + timedelta(days=x) for x in range(1,20)]
            self.duration_list = [1, 5]
            self.max_pages = 3
        
        elif mode=='random':
            pass




class ScrapeWeb():

    def __init__(self):
        return
    
   
    @staticmethod
    def euro(price_usd):
        """Transform USD to EUR"""
        rate = CurrencyRates().get_rate('USD', 'EUR')
        price_eur = price_usd * rate
        return price_eur


    @classmethod
    def loadSoup(cls, url):
        options = Options()
        options.headless = True

        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            os.system(f'export GH_TOKEN = "{github_token}"')

        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=options,
            )

        driver.get(url)  

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        return soup
    

    @classmethod
    def convertToEur(cls, entry):
        if '$' in entry:
            currency_str = '$'
            entry = entry.replace('US$', currency_str, 3)

            entry_split = entry.split(currency_str)
            entry_split_eur = []
            for sub_entry in entry_split:
                if sub_entry.isdigit():
                    sub_entry = float(sub_entry)
                    if currency_str=='$':
                        sub_entry = cls.euro(sub_entry)
                    sub_entry = '€' + str(sub_entry)

                entry_split_eur.append(sub_entry)
            
            entry_new = ''.join(entry_split_eur)
        
        else:
            entry_new = entry
        
        return entry_new


    @classmethod
    def correct(cls, card_split, currency_str='€'):
        split_new = []
        for entry in card_split:
            entry = cls.convertToEur(entry)
            
            if 'Dorms' in entry: # if discount, then it could be e.g. '-5%Dorms'
                split_new.append('Dorms')
            elif 'From' in entry: # if discount, then it could be e.g. '-From€21€20'
                split_new.append('From')

                entry_split = entry.split(currency_str)

                if Utils.canBeFloat(entry_split[-1]):
                    split_new.append(f'{currency_str}{entry_split[-1]}')
            else:
                split_new.append(entry)

        return split_new


    @classmethod
    def priceEur(cls, card_split, currency='EUR'):
        ind_dorms = card_split.index('Dorms')
        ind_price = ind_dorms + 2

        price_string = card_split[ind_price]
        if Utils.canBeFloat(price_string[1:]):
            price = float(price_string[1:])
        else:
            price = 'np.nan'

        return price


    @classmethod
    def extractData(cls, soup):

        cards_raw = soup.find_all(class_=['property-card'])

        dorm_prices = []
        ratings = []
        distances= []

        for card in cards_raw:
            if 'Dorms From' in card.get_text():

                card_split = card.get_text().split()
                card_split = cls.correct(card_split)
                
                price_EUR = cls.priceEur(card_split)

                rating = np.nan
                distance = np.nan
                for string in card_split:
                    try:
                        if (float(string)<=10) and (float(string)>=0):
                            rating = float(string)
                    except:
                        pass
                        
                    if 'km' in string:
                        distance = float(string[:-2])

                dorm_prices.append(price_EUR)
                ratings.append(rating)
                distances.append(distance)
            else:
                dorm_prices.append(np.nan)
                ratings.append(np.nan)
                distances.append(np.nan)
        
        df = pd.DataFrame(
            {
                Defs.colName('price'): dorm_prices, 
                Defs.colName('rating'): ratings, 
                Defs.colName('distance'): distances
                }
            )
        df = df.dropna(axis=0)
        
        return df


    @classmethod
    def createUrl(
        cls, country=None, city=None, date_from=None, date_to=None, duration=None, page=None
        ):
        if city=='Lisbon':
            country = 'Portugal'
            id = '725'
        elif city=='Seville':
            country = 'Spain'
            id = '1565'

        if not date_to:
            date_to = date_from + timedelta(days=duration)

        date_from = Utils.formatDate(date_from)
        date_to = Utils.formatDate(date_to)
        url = (
            f'https://www.hostelworld.com/s?q={city},%20{country}&country={country}&city={city}&'
            f'type=city&id={id}&from={date_from}&to={date_to}&guests=1&page={page}'
            )
        return url


    @classmethod
    def addMetaData(cls, data, city=None, date_from=None, duration=None):
        data_new = data.copy()
        data_new[Defs.colName('city')] = city
        data_new[Defs.colName('date_from')] = date_from
        data_new[Defs.colName('duration')] = duration
        data_new[Defs.colName('request_time')] = datetime.now()
        return data_new


    @classmethod
    def loop(
        cls, city_list=None, date_from_list=None, duration_list=None, 
        max_pages=None, params=None
        ):
        
        if not params:
            params = SearchParameters(
                mode='custom', city_list=city_list, date_from_list=date_from_list, 
                duration_list=duration_list, max_pages=max_pages
                )

        dfs = []
        for city in params.city_list:
            for date_from in params.date_from_list:
                for duration in params.duration_list:
                    logging.info(f'city: {city}, date: {date_from}, duration: {duration}')
                    cond = True
                    page = 0
                    while cond:
                        page += 1

                        url = cls.createUrl(
                            city=city, date_from=date_from, duration=duration, page=page
                            )
                        logging.info(url)
                        soup = cls.loadSoup(url)
                        df = cls.extractData(soup)
                        df = cls.addMetaData(df, city=city, date_from=date_from, duration=duration)
                        dfs.append(df)

                        if (len(df)==0) | (page==params.max_pages):
                            cond = False
        
        df_all = pd.concat(dfs)
        return df_all