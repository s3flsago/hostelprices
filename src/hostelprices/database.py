import pymongo
import pandas as pd
import numpy as np
import sys
from datetime import datetime

from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils, Defs



class CollectionName():

    def __init__(self, title=None, branch_str=None, date=None, full_name=None):

        if full_name:
            self.extractAttributes(full_name)
            try:
                assert all([
                    isinstance(self.title, str), 
                    isinstance(self.branch_str, str), 
                    isinstance(self.date_str, str)
                    ])
            except AttributeError:
                raise AttributeError("full_name could not be converted to proper CollectionName")
        else:
            if not title:
                self.title = 'default'
            else:
                self.title = title
            
            if not branch_str:
                self.branch_str = Utils.activeBranch()
            else:
                self.branch_str = branch_str
            
            if not date:
                self.date_str = Utils.fileString(datetime.now())
            else:
                self.date_str = Utils.fileString(date)
        
        assert isinstance(self.title, str)

    def __str__(self):
        return f'{self.title}-{self.branch_str}-{self.date_str}'
    

    @property
    def date(self):
        return Utils.dateTime(self.date_str)
    

    def extractAttributes(self, full_name):
        assert len(full_name)>4
       
        attributes = np.array(full_name.split('-'))
        attributes = attributes[attributes!='']
        
        if len(attributes)>3:
            if len(attributes)==5:
                self.title = attributes[0] + '_' + attributes[1]  
            if len(attributes)==4:  
                self.title = attributes[0]
            self.branch_str = attributes[-3]
            self.date_str = attributes[-2] + '-' + attributes[-1]
        


class Database():

    def __init__(
        self, client_id=None, data_base_name=None, collection_name=None, 
        overwrite=False, enforce_coll_name=True
        ):

        self.enforce_coll_name = enforce_coll_name
        self.client_id = client_id
        self.data_base_name = data_base_name

        if enforce_coll_name:
            if collection_name:
                self.collection_name = CollectionName(full_name=str(collection_name))
            else:
                self.collection_name = None
        else:
            self.collection_name = collection_name
        
        client = pymongo.MongoClient(client_id)
        db = client[data_base_name]
        self.client = client
        self.db = db
        if collection_name==None:
            self.coll_names  = db.list_collection_names()
            if self.enforce_coll_name:
                self.coll_names = [CollectionName(full_name=name) for name in self.coll_names]
            coll_list = [db[str(coll_name)] for coll_name in  self.coll_names]
            coll = None
        else:
            coll = db[str(collection_name)]
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
    

    def enforceCollNames(self):
        try:
            if self.collection_name:
                self.collection_name = CollectionName(full_name=str(self.collection_name))
            self.coll_names = [
                CollectionName(full_name=str(coll_name)) for coll_name in self.coll_names
                ]
        except ValueError:
            print('Could not enforce proper collection name pattern')


    @property
    def totalSize(self):
        stats = self.db.command('dbstats')
        total_MB = (stats["storageSize"] + stats["indexSize"]) / (10**6)
        return total_MB

    
    @staticmethod
    def GenerateCollectionName(title=None):
        collection_name = CollectionName(title=title)
        return collection_name
    

    def changeCollectionTitles(
        self, change_col_names, title=None, date_str=None, coll_name_obj=None, enforce=True
        ):
        for coll_ind, coll_name in enumerate(self.coll_names):
            if str(coll_name) in change_col_names:
                if enforce:
                    if not coll_name_obj:
                        new_coll_name = CollectionName(full_name=str(coll_name))
                        if title:
                            new_coll_name.title = title
                        if date_str:
                            new_coll_name.date_str = date_str
                    else:
                        new_coll_name = CollectionName(full_name=str(coll_name_obj))
                else:
                    if not coll_name_obj:
                        if not title:
                            raise ValueError("If you are trying to set the date. put enforce=True")
                        new_coll_name = title
                    else:
                        new_coll_name = CollectionName(full_name=str(coll_name_obj))

                self.db[self.coll_names[coll_ind]].rename(str(new_coll_name), dropTarget = True)
                self.coll_names[coll_ind] = str(new_coll_name)
    

    @staticmethod
    def queryDateFromCollName(coll_name):
        raise DeprecationWarning(
            "queryDateFromCollName is deprecated. The function from CollectionName should be used")

    
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
            df[Defs.colName('collection_name')] = str(self.collection_name)
            if type(self.collection_name)==CollectionName:
                df[Defs.colName('collection_time')] = self.collection_name.date
        else:
            df_list = []
            for coll_i, coll_name_i in zip(self.coll_list, self.coll_names):
                request_i = coll_i.find(dct)
                df_i = pd.DataFrame(list(request_i))
                df_i[Defs.colName('collection_name')] = str(coll_name_i)
                if type(coll_name_i)==CollectionName:
                    df_i[Defs.colName('collection_time')] = coll_name_i.date
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
