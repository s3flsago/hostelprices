import unittest
from copy import deepcopy
import sys
import git

import pandas as pd 

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.utils import Utils
from hostelprices.database import Database
from hostelprices.database import CollectionName


class Test(unittest.TestCase):

    def test_setup_database(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name,
            enforce_coll_name=False
            )

        assert(DB.db.command("dbstats")["db"]==data_base_name)

        DB.clear()
    

    def test_write_data_to_db(self):
        import pandas as pd 

        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name,
            enforce_coll_name=False
            )
        
        df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        
        DB.addPandasDf(df)

        request_dct = {'col1': 1}
        df = DB.getPandasDf(request_dct)
        assert(df.loc[0, 'col1']==1)
        DB.clear()
    

    def test_clear(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE_test_clear'
        collection_name = "test_coll_test_clear"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name,
            enforce_coll_name=False
            )
        
        df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        
        DB.addPandasDf(df)

        DB.clear()  

        assert(DB.totalSize==0)
    

    def test_totalSize(self):
        

        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE_totalSize'
        collection_name = "test_coll_totalSize"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name,
            enforce_coll_name=False
            )
        
        df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        
        assert(DB.totalSize==0)
        DB.addPandasDf(df)
        assert(0.005<DB.totalSize<0.01)
        DB.clear()
        assert(DB.totalSize==0)
    

    def test_multiple_collection_readout(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DB_multiple_readout'
        collection_name_1 = "test_coll_1"
        collection_name_2 = "test_coll_2"

        DB_both_init = Database(
            client_id=client_id, data_base_name=data_base_name, overwrite=True,
            enforce_coll_name=False
            )
        DB_both_init.clear()

        DB_1 = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name_1,
            overwrite=True, enforce_coll_name=False
            )
        DB_2 = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name_2,
            overwrite=True, enforce_coll_name=False
            )
        
        df1 = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        DB_1.addPandasDf(df1)
        df1_crosscheck = DB_1.getPandasDf()
        assert len(df1_crosscheck)==2

        df2 = pd.DataFrame({'col1': [3,4,5], 'col2': [30, 40, 50]})
        DB_2.addPandasDf(df2)
        df2_crosscheck = DB_2.getPandasDf()
        assert len(df2_crosscheck)==3

        df_both_true = pd.concat([df1_crosscheck, df2_crosscheck]).sort_index(ascending=True)
        assert len(df_both_true)==5
        
        DB_both = Database(
            client_id=client_id, data_base_name=data_base_name, overwrite=False,
            enforce_coll_name=False
            )

        assert DB_both.coll==None
        assert len(DB_both.coll_list)==2

        df_both = DB_both.getPandasDf()

        assert len(df_both)==5

        DB_both.clear() 
        assert DB_both.totalSize==0
        assert DB_1.totalSize==0
        assert DB_2.totalSize==0
    

    def test_column_name(self):
        cn = CollectionName()
        assert(len(str(cn).split('-'))==4)

        cn = CollectionName(title='test')
        assert(len(str(cn).split('-'))==4)

        with self.assertRaises(AssertionError):
            cn = CollectionName(full_name='test')

        cn = CollectionName(full_name='main_coll--dev-12_28_2022-13_17')
        
        cn = CollectionName(full_name='main_coll-testname-dev-12_28_2022-13_17')
    

    def test_rename_colums(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'

        DB = Database(client_id=client_id, data_base_name=data_base_name, enforce_coll_name=False)
        DB.clear()

        collection_names = [
            "test_coll",
            "main_coll--dev-12_28_2022-13_17",
            "main_coll-default-dev-01_03_2023-13_17",
            "basic",
            ]

        for collection_name in collection_names:
            if collection_name in ["test_coll", "basic"]:
                with self.assertRaises(AttributeError):
                    DB = Database(
                        client_id=client_id, data_base_name=data_base_name, 
                        collection_name=collection_name, enforce_coll_name=True
                    )
                continue
            else:
                DB = Database(
                    client_id=client_id, data_base_name=data_base_name, 
                    collection_name=collection_name, enforce_coll_name=True
                    )
            
            df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
            
            DB.addPandasDf(df)

        DB = Database(
                client_id=client_id, data_base_name=data_base_name
                )
        DB.clear()

        for collection_name in collection_names:
            DB = Database(
                client_id=client_id, data_base_name=data_base_name, collection_name=collection_name,
                enforce_coll_name=False
                )
            
            df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
            
            DB.addPandasDf(df)

        DB = Database(
                client_id=client_id, data_base_name=data_base_name, enforce_coll_name=False
                )
        
        with self.assertRaises(AttributeError):
            DB.changeCollectionTitles(['basic'], coll_name_obj="test1", enforce=True)

        DB.changeCollectionTitles(["basic"], title="test2", enforce=False)

        DB.changeCollectionTitles(
            ["test2"], coll_name_obj=CollectionName(title='test4'), enforce=True
            )

        coll_names = deepcopy(DB.coll_names)
        coll_names.remove("test_coll")
        DB.changeCollectionTitles(coll_names, title="test3", enforce=True)

        DB.clear()


    def test_enforce_coll_names(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'

        DB = Database(
                client_id=client_id, data_base_name=data_base_name, enforce_coll_name=False
                )
        DB.clear()

        collection_names = [
            "test_coll",
            "main_coll--dev-12_28_2022-13_17",
            "basic",
            ]
        
        for collection_name in collection_names:
            if collection_name in ["test_coll", "basic"]:
                with self.assertRaises(AttributeError):
                    DB = Database(
                        client_id=client_id, data_base_name=data_base_name, 
                        collection_name=collection_name, enforce_coll_name=True
                    )
                continue
            else:
                DB = Database(
                        client_id=client_id, data_base_name=data_base_name, 
                        collection_name=collection_name, enforce_coll_name=True
                    )
            
            df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
            
            DB.addPandasDf(df)

        DB = Database(
                client_id=client_id, data_base_name=data_base_name, enforce_coll_name=False
                )

        DB.enforceCollNames()
        DB.clear()
        


if __name__ == '__main__':
    unittest.main()