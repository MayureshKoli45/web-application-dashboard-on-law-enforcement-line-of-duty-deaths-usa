# Here I am scrapping police deaths in United States of America from this "https://www.odmp.org/search/year" Website and then extracting into an excel file

# Importing required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Making a url variable of the website
url = "https://www.odmp.org/search/year"
url_ext = "?year="
years_list = [y for y in range(1791,2023)]

# Making a pandas dataframe to store data into a tabular form
df_col = ["Name", "Dept", "Date", "Cause"]
df = pd.DataFrame(columns=df_col)

# Looping through the years
for year in years_list:
    mine_url = url+url_ext+str(year)
    print(mine_url)

    # Requesting and Parsing url
    res = requests.get(mine_url)
    soup = BeautifulSoup(res.content, "html.parser")

    # Finding main tag of a page
    soup_main = soup.find("main", id="main")
    # Finding all "p" tags from the page
    soup_p = soup_main.find_all("p")
    
    # Transferring all text data of p tags into a list
    content = []
    for line in soup_p:
        # Be careful in this step because sometimes website include non necessary words in tags examples are given below in if condition
        # Code is correct make sure to debug by printing content list and by finding some unecessary words
        if line.text == "Nicholas County Sheriff's Department" or line.text == "United States Department of Homeland Security - Customs and Border Protection - United States Border Patrol" or line.text == "No law enforcement officers are known to have been killed in the line of duty in "+str(year)+".":
            break
        content.append(line.text)

    while len(content) > 0 :
        # Transferring all text data from content list to new list in df_col format
        l = []
        while len(l) < 4 :
            l.append(content.pop(0))
        
        # Appending items of new list into pandas dataframe
        df.loc[len(df.index)] = l  

# Extracting pandas dataframe to Excel
filename = "police_deaths.xlsx"
df.to_excel(filename)

# For any doubts feel free to email me on kolimayuresh450@gmail.com i will try to make you understand this code
        


