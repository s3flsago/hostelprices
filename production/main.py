"""Main data taking"""

import sys
import logging

from datetime import datetime
from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils
from hostelprices.datacollecting import DataCollecting


MSG_FORMAT = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d| %(message)s"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=MSG_FORMAT, datefmt=DATE_FORMAT, stream=sys.stdout)


def main():
    """main"""

    DataCollecting.run('op')



if __name__=="__main__":
    main()
