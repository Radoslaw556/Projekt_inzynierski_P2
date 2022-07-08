#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install jovian opendatasets --upgrade --quiet')


# In[2]:


import opendatasets as od


# In[3]:


dane_zrodlowe = 'https://www.kaggle.com/ananaymital/us-used-cars-dataset' 


# In[4]:



od.download(dane_zrodlowe)


# In[5]:


import pandas as pd
import numpy as np


# In[6]:


samochody_uzywane_csv = 'us-used-cars-dataset/used_cars_data.csv'


# In[7]:


get_ipython().run_cell_magic('time', '', 'samochody_uzywane_df = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows=1000000) ')


# In[8]:


samochody_uzywane_df.shape


# In[9]:


samochody_uzywane_df.head(2)


# In[10]:


wybrane_kolumny= ['city','daysonmarket','dealer_zip','engine_cylinders','frame_damaged','make_name','horsepower','listed_date','latitude','longitude','price','wheel_system','seller_rating','maximum_seating','sp_name']


# In[11]:


get_ipython().run_cell_magic('time', '', 'uzywane_samochody_probka = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows= 1500000, usecols=wybrane_kolumny)\nuzywane_samochody_probka.head(2)')


# In[12]:


samochody_uzywane_df.describe().round(3)


# In[13]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(uzywane_samochody_probka.dtypes)


# In[14]:


wybrane_typy_danych={
   'daysonmarket' : 'int32',
   'horsepower' :'float32',
   'latitude' : 'float32',
   'longitude' : 'float32',
   'price':'float32',
   'seller_rating': 'float32'
}


# In[15]:


get_ipython().run_cell_magic('time', '', "uzywane_samochody_probka = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows= 1500000, usecols=wybrane_kolumny, dtype=wybrane_typy_danych, parse_dates=['listed_date'])")


# In[16]:


uzywane_samochody_probka.shape


# In[17]:


uzywane_samochody_probka.head()


# In[18]:


uzywane_samochody_probka.isnull().sum()


# In[19]:


get_ipython().system('pip install pyarrow --upgrade --quiet')


# In[20]:


uzywane_samochody_probka.to_feather('samochody_uzywane.feather')


# In[21]:


ls -lh samochody_uzywane.feather


# In[22]:


get_ipython().run_cell_magic('time', '', "probka_danych_finalowa = pd.read_feather('samochody_uzywane.feather')")


# In[23]:


probka_danych_finalowa.shape


# In[24]:


probka_danych_finalowa.duplicated().sum()


# In[25]:


probka_danych_finalowa=probka_danych_finalowa.drop_duplicates()


# In[26]:


probka_danych_finalowa.shape


# In[27]:


probka_danych_finalowa.isnull().sum()


# In[28]:


probka_danych_finalowa.engine_cylinders.unique()


# In[29]:


probka_danych_finalowa['engine_cylinders'].isna().sum()


# In[30]:


probka_danych_finalowa = probka_danych_finalowa.replace(r'^\s+$', np.nan, regex=True)


# In[31]:


probka_danych_finalowa['engine_cylinders'] = probka_danych_finalowa['engine_cylinders'].fillna(value = 'Nieznany')


# In[32]:


probka_danych_finalowa['engine_cylinders'].isna().sum()


# In[33]:


probka_danych_finalowa.shape


# In[34]:


probka_danych_finalowa['frame_damaged'].value_counts()


# In[35]:


probka_danych_finalowa['frame_damaged'].isna().sum()


# In[36]:


probka_danych_finalowa['frame_damaged'] = probka_danych_finalowa['frame_damaged'].fillna(value = 'Nieznany')


# In[37]:


probka_danych_finalowa['frame_damaged'].isna().sum()


# In[38]:


probka_danych_finalowa.shape


# In[39]:


probka_danych_finalowa['frame_damaged'].unique()


# In[40]:


probka_danych_finalowa['horsepower'].isna().sum() 


# In[41]:


probka_danych_finalowa.horsepower.nunique()


# In[42]:


