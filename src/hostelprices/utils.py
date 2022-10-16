import git
import os 
import json

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
    

    @classmethod
    def logPath(cls):
        log_dir = os.path.join(cls.rootPath(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        return log_dir
    

    @classmethod
    def configPath(cls):
        config_path = os.path.join(cls.rootPath(), 'config.json')
        return config_path
    
    
    @staticmethod
    def strToDatetime(date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date_obj
    

    @classmethod
    def fromConfig(cls, key):
        with open(cls.configPath(), 'r') as f:
            config_data = json.load(f)
        val = config_data[key]

        if key=='date_selection':
            val = [cls.strToDatetime(val_i) for val_i in val]

        return val