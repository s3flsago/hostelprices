import pymongo
import pandas as pd
import sys

from hostelprices.scrape_web import ScrapeWeb


class Database():

    def __init__(self, client_id=None, data_base_name=None, collection_name=None):

        client = pymongo.MongoClient(client_id)
        db = client[data_base_name]
        coll = db[collection_name]
    
        self.client = client
        self.db = db
        self.coll = coll
        self.limit_KB = 100000
    
    def checkSizeLimit(self):
        if self.totalSize() > self.limit_KB:
            exceeded = False
        else:
            exceeded = True
        return exceeded
    

    def addPandasDf(self, df):
        if self.checkSizeLimit():
            data = df.to_dict("records")
            results = self.coll.insert_many(data)
            return results
        else:
            raise MemoryError(f'Data base size limit ({self.limit_KB/1000} MB) exceeded.')
    

    def getPandasDf(self, dct=None):
        request = self.coll.find(dct)
        df = pd.DataFrame(list(request))
        return df
    
    def totalSize(self):
        stats = self.db.command('dbstats')
        total_KB = stats["storageSize"] + stats["indexSize"]
        return total_KB
    
    def clear(self):
        self.coll.drop()


# class DataTaking():

#     def __init__(
#         self, 
#         database=None, 
#         city_list=None, data_from_list=None, duration_list=None, max_pages=None,
#         ):
#         self.database = database
#         self.city_list = city_list
#         self.data_from_list = data_from_list
#         self.duration_list = duration_list
#         self.max_pages = max_pages
    
#     def run(self):
#         df = ScrapeWeb.loop(
#             city_list=self.city_list, date_from_list=self.date_from_list, 
#             duration_list=self.duration_list, max_pages=self.max_pages
#             )
        
#         self.




    