a = probka_danych_finalowa['horsepower'].describe()
a.round(2)


# In[43]:


import random
probka_danych_finalowa['horsepower'].fillna(random.uniform(200,300),inplace=True)


# In[44]:


a = probka_danych_finalowa.horsepower.describe()
a.round(2)


# In[45]:


probka_danych_finalowa['maximum_seating'].isna().sum()


# In[46]:


probka_danych_finalowa['maximum_seating'].unique()


# In[47]:


probka_danych_finalowa['maximum_seating'].value_counts()


# In[48]:


probka_danych_finalowa['maximum_seating'].fillna(value='5 seats', inplace=True)


# In[49]:


probka_danych_finalowa['maximum_seating'].isna().sum()


# In[50]:


probka_danych_finalowa['maximum_seating'].unique()


# In[51]:


probka_danych_finalowa = probka_danych_finalowa[~probka_danych_finalowa['maximum_seating'].isin(['--'])]


# In[52]:


probka_danych_finalowa['maximum_seating'].unique()


# In[53]:


def num(value):
  return value.split()[0]


# In[54]:


probka_danych_finalowa['maximum_seating'].astype(str)


# In[55]:


probka_danych_finalowa['maximum_seating'].astype(str)

probka_danych_finalowa['maximum_seating'] = probka_danych_finalowa['maximum_seating'].apply(num)


probka_danych_finalowa['maximum_seating'] = probka_danych_finalowa['maximum_seating'].astype(np.int32)


# In[56]:


probka_danych_finalowa['maximum_seating'].unique()


# In[57]:


probka_danych_finalowa['seller_rating'].isna().sum()


# In[58]:


probka_danych_finalowa['seller_rating'].value_counts()


# In[59]:


a = probka_danych_finalowa['seller_rating'].isnull()


# In[60]:


probka_danych_finalowa = probka_danych_finalowa[~a]


# In[61]:


probka_danych_finalowa['seller_rating'].isna().sum()


# In[62]:


probka_danych_finalowa['wheel_system'].isna().sum()


# In[63]:


probka_danych_finalowa['wheel_system'].unique()


# In[64]:


probka_danych_finalowa['wheel_system'].dropna(inplace=True)


# In[65]:


probka_danych_finalowa = probka_danych_finalowa[probka_danych_finalowa['wheel_system'].isin(['AWD', 'FWD', '4WD', 'RWD', '4X2'])]


# In[66]:


probka_danych_finalowa['wheel_system'].isna().sum()


# In[67]:


probka_danych_finalowa.isna().sum()


# In[68]:


probka_danych_finalowa.info()


# In[69]:


probka_danych_finalowa.reset_index(drop='index',inplace=True)


# In[70]:


probka_danych_finalowa


# In[71]:


probka_danych_finalowa.to_csv('wersja_finalowa.csv') 


# In[72]:


data_frame= pd.read_csv('wersja_finalowa.csv', low_memory = False)


# In[73]:


data_frame.drop('Unnamed: 0',axis=1,inplace=True)


# In[74]:


oczyszczony_data_frame = pd.read_csv('wersja_finalowa.csv', parse_dates=['listed_date'], low_memory = False)


# In[75]:


oczyszczony_data_frame.drop('Unnamed: 0',axis=1,inplace=True)


# In[76]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'


# In[77]:


oczyszczony_data_frame.columns


# In[78]:


oczyszczony_data_frame


# In[79]:


oczyszczony_data_frame.describe().round(3)


# In[104]:


fig = px.histogram(oczyszczony_data_frame, x="daysonmarket", marginal="box", title='Ilość dni na rynku samochodów używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')
fig.show()


# In[81]:


maksymalna_liczba_miejsc_w_samochodzie = oczyszczony_data_frame['maximum_seating'].value_counts()


# In[82]:


maksymalna_liczba_miejsc_w_samochodzie.plot.bar()
plt.title("Maksymalna liczba zarejestrowanych miejsc siedzących w samochodach używanych");
plt.xlabel("Maksymalna liczba zarejestrowanych miejsc siedzących");
plt.ylabel("Liczba samochodów");


