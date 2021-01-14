import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# maybe make a custom palette
# palette ={"Reimbursement": "C0","Income": "C1","Shopping": "C2","Total": "k"}
months =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = ['2020', '2021']


def analysis(dataframe): 
    df_main = dataframe.copy()
    df_main.reset_index(inplace=True)
    df_main['Year'] = [d.year for d in df_main.Date]
    df_main['Month'] = [d.strftime('%b') for d in df_main.Date]


    for y in years: 
        for m in months:
            # create copy
            df_copy = df_main.copy()
            # locate month and year
            df_copy = df_copy.loc[(df_copy['Month'] == str(m)[:3])]
            df_copy = df_copy.loc[(df_copy['Year'] == int(y))]

            # --------------- formatting data --------------- 
            # drop venmos that are cash out
            df_copy.drop(df_copy[(df_copy['Description'] == 'Venmo Cashout Ppd') & (df_copy['Account Name'] == 'TOTAL CHECKING')].index, inplace=True) 
            # drop tranfers from venmo as debits
            df_copy.drop(df_copy[(df_copy['Description'] == 'Transfer To Jpmorgan Chase') & (df_copy['Transaction Type'] == 'debit') & (df_copy['Account Name'] == 'Venmo')].index, inplace=True) 
            # drop credit card payments
            df_copy.drop(df_copy[df_copy['Category'] == 'Credit Card Payment'].index, inplace = True) 
            # drop dummies
            df_copy.drop(df_copy[df_copy['Category'] == 'Dummy'].index, inplace = True) 
            # drop columns
            df_copy= df_copy.drop(['Description', 'Year', 'Month'], axis=1)
            # grouping
            df_copy= df_copy.groupby([df_copy['Transaction Type'],df_copy['Category']]).sum()
            # ----------- end formatting data --------------- 

            # if empty, exit
            if df_copy.empty == False: 
                # turn dataframe into csv file
                df_copy.to_csv('/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/csv/' + m + ' ' + y + '.csv', index=True)
                # plot
                df_copy.reset_index(inplace=True)
                fig, ax = plt.subplots(1, 1)
                fig.set_figwidth(20)
                fig.set_figheight(10)
                ax = sns.barplot(x = 'Transaction Type', y = 'Amount', hue='Category', data = df_copy, palette = "icefire", ax=ax)
                for p in ax.patches:
                    s = np.sign(p.get_height())
                    # print(s)
                    ax.annotate(('$' + "%.2f" % p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height() ),
                        ha='center', va='center', fontsize=11, color='black', xytext=(0, s * 45), 
                        rotation=90, arrowprops=dict(arrowstyle="->"), textcoords='offset points')
                ax.set_title(m + ' ' + y)
                fig.savefig('/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/plots/' + m + ' ' + y + '_barplot.png')
                print(m + ' of year ' + y + ' is done.')
            else: 
                print('We have no record of ' + m + ' of year ' + y + '.')
    



