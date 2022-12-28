import git
import os 
import json
import logging
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
    

    @classmethod
    def fromConfig(cls, key):
        with open(cls.configPath(), 'r') as f:
            config_data = json.load(f)
        if not (key in config_data.keys()):
            secrets_path = cls.configPath(secret=True)
            if os.path.exists(secrets_path):
                with open(, 'r') as f:
                    config_data = json.load(f)
            elif key=='client_it':
                return os.env["MONGO_CLIENT"]
                
        
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
        '_id': {'col_name': '_id'},
        'price': {'col_name': 'price (EUR)'},
        'rating': {'col_name': 'rating'},
        'distance': {'col_name': 'distance (km)'},
        'city': {'col_name': 'city'},
        'date_from': {'col_name': 'date from'},
        'duration': {'col_name': 'duration (days)'},
        'request_time': {'col_name': 'request time'},
        'time_before': {'col_name': 'days before'},
        'rating_per_price': {'col_name': 'rating per price'},
        'collection_name': {'col_name': 'collection'},
        'collection_time': {'col_name': 'collection time'},
        }

    @classmethod
    def colName(cls, key):
        return cls.dict[key]['col_name']
    






    