# In[83]:


system_napedowy = oczyszczony_data_frame['wheel_system'].value_counts()


# In[84]:


system_napedowy.plot.pie(autopct='%1.2f%%',radius=1.8,figsize=(5,5),startangle=180);
plt.title('SYSTEM NAPĘDOWY W SAMOCHODACH UŻYWANYCH', y= 1.3);


# In[85]:


fig = px.histogram(oczyszczony_data_frame, x="price", marginal="box", title='Cena sprzedaży samochodów używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')


# In[86]:


oczyszczony_data_frame['price'].sort_values(ascending = True).iloc[1300000]


# In[87]:


a = oczyszczony_data_frame['price'].sort_values(ascending = True).iloc[:1300000]
df = pd.DataFrame(a)


# In[88]:


fig = px.histogram(df, x="price", marginal="box", title='Cena sprzedaży większości sprzedanych aut używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')


# In[89]:


sns.set_theme(style="ticks");
fig = sns.boxplot(x=oczyszczony_data_frame['seller_rating']);
fig.set(xlabel='Seller Ratings')
plt.title("Ocena sprzedawców samochodów używanych");
plt.show();


# In[110]:


px.scatter(oczyszczony_data_frame,x='horsepower',y='price',title='Cena względem mocy samochodu')


# In[113]:


df = oczyszczony_data_frame[['make_name']]
df = df.make_name.value_counts().head(30).sort_values(ascending = True)
df = pd.DataFrame(df)


# In[114]:


df.plot(kind='barh',figsize=(15,10),title='Liczba samochodów względem marki na rynku samochodów używanych ',xlabel='Nazwa marki',ylabel='Liczba samochodów');


# In[117]:


df = oczyszczony_data_frame[['city','price']]
df1 = df.groupby('city')[['price']].count().sort_values('price',ascending= False) 
df2 = df1.head(30).sort_values('price',ascending=True);


# In[118]:


df2.plot(kind='barh',legend=False,xlabel='City',ylabel='Liczba samochodów na sprzedarz', title='Top 30 miast z największą ilością samochodów używanych na sprzedaż',figsize=(13,8));


# In[95]:


oczyszczony_data_frame['year']=oczyszczony_data_frame['listed_date'].dt.year
oczyszczony_data_frame['month']=oczyszczony_data_frame['listed_date'].dt.month


# In[96]:


df1 = oczyszczony_data_frame.sort_values(by='price', ascending= True)
df1 = df1.iloc[:1300000]
df2 = df1.groupby(['year','month'])['price'].median()
df3 = df2.reset_index()
df4 = df3.pivot('year','month','price')
plt.figure(figsize = (16,8))
sns.heatmap(df4,fmt="d",cmap='Greens');


# In[119]:


dmg = oczyszczony_data_frame['frame_damaged'].value_counts()
dmg


# In[121]:


mylabels = ["Not Damaged","Unknown","Damaged"]
dmg.plot.pie(autopct='%1.2f%%',radius=1.5,figsize=(5,5),startangle=180,labels=mylabels);
plt.title('Auta uszkodzone vs auta nieuszkodzone', y= 1.1,x=1.5);


# In[122]:


df = oczyszczony_data_frame.groupby('make_name')['daysonmarket'].median().sort_values(ascending=True)
df.plot(kind='bar',figsize=(22,10),title='Czas sprzedaży samochodu danej marki',xlabel='Brands',ylabel='Number of Days');


# In[123]:


df5 = oczyszczony_data_frame[['make_name','price']]
df6 = df5.groupby('make_name')['price'].mean().round(0)
df7= {'Brand' : df6.index,
    'Price' : df6.values
      
}


# In[124]:


df8 = pd.DataFrame(df7)
df8.set_index('Brand')
df8 = df8.sort_values(by="Price",ascending=True)


# In[125]:


px.bar(df8,x='Brand',y='Price',barmode='group',range_y=[0,250000],title='Average Prices of Different Brands in Used Cars Market',width=1100,height=600)


# In[ ]:




