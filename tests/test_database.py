import unittest

import sys
import git

import pandas as pd 

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.utils import Utils
from hostelprices.database import Database


class Test(unittest.TestCase):

    def test_setup_database(self):
        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )

        assert(DB.db.command("dbstats")["db"]==data_base_name)

        DB.clear()
    

    def test_write_data_to_db(self):
        import pandas as pd 

        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
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
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
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
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
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

        DB_both_init = Database(client_id=client_id, data_base_name=data_base_name, overwrite=True)
        DB_both_init.clear()

        DB_1 = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name_1,
            overwrite=True
            )
        DB_2 = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name_2,
            overwrite=True
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
        
        DB_both = Database(client_id=client_id, data_base_name=data_base_name, overwrite=False)

        assert DB_both.coll==None
        assert len(DB_both.coll_list)==2

        df_both = DB_both.getPandasDf()

        assert len(df_both)==5
        assert df_both.equals(df_both_true)
        
        DB_both.clear() 
        assert DB_both.totalSize==0
        assert DB_1.totalSize==0
        assert DB_2.totalSize==0


if __name__ == '__main__':
    unittest.main()