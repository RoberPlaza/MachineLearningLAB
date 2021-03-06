from numpy import corrcoef, transpose, arange
from pylab import pcolor, xticks, yticks
from sklearn import preprocessing

import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt



path_in     = "data/preprocessed.csv"
path_out    = "data/data_norm.csv"


def normalize_filtered_data(file):

    exclude         = ['UserID', 'UUID', 'Version', 'TimeStemp']
    df_ex           = file.loc[:, file.columns.difference(exclude)]

    min_max_scaler  = preprocessing.MinMaxScaler()
    df_norm         = min_max_scaler.fit_transform(df_ex)

    return df_norm

def test_corr(df_ex):
    
    R   = corrcoef(transpose(df_ex))
    pcolor(R)
    plt.colorbar()
    yticks(arange(0,14),range(0,14))
    xticks(arange(0,14),range(0,14))
    plt.savefig("plots/correlation.png")

    
    sns.set(style="white")
    mask = numpy.zeros_like(R, dtype=numpy.bool)
    mask[numpy.triu_indices_from(mask)] = True
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(200, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(R, mask=mask, cmap=cmap, vmax=.8,
                square=True, xticklabels=2, yticklabels=2,
                linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
    
    plt.savefig("plots/heat_map.png")
    

def read_df(path):
   return pd.read_csv(path, low_memory=False)


def to_csv(path,dataframe):
    numpy.savetxt(path, dataframe, delimiter=",")

def view_columns_name(path_in):
    df = read_df(path_in)
    print(df.columns)

if __name__ == '__main__':
    
    #First we load the preprocessed dataset in df_pred
    df_prep = read_df(path_in) 
    #Here we have to normalize the data in dfnorm
    df_norm = normalize_filtered_data(df_prep)
    to_csv(path_out,df_norm)
    df_norm = read_df(path_out)
    #corr tests
    test_corr(df_norm)
    view_columns_name(path_in)

