# transfer is counted as debit from one point to another
import pandas as pd
import transactions as tr

### Read Data
pd.set_option('display.max_rows', None)
df = pd.read_csv('/Users/abhi.mand/Documents/Programming/Data/transactions.csv', parse_dates=['Date'], index_col=['Date'])

### Data Cleaning
df = df.drop(columns=['Labels', 'Notes'])
df = df.sort_index()

### Graph credit and debit
tr.graphBar(df)

### Pie Chart of Categories


