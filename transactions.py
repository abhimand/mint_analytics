import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    fig.savefig('bar_plot.png')

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