import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def piechart(dataframe): 
    df_category = dataframe.copy()
    df_category.reset_index(inplace=True)
    fig, ax = plt.subplots(1,1)
    fig.set_figwidth(10)
    fig.set_figheight(5)
    ax = df_category['Category'].value_counts().plot(kind='pie')
    fig.savefig('pie_plot.png')