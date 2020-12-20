import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import cycle, islice

def graphBar(dataframe): 
    # Clean and Prep Data
    df_transactions = dataframe.copy()
    df_transactions.reset_index(inplace=True)
    df_transactions['Year'] = [d.year for d in df_transactions.Date]
    df_transactions['Month'] = [d.strftime('%b') for d in df_transactions.Date]
    print(df_transactions)
    # Sort by Months
    df_transactions["month_num"] = df_transactions["Date"].dt.month

    # Group Credit 
    df_credit = df_transactions.loc[df_transactions['Transaction Type'] == 'credit', ['Month', 'Year', 'Amount', 'month_num']]
    df_credit = df_credit.groupby([df_credit['Year'],df_credit['Month'], df_credit['month_num']]).sum() # obtain sum of all values
    df_credit = df_credit.sort_values(by=['month_num']) # sort the months by the month num instead of num

    df_credit.reset_index(inplace=True) # reset index and place multi-index columns into regular ones
    df_credit = df_credit.unstack() # create wide form to plot well

    # Group Debit
    df_debit = df_transactions.loc[df_transactions['Transaction Type'] == 'debit', ['Month', 'Year', 'Amount', 'month_num']]
    df_debit = df_debit.groupby([df_debit['Year'], df_debit['Month'], df_debit['month_num']]).sum() # obtain sum of all values
    df_debit = df_debit.sort_values(by=['month_num']) # sort the months by the month num instead of num

    df_debit.reset_index(inplace=True) # reset index and place multi-index columns into regular ones
    df_debit = df_debit.unstack() # create wide form to plot well

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figwidth(20)
    fig.set_figheight(10)
    ax1 = sns.barplot(x = 'Year', y = 'Amount', hue='Month', data = df_credit, palette = 'magma', ax=ax1)
    ax2 = sns.barplot(x = 'Year', y = 'Amount', hue='Month', data = df_debit, palette = 'magma', ax=ax2)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')