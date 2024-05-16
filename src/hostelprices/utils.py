import git
import os 
import json
import logging
from datetime import datetime

from datetime import datetime

class Utils():

    @staticmethod
    def formatDate(date):
        string = f'{date.year}-{date.month}-{date.day}'
        return string
    
    @staticmethod
    def rootPath():
        repo_root_path = git.Repo(".", search_parent_directories=True).working_tree_dir
        return repo_root_path

    @staticmethod
    def activeBranch():
        branch_str = git.Repo(".", search_parent_directories=True).active_branch.name
        return branch_str

    @classmethod
    def logPath(cls):
        log_dir = os.path.join(cls.rootPath(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        return log_dir
    

    @classmethod
    def configPath(cls, secret=False):
        secret_str = ''
        if secret:
            secret_str = '_secrets'
        config_path = os.path.join(cls.rootPath(), f'config{secret_str}.json')
        return config_path
    
    
    @staticmethod
    def strToDatetime(date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date_obj
    

    @classmethod
    def fromConfig(cls, key):
        with open(cls.configPath(), 'r') as f:
            config_data = json.load(f)
<<<<<<< HEAD
        val = config_data[key]

        if key=='date_selection':
            val = [cls.strToDatetime(val_i) for val_i in val]

        return val
=======
        if not (key in config_data.keys()):
            secrets_path = cls.configPath(secret=True)
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r') as f:
                    config_data = json.load(f)
            elif key=='mongo_client':
                return os.environ["MONGO_CLIENT_ID"]
                
        return config_data[key]



    @classmethod
    def testPath(cls):
        test_path = os.path.join(cls.rootPath(), 'tests')
        return test_path


    @classmethod
    def testFixturesPath(cls):
        test_fixtures_path = os.path.join(cls.testPath(), 'fixtures')
        return test_fixtures_path


    @staticmethod
    def fileString(time):
        return time.strftime("%m_%d_%Y-%H_%M")
    
    @staticmethod
    def dateTime(file_str):
        return datetime.strptime(file_str, "%m_%d_%Y-%H_%M")

    
    @staticmethod
    def canBeFloat(string):
        return any([substr.isdigit() for substr in string.split('.')])




class Defs():

    
    dict = {
        '_id': {'col_name': '_id', 'alt_col_names': []},
        'price': {'col_name': 'price (EUR)', 'alt_col_names': []},
        'rating': {'col_name': 'rating', 'alt_col_names': []},
        'distance': {'col_name': 'distance (km)', 'alt_col_names': []},
        'city': {'col_name': 'city', 'alt_col_names': []},
        'date_from': {'col_name': 'date from', 'alt_col_names': ['date_from']},
        'duration': {'col_name': 'duration (days)', 'alt_col_names': []},
        'request_time': {'col_name': 'request time', 'alt_col_names': ['request_time']},
        'time_before': {'col_name': 'days before', 'alt_col_names': ['time_before']},
        'rating_per_price': {'col_name': 'rating per price', 'alt_col_names': []},
        'collection_name': {'col_name': 'collection', 'alt_col_names': []},
        'collection_time': {'col_name': 'collection time', 'alt_col_names': ['collection_time']},
        }

    @classmethod
    def colName(cls, key):
        return cls.dict[key]['col_name']
    






    
>>>>>>> 7a6a857929766f56301196042efbc499144b85ff
