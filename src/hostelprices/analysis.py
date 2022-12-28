import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from hostelprices.utils import Utils, Defs




class HostelDF(pd.DataFrame):

    def __init__(self, df):
        super().__init__(df)
        self.transform_column_names()
        self.addSecondaryColumns()
        self.check_colum_names()


    def addSecondaryColumns(self):
        if not Defs.colName('rating_per_price') in self.columns:
            self[Defs.colName('rating_per_price')] = \
                self[Defs.colName('rating')] / self[Defs.colName('price')]
        
        if not Defs.colName('time_before') in self.columns:
            self[Defs.colName('time_before')] = (
                self[Defs.colName('date_from')] - self[Defs.colName('collection_time')]
                ).dt.total_seconds().astype(np.float)/(3600*24)


    def transform_column_names(self):
        for col in self.columns:
            if col in ['date_from', 'date from']:
                self[Defs.colName('date_from')] = self[col]
            if col in ['request_time', 'request time']:
                self[Defs.colName('request_time')] = self[col]


    def check_colum_names(self):
        columns_self = set(self.columns)
        columns_hosteldf = set([val["col_name"] for val in Defs.dict.values()])

        condition = columns_hosteldf.issubset(columns_self)

        if not condition:
            raise ValueError("DataFrame does not fullfill requirements for HostelDF")
        else: 
            return True
    

    def filter(self, condition):
        df_new = self[condition]
        return HostelDF(df_new)


    def processed_values(
        self, 
        min_rating=0, min_price=5, max_price=1000, max_dist=50,
        min_time_before=0, max_time_before=1000,
        ):
        condition = (self[Defs.colName('price')]<max_price) & \
            (self[Defs.colName('price')]>min_price) & \
            (self[Defs.colName('rating')]>min_rating) & \
            (self[Defs.colName('distance')]<max_dist) & \
            (self[Defs.colName('time_before')]>min_time_before) & \
            (self[Defs.colName('time_before')]<max_time_before)
        df_new = self.filter(condition)
        prices = df_new[Defs.colName('price')].values
        prices = np.sort(prices)
        avg_price = prices[1:6].mean()
        n_hostels = len(prices)

        return avg_price, n_hostels
    

    def cummulated(self):
        times_before = np.sort(self[Defs.colName('time_before')].value_counts().index.values)
        edges = (times_before[1:] + times_before[:-1]) / 2
        edges = [times_before[0]-(edges[0]-times_before[0])] + \
            list(edges) + \
            [times_before[-1]+(times_before[-1]-edges[-1])]
        edges = [[edges[ind], edges[ind+1]] for ind in range(len(edges)-1)]
        avg_price_arr = []
        n_hostels_arr = []
        for t0, t1 in edges:
            avg_price, n_hostels = self.processed_values(min_time_before=t0, max_time_before=t1)
            avg_price_arr.append(avg_price)
            n_hostels_arr.append(n_hostels)

        return times_before, avg_price_arr, n_hostels_arr



    def plot(
        self, x=None, y=None, col=None, row=None, 
        y_label='', x_label='', ylim=(None,None), xlim=(None,None),
        marker_size=1, hist=False, nbinsy=None, nbinsx=None, nbins=None,
        label_fct=None, leg_title=None
        ):
        if nbins:
            nbinsx = nbins
            nbinsy = nbins
        elif not nbinsy and not nbinsx:
            nbinsx = 10
            nbinsy = 10

        bins = (np.linspace(*xlim, nbinsx), np.linspace(*ylim, nbinsy))
        if label_fct==None:
            def default_fct(x):
                return x
            label_fct = default_fct

        if type(y)==str:
            y = [y]

        if not y_label and len(y)==1:
            y_label = y[0]
        if not x_label:
            x_label = x
        
        if col:
            col_list = np.sort(self[col].value_counts().index)
        else:
            col_list = [None]
        n_cols = len(col_list)

        if row:
            row_list = np.sort(self[row].value_counts().index)
        else:
            row_list = [None]
        n_rows = len(row_list)

        fig, axs = plt.subplots(n_rows, n_cols)
        fig.set_size_inches(n_cols*10, n_rows*6)
        for ind_row, row_val in enumerate(row_list):
            for ind_col, col_val in enumerate(col_list):
                
                if type(axs)!=np.ndarray:
                    ax = axs
                else:
                    ax = axs.reshape((n_rows, n_cols))[ind_row, ind_col]
                
                df_choice = self.copy()
                if col_val!=None:
                    df_choice = df_choice[df_choice[col]==col_val]
                if row_val!=None:
                    df_choice = df_choice[df_choice[row]==row_val]
                
                n_events = len(df_choice)

                if len(df_choice)==0:
                    fig.delaxes(ax)

                else:
                    for y_i in y:
                        if hist:
                            hist = ax.hist2d(
                                df_choice[x], df_choice[y_i], bins=bins, cmap='Oranges'
                                )
                            fig.colorbar(hist[3], ax=ax)
                        else:
                            ax.scatter(
                                df_choice[x], df_choice[y_i], label=label_fct(y_i), s=marker_size
                                )

                ax.set_ylim(bottom=ylim[0], top=ylim[1])
                ax.set_xlim(left=xlim[0], right=xlim[1])

                title_str_col = ''
                title_str_row = ''
                if n_cols>1:
                    title_str_col = f'{label_fct(col)}={label_fct(col_val)}'
                if n_rows>1:
                    title_str_row = f'{label_fct(row)} = {label_fct(row_val)}'

                ax.set_title(f'{title_str_row}   {title_str_col}')
                ax.set_ylabel(label_fct(y_label))
                ax.set_xlabel(label_fct(x_label))

                handles, _ = ax.get_legend_handles_labels()
                labelspacing = None
                fontsize = None
                if handles==[]:
                    patch = matplotlib.patches.Patch(color='white', label='')
                    handles.append(patch)
                    labelspacing=0
                if leg_title=='events':
                    title = f'{n_events} events'
                else:
                    title = None
                ax.legend(
                    title=title, handles=handles, fontsize=fontsize, 
                    labelspacing=labelspacing, title_fontsize=20
                    )
        
        fig.show()

        return fig, axs


