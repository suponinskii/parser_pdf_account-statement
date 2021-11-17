import tabula #Импортируем нужные библиотеки
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#tabula.convert_into_by_batch(pdf_path, output_format='csv', pages='all')


name_file = input('Enter the name of file: ')
pdf_path = 'C:/Users/ASUS/PycharmProjects/parse_pdf/'
num_month = int(input('Enter the number of first month for parsing: '))
num_month_end = int(input('Enter the nubmer of last month for parsing: '))

data = pd.read_csv(pdf_path + name_file, encoding='cp1251')
df = data.copy() #
df.columns = ['date', 'category', 'summa', 'rest']
df['date'] = df.date.str.extract(r'(\d\d.\d\d.\d\d\d\d)',expand=False)
df=df.tail(-2)
df['summa'].fillna(0, inplace=True)
df['rest'].fillna(0, inplace=True)
df=df.reset_index(drop=True)
df1=df.iloc[1::].copy().reset_index(drop=True)
df1=df1.reset_index(drop=True)
df1 = pd.concat([df, df1.category], axis=1)
df1.drop(df[df.summa == 0].index,axis=0, inplace=True)
df1.dropna(axis=0, inplace=True)
df1['summa'] = df1['summa'].str.replace('+','-')
df1['summa'] = df1['summa'].str.replace(',','.')
df1['summa'] = df1['summa'].str.replace(' ','')
df1['summa'] = df1['summa'].astype(float)
df1['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y")
df1 = df1.drop('rest', 1)
df1['cat']=df1.iloc[:,-1] + ' ' + df1.iloc[:,1]
df1 = df1.drop('category', 1)



def get_month(m):
  dfs = df1[df1['date'].dt.month == m]
  return dfs


def get_win(m):
  dfs = get_month(m)
  dfs = dfs[dfs['summa'] < 0]
  dfs.summa=dfs['summa'].abs()
  return dfs.summa.sum()


def get_food(m):
  dfs = get_month(m)
  dfs = dfs[dfs['cat'].str.contains('Супермаркеты|Рестораны')]
  win = get_win(m)
  return dfs.summa.sum()/win


def get_alco(m):
  dfs=get_month(m)
  dfs = dfs[dfs['cat'].str.contains('KRASNOE|BRISTOL')]
  win = get_win(m)
  return dfs.summa.sum()/win


def get_all(m):
  win = []
  month = []
  foods = []
  alco = []

  for i in range (m,num_month_end):
    win.append(round(get_win(i),1))
    month.append(i)
    foods.append(round(get_food(i),2))
    alco.append(round(get_alco(i),2))
    # plt.plot(month, fall)
    # plt.show()
  print('Доходы по месяцам: ', win)
  if sum(win)/float(len(win)) > win[-2]:
    print('Доходы снижаются')
  elif sum(win)/float(len(win)) < win[-1]:
    print('Доходы растут')
  else:
    print('Доходы в норме')
  print('% на еду по месяцам: ', foods, 'в среднем: ', round(sum(foods[:-1]) / float(len(foods[:-1])),3))
  print('% на алкомаркеты по месяцам: ', alco, 'в среднем: ', round(sum(alco[:-1])/float(len(alco[:-1])),4))


get_all(m=num_month)


def dec_to_pct(i):
  return int(i * 100)