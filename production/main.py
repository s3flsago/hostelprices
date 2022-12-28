"""Main data taking"""

import sys
import argparse
import logging

from datetime import datetime
from hostelprices.scrape_web import ScrapeWeb
from hostelprices.utils import Utils
from hostelprices.datacollecting import DataCollecting


MSG_FORMAT = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d| %(message)s"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=MSG_FORMAT, datefmt=DATE_FORMAT, stream=sys.stdout)

parser = argparse.ArgumentParser()
parser.add_argument("--mongo_client", help="MongoDB client ID. Careful: Contains password")
parser.add_argument("--mode", help="One of the modes from scrape_web.SearchParameters")
parser.add_argument("--title", help="Title will be found in collection name later")
args = parser.parse_args()

def main():
    """main"""

    DataCollecting.run(args.mode, client_id=args.mongo_client, title=args.title)



if __name__=="__main__":
    main()
