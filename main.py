# transfer is counted as debit from one point to another
import pandas as pd
import transactions as tr
import category as category
import matplotlib as plt

### TO_DO: Create a dummy file 

### Read Data
pd.set_option('display.max_rows', None)
df = pd.read_csv('/Users/abhi.mand/Documents/Programming/Data/transactions.csv', parse_dates=['Date'], index_col=['Date'])
df2 = pd.read_csv('/Users/abhi.mand/Documents/Programming/Data/dummy.csv', parse_dates=['Date'], index_col=['Date'])
df = df.append(df2)

### Data Cleaning
df = df.drop(columns=['Labels', 'Notes'])
df = df.sort_index()


### Group labels

### Graph current trend of income

### Graph credit and debit
tr.graphBar(df)

### Pie Chart of Categorie
category.piechart(df)

