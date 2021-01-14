# transfer is counted as debit from one point to another
import pandas as pd
import overview as ov
import months as mths
import matplotlib as plt

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
# Venmos that are credit or income = reimbursement
df.loc[((df['Account Name'] == 'Venmo') & (df['Transaction Type'] == 'credit')),'Category'] = 'Reimbursement'
# Drop transfers from Total Checking to Venmo
df = df.drop(df[(df['Account Name'] == 'TOTAL CHECKING') & (df['Category'] == 'Transfer') & (df['Description'] == 'Venmo')].index)

### Graph credit and debit
ov.graphBar(df)

### Months Analysis
mths.analysis(df)

### Overview Analysis
ov.overviewCSV()

### Trendline Analysis
ov.trendLine()