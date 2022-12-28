import unittest

import sys
import git
import os
import json

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from hostelprices.utils import Utils

from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np



class Test(unittest.TestCase):

    def test_fromConfig(self):
        Utils.fromConfig('mongo_client')



if __name__ == '__main__':

    unittest.main()