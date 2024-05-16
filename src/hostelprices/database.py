import pymongo
import pandas as pd
import sys
from datetime import datetime

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils, Defs


class Database():

    def __init__(
        self, client_id=None, data_base_name=None, collection_name=None, 
        overwrite=False
        ):

        self.client_id = client_id
        self.data_base_name = data_base_name
        self.collection_name = collection_name
        

        client = pymongo.MongoClient(client_id)
        db = client[data_base_name]
        self.client = client
        self.db = db
        if collection_name==None:
            self.coll_names  = db.list_collection_names()
            coll = None
            coll_list = [db[coll_name] for coll_name in  self.coll_names]
        else:
            coll = db[collection_name]
            coll_list = [coll]
    
       
        self.coll = coll
        self.coll_list = coll_list
        self.limit_KB = 100000

        if overwrite:
            self.clear()
    

    def filterCollections(self, contains='', contains_not='no_meaning'):
        coll_names_new = []
        colls_new = []
        for ind, coll_name in enumerate(self.coll_names):
            if (contains in coll_name) & (not contains_not in coll_name):
                coll_names_new.append(coll_name)
                colls_new.append(self.coll_list[ind])
        self.coll_names = coll_names_new
        self.coll_list = colls_new


    @property
    def totalSize(self):
        stats = self.db.command('dbstats')
        total_MB = (stats["storageSize"] + stats["indexSize"]) / (10**6)
        return total_MB

    
    @staticmethod
    def GenerateCollectionName(title=None):
        if not title:
            title = 'default'
        branch_str = Utils.activeBranch()
        collection_name = f'main_coll-{title}-{branch_str}-{Utils.fileString(datetime.now())}'
        return collection_name
    

    @staticmethod
    def queryDateFromCollName(coll_name):
        date_str = '-'.join(coll_name.split('-')[-2:])
        try:
            t_query = Utils.dateTime(date_str)
        except Exception:
            t_query = None
        return t_query

    
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
    

    def getPandasDf(self, dct={}, return_hostel_df=True):
        if self.coll!=None:
            request = self.coll.find(dct)
            df = pd.DataFrame(list(request))
            df[Defs.colName('collection_name')] = self.collection_name
            df[Defs.colName('collection_time')] = self.queryDateFromCollName(self.collection_name)
        else:
            df_list = []
            for coll_i, coll_name_i in zip(self.coll_list, self.coll_names):
                request_i = coll_i.find(dct)
                df_i = pd.DataFrame(list(request_i))
                df_i[Defs.colName('collection_name')] = coll_name_i
                df_i[Defs.colName('collection_time')] = self.queryDateFromCollName(coll_name_i)
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
