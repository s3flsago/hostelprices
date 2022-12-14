"""Main data taking"""

import sys
import logging

from datetime import datetime
from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils
from hostelprices.database import Database


MSG_FORMAT = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d| %(message)s"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=MSG_FORMAT, datefmt=DATE_FORMAT, stream=sys.stdout)

# pwd = os.getcwd()
# module_path = f"{pwd}\..\src"
# sys.path.insert(0, module_path)

def main():
    """main"""

    client_id = Utils.fromConfig('mongo_client')
    data_base_name = Utils.fromConfig('data_base_name')
    collection_name = "main_coll"

    database = Database(
        client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
        )

    city_list = ['Lisbon']#, 'Seville']
    date_from_list = [datetime(2023, 2, 13)]#, datetime(2023, 2, 1)]
    duration_list = [2]#, 5]
    max_pages = 1

    df_all = ScrapeWeb.loop(
        city_list=city_list, date_from_list=date_from_list, duration_list=duration_list, 
        max_pages=max_pages
        )

    print(df_all)

    database.addPandasDf(df_all)



if __name__=="__main__":
    main()
