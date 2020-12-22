import matplotlib.pyplot as plt
import seaborn as sns

def graphBar(dataframe): 
    # Clean and Prep Data
    df_transactions = dataframe.copy()
    df_transactions.reset_index(inplace=True)
    df_transactions['Year'] = [d.year for d in df_transactions.Date]
    df_transactions['Month'] = [d.strftime('%b') for d in df_transactions.Date]
    # Sort by Months
    df_transactions["month_num"] = df_transactions["Date"].dt.month
    # Group Credit
    df_credit = transactionTypeDF(df_transactions, 'credit')
    # Group Debit
    df_debit = transactionTypeDF(df_transactions, 'debit')
    # Set up figures and axes (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figwidth(30)
    fig.set_figheight(15)
    # Plot data
    ax1 = plot(ax1, df_credit, 'Credit')

    ax2 = plot(ax2, df_debit, 'Debit')
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')

def transactionTypeDF(df, type): 
    df_type = df.loc[df['Transaction Type'] == type, ['Month', 'Year', 'Amount', 'month_num']]
    df_type = df_type.groupby([df_type['Year'],df_type['Month'], df_type['month_num']]).sum() # obtain sum of all values
    df_type = df_type.sort_values(by=['month_num']) # sort the months by the month num instead of num
    df_type.reset_index(inplace=True) # reset index and place multi-index columns into regular ones
    # print(df)
    return df_type

def plot(ax, data, title): 
    ax = sns.barplot(x = 'Year', y = 'Amount', hue='Month', data = data, palette = 'magma', ax=ax)
    for p in ax.patches:
        ax.annotate(('$' + "%.2f" % p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='center', fontsize=11, color='gray', xytext=(0, 50), rotation=90,
            arrowprops=dict(arrowstyle="->"),
            textcoords='offset points')
    ax.set_title(title)
    return ax
