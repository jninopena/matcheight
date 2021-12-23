#This case have several possible anwers
#My approach was to take residuals of the input param against each unique Height.
#After that I just show the names o plaeys based on conditions of residual and the number of players for each unique height
#this algo is O(log(n)) since it makes comparasions based only in a unique list of ages

import requests
import pandas as pd
import math
import sys

def makeResponse(a,b, answers):
    print('this is response number %d:', answers)
    print(a)
    print (b)
    return

def showResults(subset, original):
    df_dict = subset.to_dict('records')
    possibleAnswers = 0
    for row in df_dict:
        if row['result'] < row['Counts']:
            namesA = original[original['h_in']== row['H']]
            namesB = original[original['h_in'] == row['residual']]
            possibleAnswers += 1
            namesA = namesA[['first_name', 'last_name']]
            namesB= namesB[['first_name', 'last_name']]
            response = makeResponse(namesA.head(int(math.floor(row['result']))), namesB, possibleAnswers)
    if possibleAnswers == 0:
        print('No match')        

def main(arg):
    param = int(arg)
    req = requests.get('https://mach-eight.uc.r.appspot.com/', 'json.parser')
    data = req.json()['values']
    df = pd.DataFrame.from_dict(data)
    df['h_in'] = df['h_in'].astype(int)
    max_value = df['h_in'].max()
    min_value = df['h_in'].min()
    total_value = df['h_in'].sum()
    print (max_value, min_value, total_value)
    grouped = df.groupby('h_in').agg({'first_name':'count'}).reset_index()
    grouped.columns = ['H', 'Counts']
    if param < min_value:
        print ('No match')
    elif param > total_value:
        print ('No match')
    else:
        grouped['result'] = param / grouped['H']
        grouped['residual'] = param % grouped['H']
        filtered = grouped[(grouped['residual']>=min_value) & (grouped['residual']<=max_value)]
        showResults(filtered,df)

if __name__ == "__main__":
    main(sys.argv[1])