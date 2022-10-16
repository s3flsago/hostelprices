import sys
import os
import logging

msg_format = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d| %(message)s"
date_format = "%d-%b-%y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=msg_format, datefmt=date_format, stream=sys.stdout)

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils
from hostelprices.database import Database


def main():

    client_id = Utils.fromConfig('mongo_client')
    data_base_name = Utils.fromConfig('data_base_name')
    collection_name = "test_coll"

    DB = Database(
        client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
    )
    

    city_list = Utils.fromConfig('city_selection')
    date_from_list = Utils.fromConfig('date_selection')
    duration_list = Utils.fromConfig('duration_selection')
    max_pages = Utils.fromConfig('max_pages')

    df = LoadData.loop(
        city_list=city_list, date_from_list=date_from_list, duration_list=duration_list, 
        max_pages=max_pages
    )


    DB.addPandasDf(df)



if __name__=="__main__":
    main()