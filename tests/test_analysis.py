import unittest

import sys
import git

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.database import Database
from hostelprices.utils import Utils, Defs
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
        collection_name = Database.GenerateCollectionName()

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

        df_false = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})

        hdf = HostelDF(df_loaded)

        with self.assertRaises(AttributeError):
            HostelDF(df_false)

        hdf = hdf.filter(hdf[Defs.colName('price')]<30)

        DB.clear()
    

    def test_data_loading_SearchParameters(self):
        database = DataCollecting.run('debug')

        df_loaded = database.getPandasDf({})

        hdf = HostelDF(df_loaded)

        database.clear()
    

