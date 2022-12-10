import unittest

import sys
import git

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.database import Database
from hostelprices.utils import Utils

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


class Test(unittest.TestCase):

    def test_hostel_data_from_database(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )        
        
        city_list = ['Lisbon']#, 'Seville']
        date_from_list = [datetime(2023, 2, 13), datetime(2023, 2, 1)]
        duration_list = [2]#, 5]
        max_pages = 1

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

