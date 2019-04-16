#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
import re


# In[2]:


###爬取
data = pd.DataFrame()    
url_list = []
for i in range(1, 11):
    url = 'http://www.espn.com/nba/salaries/_/page/%s' % i
    url_list.append(url)
for url in url_list:
    data = data.append(pd.read_html(url), ignore_index=True)
data = data[[x.startswith('$') for x in data[3]]]
data.to_csv('NAB_salaries.csv',header=0, index=False)


# In[2]:


NBA_salary=pd.read_csv('NAB_salaries.csv',names=['Rank','Name','Team','Salary'])
NBA_salary.head()


# In[3]:


NBA_salary.info()


# In[56]:


###另一种方式
money2int = lambda x: "".join(filter(str.isdigit, x))
team_name = lambda x: x.split()[-1]
get_name = lambda x: x.split(',')[0]


# In[6]:


###分割Name，最好用find方式
def cut_word(word):
    pos = word.find(',')
    if pos != -1:
        Name=word[: pos]
    return Name


# In[7]:


def cut_word2(word):
    pos = word.find(',')
    if pos != -1:
        Position=word[pos+1:]
    return Position


# In[8]:


NBA_salary['Position']=NBA_salary.Name.apply(cut_word2)
NBA_salary['Name']=NBA_salary.Name.apply(cut_word)


# In[9]:


NBA_salary=pd.DataFrame(NBA_salary, columns=['Rank','Name','Position','Team','Salary']) 
NBA_salary.head()


# In[12]:


NBA_salary['Position'].unique()


# In[14]:


###salary字段的处理
NBA_salary['Salary']=NBA_salary['Salary'].str[1:]


# In[15]:


NBA_salary.head()


# In[18]:


NBA_salary.to_csv('C:/Users/Carman/Desktop/NBA_Player_Salaries.csv',header=0, index=False)
##配合excel的使用


# In[20]:


NBA_salary=pd.read_csv('C:/Users/Carman/Desktop/NBA_Player_Salaries.csv',names=['Rank','Name','Position','Team','Salary'])
NBA_salary.head()


# In[21]:


def cut_team(x):
    team_name = x.split()[-1]
    return team_name 


# In[22]:


NBA_salary['Team']=NBA_salary.Team.apply(cut_team)    
NBA_salary.head()
###使用lambda更加便利的解决，分割
###salary['POSITION'] = salary['POSITION'].map(lambda x: x.split(',')[1])


# In[23]:


team_salary_rank=NBA_salary.groupby(['Team'])['Salary'].sum().reset_index().sort_values(['Salary'],ascending=False)
team_salary_rank=team_salary_rank.reset_index(drop=True)
team_salary_rank.head()


# In[24]:


team_salary_rank.index = team_salary_rank['Team']
fig=plt.figure(figsize=(8,8),dpi=100)
ax = fig.add_subplot(111)
plt.barh(team_salary_rank['Team'],team_salary_rank['Salary'],)
plt.ylabel('team')
plt.xlabel('salary')
plt.title('球队队员工资总和($)')  
plt.axvline(x=60000000, c='g', ls='-.', lw=2)
plt.show()


# In[25]:


team_salary_rank.boxplot(column='Salary')


# In[28]:


plt.hist(team_salary_rank['Salary'],bins=15,color = 'g',histtype = 'bar',rwidth = 0.95,alpha = 0.6)
##设置图表的属性能使图表更加清晰


# In[29]:


###按所在队来分割球员,继续思考
Spurs_salary=NBA_salary[NBA_salary['Team']=='Spurs']
Spurs_salary=Spurs_salary.reset_index(drop=True)
Spurs_salary
#Spurs_salary.boxplot(column='Salary')
#Spurs_salary.Salary.mean()


# In[32]:


