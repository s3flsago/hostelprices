"""Main data taking"""

import sys
import logging

from datetime import datetime
from hostelprices.scrape_web import ScrapeWeb, SearchParameters
from hostelprices.utils import Utils
from hostelprices.database import Database

MSG_FORMAT = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d| %(message)s"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=MSG_FORMAT, datefmt=DATE_FORMAT, stream=sys.stdout)




class DataCollecting():

    @staticmethod
    def run(mode, client_id=None, title=None):
        if not client_id:
            client_id = Utils.fromConfig('mongo_client')

        data_base_name = Utils.fromConfig('data_base_name')
        collection_name = Database.GenerateCollectionName(title=title)

        database = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )

        params = SearchParameters(mode=mode)

        df_all = ScrapeWeb.loop(params=params)

        database.addPandasDf(df_all)

        return database
