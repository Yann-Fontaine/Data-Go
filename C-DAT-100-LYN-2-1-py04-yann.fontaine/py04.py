#!/usr/bin/env python
# coding: utf-8

# # EXERCISE 1

# 1/ Import requests and BeautifulSoup

# In[1]:


import requests
from bs4 import BeautifulSoup


# 2/ Storing parts of URI

# In[2]:


url = 'https://www.leboncoin.fr'
route = '/recherche'
payload = {'category': '41', 'text': 'totoro', 'price': '1-max'}
header = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}


# 3/ Requesting

# In[3]:


r = requests.get('https://www.leboncoin.fr/recherche', params = payload, headers = header)
print(r.content)


# 4/ Let's make the request up

# In[4]:


content = BeautifulSoup(r.content, 'html.parser')
print(content.prettify())


# 4/ Find title, price, date (format to ISO8601), city and postal code

# In[5]:


#browsing and filtering the requested elements
titles = content.find_all('p', {'class': '_1MlU1 _1qZ_s'})
#take the data
title_list = []
for title in titles:
    print(title.get_text())
    title_list.append(title.get_text())
print(title_list)


# In[6]:


#browsing and filtering the requested elements
prices = content.find_all('span', {'class': "_1C-CB"})
#taking the data
price_list = []
for price in prices:
    price_list.append(price.get_text())
print(price_list)
price = []
for price_b in price_list:
    price.append(price_b.rstrip('\xa0€'))
print(price)


# In[7]:


#browsing and filtering the requested elements
others = content.find_all('div', {'class': "_1UzWr"})
#buffering filtered data
other_list = []
for other in others:
    other_list.append(other.get_text())
#targetting the 'Livraison possible' strings and removing them
index_array = []
i=0
for value in other_list:
    if value == 'Livraison possible':
        index_array.append(i)
        i += 1
    else:
        i += 1
reverse_index = index_array[::-1]
for index in reverse_index:
    other_list.pop(index)
#buffering our filtered datas
location_list = []
j=1
date_list = []
k=2
while j<len(other_list) and k<len(other_list):
    location_list.append(other_list[j])
    j += 3
    date_list.append(other_list[k])
    k += 3
reloc_list = []
for loc in location_list:
    if loc[0:3] == 'Le ' or loc[0:3] == 'La ':
        loclist = list(loc)
        loclist[2] = '_'
        locstring = ''.join(loclist)
        reloc_list.append(locstring.split(' '))
    else:
        reloc_list.append(loc.split(' '))
#finally extracting location and zip code
location = []
zip_code = []
for reloc in reloc_list:
    location.append(reloc[0])
    zip_code.append(reloc[1])
#formatting the date
sep_d_h = []
for d_h in date_list:
    sep_d_h.append(d_h.split(', '))
m_d_list=[]
h_m_list=[]
for re_d_h in sep_d_h:
    m_d_list.append(re_d_h[0])
    h_m_list.append(re_d_h[1])
#changing "Hier" strings
from datetime import date, timedelta
today = date.today()
yesterday = date.today() - timedelta(days=1)
l=0
for date in m_d_list:
    if date == 'Aujourd\'hui':
        m_d_list[l] = today.strftime('%d %b')
        l += 1
    elif date == 'Hier':
        m_d_list[l] = yesterday.strftime('%d %b')
        l += 1
#separate months and days
months_list = []
days_list = []
re_m_d_list=[]
for m_d in m_d_list:
    re_m_d_list.append(m_d.split(' '))
months_list = []
days_list = []
for re_m_d in re_m_d_list:
    days_list.append(re_m_d[0])
    months_list.append(re_m_d[1])
#formatting months
month_list = []
for month in months_list:
    if month == 'Dec' or month == 'déc':
        month_list.append('12')
    elif month.lower() == 'nov':
        month_list.append('11')
    elif month.lower() == 'oct':
        month_list.append('10')
    elif month == 'Sep' or month == 'sept':
        month_list.append('09')
    elif month == 'Aug' or month == 'août':
        month_list.append('08')
    elif month == 'Jul' or month == 'juillet':
        month_list.append('07')
    elif month == 'Jun' or month == 'juin':
        month_list.append('06')
    elif month == 'May' or month == 'mai':
        month_list.append('05')
    elif month == 'Apr' or month == 'avr':
        month_list.append('04')
    elif month.lower() == 'mar':
        month_list.append('03')
    elif month == 'Feb' or month == 'fév':
        month_list.append('02')
    elif month.lower() == 'jan':
        month_list.append('01')
iso_date = []
d = 0
for month in month_list:
    iso_date.append(f'2020-{month}-{days_list[d]}T{h_m_list[d]}')
    d  += 1
print(location)
print(zip_code)
print(iso_date)


# 5/ Insert our data in a dataframe

# In[8]:


import pandas as pd

d = {'Title': title_list, 'Price': price, 'Location': location, 'Zip_Code': zip_code, 'Date': iso_date}
df = pd.DataFrame(data=d)
print(df)


# # EXERCISE 2

# In[9]:


df.to_pickle('./data.pickle')

