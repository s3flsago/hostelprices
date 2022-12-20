import pymongo
import pandas as pd
import sys
from datetime import datetime

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils


class Database():

    def __init__(self, client_id=None, data_base_name=None, collection_name=None):

        self.client_id = client_id
        self.data_base_name = data_base_name
        self.collection_name = collection_name

        client = pymongo.MongoClient(client_id)
        db = client[data_base_name]
        coll = db[collection_name]
    
        self.client = client
        self.db = db
        self.coll = coll
        self.limit_KB = 100000

    @property
    def totalSize(self):
        stats = self.db.command('dbstats')
        total_MB = (stats["storageSize"] + stats["indexSize"]) / (10**6)
        return total_MB

    
    @staticmethod
    def GenerateCollectionName():
        branch_str = Utils.activeBranch()
        collection_name = f'main_coll-{branch_str}-{Utils.fileString(datetime.now())}'
        return collection_name
    

    def checkSizeLimit(self):
        if self.totalSize > self.limit_KB:
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
    

    def clear(self):
        self.coll.drop()
