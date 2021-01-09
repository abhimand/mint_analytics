# transfer is counted as debit from one point to another
import pandas as pd
import transactions as tr
import category as category
import budget as bd
import matplotlib as plt

### TO_DO: Create a dummy file 

### Read Data
pd.set_option('display.max_rows', None)
df = pd.read_csv('/Users/abhi.mand/Documents/Programming/Data/transactions.csv', parse_dates=['Date'], index_col=['Date'])
df2 = pd.read_csv('/Users/abhi.mand/Documents/Programming/Data/dummy.csv', parse_dates=['Date'], index_col=['Date'])
df = df.append(df2)

### Data Cleaning & formatting
df = df.drop(columns=['Labels', 'Notes'])
df = df.sort_index()
# Food & Dining = Fast Food, Restaurants, Coffee Shops, Alcohol
df.loc[((df['Category'] == 'Fast Food') | (df['Category'] == 'Restaurants') | (df['Category'] == 'Coffee Shops') | (df['Category'] == 'Restaurants') | (df['Category'] == 'Alcohol & Bars')),'Category'] = 'Food & Dining'
# Auto & Transport = Gas & Fuel, Parking, Service & Auto Parts, Public Transportation
df.loc[((df['Category'] == 'Gas & Fuel') | (df['Category'] == 'Parking') | (df['Category'] == 'Service & Auto Parts') | (df['Category'] == 'Public Transportation')),'Category'] = 'Auto & Transport'
# Travel = Air Travel, Hotel
df.loc[((df['Category'] == 'Hotel') | (df['Category'] == 'Air Travel') | (df['Category'] == 'Vacation')),'Category'] = 'Travel'
# Income = Paycheck
df.loc[((df['Category'] == 'Paycheck')),'Category'] = 'Income'
# Shopping = Clothing, Gift
df.loc[((df['Category'] == 'Clothing') | (df['Category'] == 'Gift')),'Category'] = 'Shopping'
# Entertainment = Amusement
df.loc[((df['Category'] == 'Amusement')),'Category'] = 'Entertainment'
# Investments = Buy
df.loc[((df['Category'] == 'Buy')),'Category'] = 'Investments'

### Graph credit and debit
# tr.graphBar(df)

### Pie Chart of Categorie
# category.piechart(df)

### Budget Analysis
bd.analysis(df)
