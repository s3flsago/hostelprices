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

from hostelprices.utils import Utils

class ScrapeWeb():

    def __init__(self):
        return 


    @classmethod
    def loadSoup(cls, url):
        options = Options()
        options.headless = True

        log_dir = Utils.logPath()
        log_path = os.path.join(log_dir, 'geckodriver.log')

        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=options,
            log_path=log_path
            )

        driver.get(url)  

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        return soup

    @staticmethod
    def correct(card_split):
        split_new = []
        for entry in card_split:
            if 'Dorms' in entry: # if discount, then it could be e.g. '-5%Dorms'
                split_new.append('Dorms')
            elif 'From' in entry: # if discount, then it could be e.g. '-From€21€20'
                split_new.append('From')

                currency_str = '€'
                if 'US$' in entry:
                    currency_str = 'US$'

                entry_split = entry.split(currency_str)
                if entry_split[-1].isdigit():
                    split_new.append(f'{currency_str}{entry_split[-1]}')
            else:
                split_new.append(entry)

        return split_new

    @staticmethod
    def euro(price_usd):
        """Transform USD to EUR"""
        rate = CurrencyRates().get_rate('USD', 'EUR')
        price_eur = price_usd * rate
        return price_eur

    @classmethod
    def priceEur(cls, card_split, currency='EUR'):
        ind_dorms = card_split.index('Dorms')
        ind_price = ind_dorms + 2

        # if there is a discount, ther first price after "Dorms From" is crossed out...
        if len(card_split)>ind_dorms+3:
            if any(char in  card_split[ind_dorms+3] for char in ['$', '€']):
                ind_price = ind_dorms + 3
        try:
            price_string = card_split[ind_price]
        except Exception:
            raise Exception(f'index: {ind_price} \n card_split: {card_split}')

        if '$' in price_string:
            currency = 'USD'

        if currency=='USD':
            price_usd = float(price_string[3:])
            price = cls.euro(price_usd)
        else:
            price = float(price_string[1:])

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
                #print(card_split)
                
                price_EUR = cls.priceEur(card_split)

                # ind_dorms = card_split.index('Dorms')
                # ind_price = ind_dorms + 2

                # # if there is a discount, ther first price after "Dorms From" is crossed out...
                # if len(card_split)>ind_dorms+3:
                #     if any(char in  card_split[ind_dorms+3] for char in ['$', '€']):
                #         ind_price = ind_dorms + 3
                
                # price_string = card_split[ind_price]
                # if '$' in price_string:
                #     currency_dollar = True
                # if currency_dollar:
                #     price = float(price_string[3:])
                # else:
                #     price = float(price_string[1:])

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
            {'price (EUR)': dorm_prices, 'rating': ratings, 'distance (km)': distances}
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
        data_new['city'] = city
        data_new['date_from'] = date_from
        data_new['duration (days)'] = duration
        data_new['request_time'] = datetime.now()
        return data_new


    @classmethod
    def loop(
        cls, city_list=None, date_from_list=None, duration_list=None, 
        max_pages=None,
        ):

        dfs = []
        for city in city_list:
            for date_from in date_from_list:
                for duration in duration_list:
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

                        if (len(df)==0) | (page==max_pages):
                            cond = False
        
        df_all = pd.concat(dfs)
        return df_all