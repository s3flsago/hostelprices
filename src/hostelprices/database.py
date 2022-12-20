import pymongo
import pandas as pd
import sys
from datetime import datetime

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils


class Database():

    def __init__(self, client_id=None, data_base_name=None, collection_name=None, overwrite=False):

        self.client_id = client_id
        self.data_base_name = data_base_name
        self.collection_name = collection_name

        client = pymongo.MongoClient(client_id)
        db = client[data_base_name]
        if collection_name==None:
            coll_names  = db.list_collection_names()
            coll = None
            coll_list = [db[coll_name] for coll_name in coll_names]
        else:
            coll = db[collection_name]
            coll_list = [coll]
    
        self.client = client
        self.db = db
        self.coll = coll
        self.coll_list = coll_list
        self.limit_KB = 100000

        if overwrite:
            self.clear()


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
        if self.coll==None:
            raise ValueError(
                "Data can only be added if a single collection is selected in the constructor"
                )
        if self.checkSizeLimit():
            data = df.to_dict("records")
            results = self.coll.insert_many(data)
            return results
        else:
            raise MemoryError(f'Data base size limit ({self.limit_KB/1000} MB) exceeded.')
    

    def getPandasDf(self, dct={}):
        if self.coll!=None:
            request = self.coll.find(dct)
            df = pd.DataFrame(list(request))
        else:
            df_list = []
            for coll_i in self.coll_list:
                request_i = coll_i.find(dct)
                df_i = pd.DataFrame(list(request_i))
                df_list.append(df_i)
            df = pd.concat(df_list)
        df = df.sort_index(ascending=True)
        return df
    

    def clear(self):
        if self.coll!=None:
            self.coll.drop()
        else:
            for coll in self.coll_list:
                coll.drop()
