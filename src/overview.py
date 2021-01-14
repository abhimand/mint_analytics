import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob as glob
import pandas as pd
from sklearn.linear_model import LinearRegression


months =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = ['2020', '2021']
index = ['Income', 'Reimbursement', 'Investments','Student Loan', 'Food & Dining', 'Groceries', 'Shopping', 'Travel', 'Business Services', 'Entertainment', 'Auto & Transport', 'Service & Parts','Taxes', 'Electronics & Software','Credit Total','Debit Total', 'Profit']

sns.set_theme(style="darkgrid")

def graphBar(dataframe): 
    # reset data
    df_transactions = dataframe.copy()
    df_transactions.reset_index(inplace=True)
    # drop credit card payments and venmo transfers
    index_names = df_transactions[ (df_transactions['Transaction Type'] == 'credit') & (df_transactions['Category'] == 'Credit Card Payment')].index
    df_transactions.drop(index_names, inplace = True) 
    index_names = df_transactions[ (df_transactions['Transaction Type'] == 'debit') & (df_transactions['Category'] == 'Transfer') & (df_transactions['Account Name'] == 'Venmo')].index
    df_transactions.drop(index_names, inplace = True) 
    # format dates into own columns
    df_transactions['Year'] = [d.year for d in df_transactions.Date]
    df_transactions['Month'] = [d.strftime('%b') for d in df_transactions.Date]
    # Sort by Months
    df_transactions["month_num"] = df_transactions["Date"].dt.month
    # Group Credit
    df_credit = transactionTypeDF(df_transactions, 'credit')
    # Group Debit
    df_debit = transactionTypeDF(df_transactions, 'debit')

    #combine
    df_combine = transactionTypeDF(df_transactions, 'credit')
    df_combine['Amount'] = df_credit['Amount'] - df_debit['Amount']

    # Set up figures and axes (using Seaborn)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_figwidth(40)
    fig.set_figheight(30)
    # Plot data
    ax1 = plotBar(ax1, df_credit, 'Credit')
    ax2 = plotBar(ax2, df_debit, 'Debit')
    ax3 = plotBar(ax3, df_combine, 'Combined')

    # Save image and return fig (don't change this part)
    fig.savefig('/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/plots/bar_plot.png')

def transactionTypeDF(df, type): 
    # locate data that has transaction of type
    df_type = df.loc[df['Transaction Type'] == type, ['Month', 'Year', 'Amount', 'month_num', 'Date']]
    # group the data and sum
    df_type = df_type.groupby([df_type['Year'],df_type['Month'], df_type['month_num']]).sum() # obtain sum of all values
    # sort
    df_type = df_type.sort_values(by=['month_num']) # sort the months by the month num instead of num
    # reset index
    df_type.reset_index(inplace=True) # reset index and place multi-index columns into regular ones
    # print(df)
    return df_type

def plotBar(ax, data, title): 
    # plot data
    ax = sns.barplot(x = 'Year', y = 'Amount', hue='Month', data = data, palette = 'magma', ax=ax)
    # annotate each bar with the value
    for p in ax.patches:
        s = np.sign(p.get_height())
        # print(s)
        ax.annotate(('$' + "%.2f" % p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height() ),
            ha='center', va='center', fontsize=11, color='black', xytext=(0, s * 45), 
            rotation=90, arrowprops=dict(arrowstyle="->"), textcoords='offset points')
    ax.set_title(title)
    return ax
def overviewCSV(): 
    # get path of csv files
    path = r'/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/csv' # use your path
    # obtain all files that end with .csv
    all_files = glob.glob(path + "/*.csv")
    li = []
    # keys = []

    for filename in all_files:
        # read csv
        df_csv = pd.read_csv(filename, index_col=None, header=0)
        # obtain credit and debit sums
        credit_sum = df_csv.loc[df_csv['Transaction Type'] == 'credit', 'Amount'].sum()
        debit_sum = df_csv.loc[df_csv['Transaction Type'] == 'debit', 'Amount'].sum()
        profit = credit_sum - debit_sum
        # create rows with debit and credit sums
        new_row_credit = {'Transaction Type' : 'credit', 'Category':'Credit Total', 'Amount': credit_sum}
        new_row_debit = {'Transaction Type' : 'debit', 'Category':'Debit Total', 'Amount': debit_sum}
        new_row_profit = {'Transaction Type' : 'profit', 'Category':'Profit', 'Amount': profit}
        # add new rows
        df_csv = df_csv.append(new_row_credit, ignore_index=True)
        df_csv = df_csv.append(new_row_debit, ignore_index=True)
        df_csv = df_csv.append(new_row_profit, ignore_index=True)
        # set category as index
        df_csv = df_csv.set_index('Category')
        # get file name
        name = filename.split('csv/',1)[1].split('.csv')[0]
        # rename category with file name [month_year]
        df_csv.rename(columns={"Amount": name}, inplace=True)
        # drop Transaction Type column
        df_csv.drop(columns=['Transaction Type'], inplace=True)
        li.append(df_csv)
        # keys.append(name)

    # combine all dataframes into one
    df_combined = pd.concat(li, axis=1)

    # create month and year column to reindex
    column_list_reindex = []
    for y in years: 
        for m in months: 
            column_list_reindex.append(m + ' ' + y)
    # reindex both column and rows
    df_combined = df_combined.reindex(index, columns=column_list_reindex)
    # drop columns with no data
    df_combined = df_combined.dropna(how='all', axis=1)

    df_combined.to_csv('/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/csv/overview.csv', index=True)

def trendLine(): 
    filename = '/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/csv/overview.csv'
    df_overview = pd.read_csv(filename, index_col='Unnamed: 0', header=0)

    X_num_months = np.array([i + 1 for i,v in enumerate(df_overview.columns.values)]).reshape(-1, 1) # num of months
    X_months = df_overview.columns.values.reshape(-1, 1) # months & year
    Y = df_overview.loc['Profit'].values.reshape(-1, 1)

    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X_num_months, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X_num_months)  # make predictions

    plt.clf()
    plt.scatter(X_num_months, Y)
    plt.plot(X_num_months, Y_pred, color='red')

    plt.title('Profit Trend')
    plt.xlabel('Months')
    plt.ylabel('Profit')
    plt.savefig('/Users/abhi.mand/Documents/Programming/Visualization/mint_analytics/plots/trend_plot.png')
