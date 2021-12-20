import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents


def get_all_tables(URL):

    response=requests.get(URL)


    soup = BeautifulSoup(response.text, 'html.parser')
    all_tables=soup.find_all('table',{'class':"wikitable"})

    table_list = []

    df=pd.read_html(str(all_tables))
    # convert list to dataframe

    for i in range(len(df)):
        table_heading = df[i].columns[0]


        col_names = list(df[i].iloc[0,:])


        df[i] = df[i].iloc[1:,:]
        df[i].columns = col_names
        temp = str(df[i].head().to_json(orient="records")).replace(':'," ")
        table_list.append((table_heading , temp))


    for i in table_list:
        if i[1] == '[]':
            table_list.remove(i)
    
    return table_list




# wikiurl="https://en.wikipedia.org/wiki/MS_Dhoni"
# print(get_all_tables(wikiurl))