###构造DataFrame的方式
team_salary = pd.DataFrame({'Cavaliers': NBA_salary[NBA_salary['Team'] == 'Cavaliers']['Salary'],
                     'Warriors': NBA_salary[ NBA_salary['Team'] == 'Warriors']['Salary'],
                     'Rockets': NBA_salary[NBA_salary['Team'] == 'Rockets']['Salary'],
                     'Lakers': NBA_salary[NBA_salary['Team'] == 'Lakers']['Salary'],
                     'Spurs': NBA_salary[NBA_salary['Team'] == 'Spurs']['Salary']
                     })
plt.ylabel("球员薪资（单位：$）")
plt.xlabel("球队名") 
team_salary.boxplot()
plt.show()


# In[33]:


Position_salary=NBA_salary.groupby(['Position'])['Salary'].sum().reset_index().sort_values(['Salary'],ascending=False)
Position_salary=Position_salary.reset_index(drop=True)
Position_salary


# In[34]:


Position_conut=NBA_salary.groupby(['Position'])['Name'].count().reset_index().sort_values('Name',ascending=False)
Position_conut=Position_conut.rename(columns={'Name': 'Number'}) 


# In[35]:


Position_salary=pd.merge(Position_salary,Position_conut,how='left',on='Position')
Position_salary


# In[36]:


Position_salary['Salary_mean']=Position_salary['Salary']/Position_salary['Number']
Position_salary['Salary_mean']=Position_salary['Salary_mean'].astype('int64')
Position_salary
###计算平均薪资
###NBA_salary.Salary.mean()   #联盟所有球员的平均薪资
### 各个位置的平均薪资
### NBA_salary.groupby(['Position'])['Salary'].mean().astype('int64')   也可以用mean()直接计算
###NBA_salary.groupby(['Team'])['Salary'].mean().astype('int64')   计算每只球队的平均薪资


# In[37]:


list(Position_salary.Position)


# In[38]:


fig=plt.figure(figsize=(8,8))
plt.bar(Position_salary['Position'],Position_salary['Salary'],color='b',align='center', alpha=0.4)
plt.xlabel('position')
plt.ylabel('salary（$B）')
plt.title('位置薪资分布图')


# In[39]:


###饼图比列
labels=['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F']
explode = [0.1, 0, 0, 0, 0,0,0]
fig=plt.figure(figsize=(8,8))
plt.pie(Position_salary['Salary'], explode = explode,
        labels = labels, autopct='%.2f',
        startangle = 180, shadow = True)
plt.axis('equal')  
plt.title('各位置薪资占比图')
plt.show()


# In[35]:


###内嵌环形图
plt.figure(figsize = (8, 8))
labels=['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F']
colors = ['c', 'r', 'y', 'g', 'gray','b','m']
# 外环
wedges1, texts1, autotexts1 = plt.pie(Position_salary['Salary'],
    autopct='%.2f',
    radius = 1,
    pctdistance = 0.85,
    colors = colors,
    startangle = 180,
    textprops = {'color': 'w'},
    wedgeprops = {'width': 0.3, 'edgecolor': 'w'}
)
# 内环
wedges2, texts2, autotexts2 = plt.pie(Position_salary['Salary_mean'],
    autopct='%.2f',
    radius = 0.7,
    pctdistance = 0.75,
    colors = colors,
    startangle = 180,
    textprops = {'color': 'w'},
    wedgeprops = {'width': 0.3, 'edgecolor': 'w'}
)
plt.legend(wedges1,labels,fontsize = 12,title = '位置列表',loc='upper left',bbox_to_anchor = (1, 0.6))
# 设置文本样式
plt.setp(autotexts1, size=15, weight='bold')
plt.setp(autotexts2, size=15, weight='bold')
plt.setp(texts1, size=15)
plt.title('NBA位置薪资分析图', fontsize=20)
plt.show()


# In[18]:


plt.bar(Position_salary['Position'],Position_salary['Salary_mean'],color='c',align='center', alpha=0.4)
plt.xlabel('position')
plt.ylabel('salary（$M）')
plt.title('各位置平均薪资')


# In[ ]:


###关键是关联，把球员的薪资和球员的表现结合起来看

