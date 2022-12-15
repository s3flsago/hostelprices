import git
import os 
import json

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
    def configPath(cls):
        config_path = os.path.join(cls.rootPath(), 'config.json')
        return config_path
    

    @classmethod
    def fromConfig(cls, key):
        with open(cls.configPath(), 'r') as f:
            config_data = json.load(f)
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
    def canBeFloat(string):
        return any([substr.isdigit() for substr in string.split('.')])

