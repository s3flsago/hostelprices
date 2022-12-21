import unittest

import sys
import git

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.database import Database
from hostelprices.utils import Utils
from hostelprices.datacollecting import DataCollecting
from hostelprices.analysis import HostelDF

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Test(unittest.TestCase):

    def test_hostel_data_from_database(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )        
        
        city_list = ['Lisbon']#, 'Seville']
        date_from_list = [datetime(2023, 2, 13)]#, datetime(2023, 2, 1)]
        duration_list = [2]#, 5]
        max_pages = 2

        df_all = ScrapeWeb.loop(
            city_list=city_list, date_from_list=date_from_list, duration_list=duration_list, 
            max_pages=max_pages
            )
        
        DB.addPandasDf(df_all)

        df_loaded = DB.getPandasDf({})

        sns.relplot(
        data=df_loaded,    
            x='price (EUR)',
            y='rating',
            col='date_from',
            hue='city'
            )
        plt.close()

        DB.clear()
    

    def test_data_loading_SearchParameters(self):
        database = DataCollecting.run('debug')

        df_loaded = database.getPandasDf({})

        sns.relplot(
        data=df_loaded,    
            x='price (EUR)',
            y='rating',
            col='date_from',
            hue='city'
            )
        plt.close()

        database.clear()
    

    def test_HostelDF(self):
        from bson.objectid import ObjectId
        df_right = {
            '_id': {0: ObjectId('63a310561e3c536865caa934'),
            1: ObjectId('63a310561e3c536865caa935')},
            'price (EUR)': {0: 33.9654684404189, 1: 29.2480422681385},
            'rating': {0: 9.7, 1: 9.7},
            'distance (km)': {0: 0.5, 1: 0.4},
            'city': {0: 'Lisbon', 1: 'Lisbon'},
            'date_from': {0: 1,1: 1},
            'duration (days)': {0: 1, 1: 1},
            'request_time': {0: 1, 1: 1}
            }

        df_false = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})

        hdf = HostelDF(df_right)

        with self.assertRaises(ValueError):
            HostelDF(df_false)
        
    def test_HostelDF_filter(self):
        from bson.objectid import ObjectId
        df = {
            '_id': {0: ObjectId('63a310561e3c536865caa934'),
            1: ObjectId('63a310561e3c536865caa935')},
            'price (EUR)': {0: 33.9654684404189, 1: 29.2480422681385},
            'rating': {0: 9.7, 1: 9.7},
            'distance (km)': {0: 0.5, 1: 0.4},
            'city': {0: 'Lisbon', 1: 'Lisbon'},
            'date_from': {0: 1,1: 1},
            'duration (days)': {0: 1, 1: 1},
            'request_time': {0: 1, 1: 1}
            }
        
        hdf = HostelDF(df)

        assert len(hdf)==2
        hdf = hdf.filter(max_price=30)
        assert len(hdf)==1


