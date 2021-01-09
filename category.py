import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def piechart(dataframe): 
    df_category = dataframe.copy()
    df_category.reset_index(inplace=True)

    # format dates into own columns
    df_category['Year'] = [d.year for d in df_category.Date]
    df_category['Month'] = [d.strftime('%b') for d in df_category.Date]
    df_category = df_category.drop(['Description', 'Original Description', 'Account Name'], axis=1)

    # group data by month and category sum
    df_category = df_category.groupby([df_category['Year'], df_category['Month'],df_category['Category']]).sum() # obtain sum of all values
    df_category = df_category.unstack(level=0)
    # df_category.reset_index(inplace=True)

    print(type(df_category.index))

    for label, content in df_category.items():
        # function that gets the percentage of all
        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n($ {:d})".format(pct, absolute)
        
        # time to plot!
        fig, ax = plt.subplots(figsize=(20, 10), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(content, autopct=lambda pct: func(pct, content),
                                  textprops=dict(color="k"))
        # ax.legend(wedges, months,
        #   title="Ingredients",
        #   loc="center left",
        #   bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        fig.savefig('./plots/pie_plot_' + label[1] + '.png')





                # set up value and pop whichever ones are 0
        # vals = list(np.nan_to_num(content.values))
        # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        # popList = []
        # print(label[1])
        # for i,v in enumerate(vals): 
        #     print(v)
        #     if v == 0 or v == 0.0: 
        #         popList.append(i)
        # for i in popList: 
        #     print(i)
        #     vals.pop(i)
        #     months.pop(i)
        # if label[1] == "Fast Food": 
        #     print(vals)
        #     print(months)