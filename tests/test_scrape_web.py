import unittest

import sys
import git

working_tree_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
module_path = f"{working_tree_dir}\src"
sys.path.insert(0, module_path)

from hostelprices.scrape_web import ScrapeWeb



class Test(unittest.TestCase):

    def test_load_soup(self):
        url = 'http://www.google.com/'
        soup = ScrapeWeb.loadSoup(url)

        string = soup.find('html').get_text()
        assert('Google' in string)
    
    
    def test_create_url(sef):
        from datetime import datetime

        city = 'Lisbon'
        date_from = datetime(2023, 1, 5)
        duration = 2
        page = 1

        url = ScrapeWeb.createUrl(city=city, date_from=date_from, duration=duration, page=page)

        soup = ScrapeWeb.loadSoup(url)

        string = soup.find('html').get_text()
        assert('hostel' in string)


    def test_extract_data(self):
    
        from datetime import datetime, timedelta
        import numpy as np

        city = 'Lisbon'
        date_from = datetime(2023, 1, 5)
        duration = 2
        page = 1

        url = ScrapeWeb.createUrl(city=city, date_from=date_from, duration=duration, page=page)
        soup = ScrapeWeb.loadSoup(url)
        df = ScrapeWeb.extractData(soup)

        assert(list(df.columns)==['price (EUR)', 'rating', 'distance (km)'])
        assert(len(df)>3)
        assert(np.median(df["price (EUR)"])>10)
        assert(np.median(df["rating"])>4)
        assert(np.median(df["rating"])>4)
        
    
    def test_loop(self):
        from datetime import datetime
        import numpy as np

        city_list = ['Lisbon', 'Seville']
        date_from_list = [datetime(2023, 1, 5), datetime(2023, 4, 1)]
        duration_list = [2, 5]
        max_pages = 2

        df = ScrapeWeb.loop(
            city_list=city_list, date_from_list=date_from_list, duration_list=duration_list, 
            max_pages=max_pages
            )
        
        assert(
            list(df.columns)==[
                'price (EUR)', 'rating', 'distance (km)', 'city', 'date_from', 'duration (days)',
                'request_time'
                ]
                )
        assert(len(df)>3)
        assert(np.median(df["price (EUR)"])>10)
        assert(np.median(df["rating"])>4)
        assert(np.median(df["rating"])>4)
        






if __name__ == '__main__':
    unittest.main()