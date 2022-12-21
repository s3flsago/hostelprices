import pandas as pd

from hostelprices.utils import Utils, Definitions




class HostelDF(pd.DataFrame):

    def __init__(self, df):
        super().__init__(df)
        self.check_colum_names()

        self["rating_per_price"] = self["rating"] / self["price (EUR)"]


    def check_colum_names(self):
        Defs = Definitions()

        columns_self = set(self.columns)
        columns_hosteldf = set([val["col_name"] for val in Defs.dict.values()])
        print(columns_self)
        print(columns_hosteldf)
        condition = columns_hosteldf.issubset(columns_self)

        if not condition:
            raise ValueError("DataFrame does not fullfill requirements for HostelDF")
        else: 
            return True
    

    def filter(self,  min_rating=0, max_price=1000, max_dist=50):
        Defs = Definitions()
        condition = (self[Defs.colName('price')]<max_price) & \
            (self[Defs.colName('rating')]>min_rating) & \
            (self[Defs.colName('distance')]<max_dist) 
        df_new = self[condition]

        return HostelDF(df_new)
    




