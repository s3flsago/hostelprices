import unittest

import sys
import git

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
        import pandas as pd 

        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )
        
        df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        
        DB.addPandasDf(df)

        DB.clear()  

        assert(DB.totalSize==0)
    
    def test_totalSize(self):
        import pandas as pd 

        client_id = Utils.fromConfig('mongo_client')
        data_base_name = 'TEST_DATA_BASE'
        collection_name = "test_coll"

        DB = Database(
            client_id=client_id, data_base_name=data_base_name, collection_name=collection_name
            )
        
        df = pd.DataFrame({'col1': [1,2], 'col2': [10, 20]})
        
        assert(DB.totalSize==0)
        DB.addPandasDf(df)
        assert(0.005<DB.totalSize<0.01)
        DB.clear()
        assert(DB.totalSize==0)




if __name__ == '__main__':
    unittest.main()