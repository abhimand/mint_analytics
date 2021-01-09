import pandas as pd
import inquirer

def analysis(dataframe): 
    df = dataframe.copy()
    df.reset_index(inplace=True)
    # prompt questions
    questions = [
        inquirer.Text('year', message="What year?"),
        inquirer.List('month',
                message="What month?",
                choices=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            ),
    ]
    answers = inquirer.prompt(questions)
    # parse year and month
    df['Year'] = [d.year for d in df.Date]
    df['Month'] = [d.strftime('%b') for d in df.Date]
    # locate month and year matching from answers
    df = df.loc[(df['Month'] == answers['month'][:3])]
    df = df.loc[(df['Year'] == int(answers['year']))]
    # replace income with reimbursement if account name is venmo
    df.loc[((df['Account Name'] == 'Venmo') & (df['Category'] == 'Income')),'Category'] = 'Reimbursement'
    df.loc[((df['Account Name'] == 'Venmo') & (df['Transaction Type'] == 'credit')),'Category'] = 'Reimbursement'
    # drop tranfers from venmo as debits
    df.drop(df[(df['Transaction Type'] == 'debit') & (df['Category'] == 'Transfer')].index, inplace = True) 
    # drop venmos that are cash out
    df.drop(df[(df['Description'] == 'Venmo Cashout Ppd') & (df['Category'] == 'Income')].index, inplace = True) 
    df.drop(df[(df['Description'] == 'Venmo Cashout Ppd') & (df['Category'] == 'Transfer')].index, inplace = True) 
    # drop credit card payments
    df.drop(df[df['Category'] == 'Credit Card Payment'].index, inplace = True) 
    # drop dummies
    df.drop(df[df['Category'] == 'Dummy'].index, inplace = True) 
    # drop columns
    df = df.drop(['Description', 'Year', 'Month'], axis=1)
    # grouping
    df = df.groupby([df['Transaction Type'],df['Category']]).sum()
    if df.empty: 
        print('We have no records for the month and year you have provided :(')
    else: 
        print('Year: ' + answers['year'], 'Month: ' + answers['month'])
        print(df)
        compression_opts = dict(method='zip',archive_name='out.csv') 
        df.to_csv('out.zip', index=True, compression=compression_opts)

    