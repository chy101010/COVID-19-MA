#!/usr/bin/env python
# coding: utf-8

# In[33]:


import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import date 
import csv


# In[34]:


url = 'https://www.worldometers.info/coronavirus/country/us/'
result = requests.get(url)
result.status_code
result = result.text


# In[35]:


# adds MA today's data into the Covid-19.csv
def updateToday():
    getCsv()
    data = getData('Massachusetts')
    addCsv(data)
    print(data)
updateToday()


# In[36]:


soup = BeautifulSoup(result, 'html.parser')

# returns the an Array of [date, number of total cases, new cases]
def getData(state):
    # locates the table of contents for all states  
    table = soup.find(id = 'usa_table_countries_today')
    states = table.contents[3]
    
    notFound = True
    index = 1
    
    state_content = ""
    # locate the table contents for the given state
    while notFound:
        someState = str(states.contents[index])
        if(someState.find(state) != -1):
            notFound = False
            state_content = states.contents[index]
        else:
            index = index + 1
   
    # gets the total case & new cases
    data = dataExtract(state_content) 
    
    # gets the date in #month.#days form
    date = getDate()
    
    return [date, data[0], data[1]] 

# returns the number of new cases and current total cases from the given 
# table of contents of a state
def dataExtract(content):
    # string containing the number of cases
    stringCase = str(content.contents[3])        
    # string containing the number of new cases
    stringNewCase = str(content.contents[5])
    # total number of new cases in the state
    
    # checking whether the new cases are removed from the web
    checkerNewCase = extractCounts(stringNewCase)
    if checkerNewCase == "":
        numNewCase = 0
    else:
        numNewCase = int(checkerNewCase.replace(",", ""))
        
    # total number of cases in the state
    numCase = int(extractCounts(stringCase).replace(",", ""))
    return numCase, numNewCase
    
# extracts the count from the given input
# the input should be in the format of ("someString>123,123 </td>)
def extractCounts(input):
    index = len(input) - len(" </td>")
    stringAccumulator = ""
    
    while (input[index - 1]).isdigit() or input[index - 1] == ",":
        index = index - 1
        stringAccumulator = input[index] + stringAccumulator 
        
    return stringAccumulator

# Get date in #month.#days form
def getDate():
    lDate = str(date.today())
    sDate = lDate[5:len(lDate)]
    numDate = float(sDate.replace("-", "."))
    return numDate


# In[37]:


# creates the csv if not created 
def getCsv():
    fields = ['Date', 'Total Cases', 'New Cases']
    with open('Covid-19.csv', newline = '') as f:
        reader = csv.reader(f)
        csv_heading = next(reader)
        if np.size(csv_heading) == 0:
            with open('Covid-19.csv', 'w', newline='') as covidfile:
                cvsWritter = csv.writer(covidfile)
                cvsWritter.writerow(fields)

# adds the given data in the csv is not yet exist
# wont add if the total cases or date is the same  
def addCsv(dat):
    ArrayDate = []
    ArrayCases = []
    with open('Covid-19.csv', newline = '') as f:
        reader = csv.reader(f)
        csv_heading = next(reader)
        for row in reader:
            ArrayDate = np.append(ArrayDate, row[0])
            ArrayCases = np.append(ArrayCases, row[1])                  
            
    with open('Covid-19.csv', 'a', newline='') as covidfile:
        cvsWritter = csv.writer(covidfile)
        if not repeated(ArrayDate, dat[0]) and not repeated(ArrayCases, dat[1]) :
            cvsWritter.writerow(dat)


# In[38]:


# determines whether this given num is in the arr
def repeated(arr, num):
    checker = False
    arrayLength = np.size(arr)
    index = 0
    
    while index < arrayLength and not checker:
        if float(arr[index]) == num:
            checker = True
        index = index + 1
    return checker

