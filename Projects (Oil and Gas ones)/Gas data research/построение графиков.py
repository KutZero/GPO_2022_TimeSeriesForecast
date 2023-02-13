#from scipy.signal import savgol_filter
#import tensorflow as tf

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.plotting import autocorrelation_plot
from matplotlib import ticker
#import sys
#sys.path.append('custom_modules')

#import Data_processing as dp
#import Data_visualization as dv
path_to_data = 'data\\Новые данные\\Run1\\run1_WM32_data.csv'
row_num = 73 # Номер строки, который мы хотим взять для анализа (от 0 до 114)
determ_nums = [0] # Какие измерения хотим посмотреть (от 0 до 30 или 31)
row_nums_list=[i for i in range(45,55)]
def get_df(path: str):
    df = pd.read_csv(path, delimiter=';')
    return df
# Чтение данных из файла
first_df = get_df(path_to_data)
# Удаляем пустые столбцы
print(first_df.shape)
first_df = first_df.T
for col in first_df.columns:
    first_df = first_df.loc[~first_df[col].isin(['--'])]
first_df = first_df.T
print(first_df.shape)
# Что прочли из файла
display(first_df)
# Вырезаем интересующую строку из начального датафрейма
# Разделяем значения её ячеек по строкам (разделитель - ","). Считаем каждый датчик провел 31 измерение за 1 пуск 
# Выводим полученный датафрейм со столбцами - номерами датчиков и строками - номерами измерений
# В каждой ячейке пара время + амплитуда 

# Датафрейм со всеми измерениями без деления на время и амплитуду
#determines_df = first_df.iloc[:1,2:].squeeze().str.split(pat=',', expand=True).T

def proccess_func(k, row_num):
    determines_df = first_df.iloc[row_num,2:].str.split(pat=',', expand=True).T
    display(determines_df)
    # Берем 1 строку из determines_df, то есть определенный номер измерения для всех датчиков
    # Делим пары чисел в ячейках на столбцы "Время" и "Амплитуда"

    # Список из датафреймов, каждый из которых описывает время и амплитуду раздельно для каждого измерения
    divided_determines_dfs_list = list()

    for i in determ_nums:
        temp = determines_df.iloc[i,:].str.split(pat=':', expand=True).T
        temp.rename(index = {0 : 'Time', 1: 'Amplitude'}, inplace = True)
        temp = temp.T
        temp = temp.astype(float)
        print(temp.dtypes)
        divided_determines_dfs_list.append(temp)
    # Вывод датафреймов, описывающих измерения и номера этих измерений для проверки
    # Номер измерения НАД датафреймом
    # кол-во элементов в determ_nums и divided_determines_dfs_list равно
    itr = iter(determ_nums)
    for df_item in divided_determines_dfs_list:
        print(f"Для измерения номер: {next(itr)}")
        display(df_item.T)
    # Считаем что выводим только 1 измерение (номер 0)
    # Можно посмотреть ВСЕ значения времени и амплитуды для 22 строки исходного .csv файла
    # Измерение (т.е. номер одной из пар чисел в каждой ячейке) - 0
    i = 0
    while(i < 400):
        display(divided_determines_dfs_list[0].T.iloc[:,i:i + 10])
        i+=10
    for df_item in divided_determines_dfs_list:
        detecters_left_border = 7
        detecters_right_border =31
        x = [j for j in range(detecters_left_border, detecters_right_border)]
        y = [k]*(detecters_right_border-detecters_left_border)
        z = df_item['Amplitude'][detecters_left_border:detecters_right_border]
    return x,y,z
fig = plt.figure()
fig.set_figwidth(20)
fig.set_figheight(16)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Номер датчика', fontsize=15)
ax.set_ylabel('Строка', fontsize=15)
ax.set_zlabel('Амплитуда', fontsize=15)
k=0
for num in row_nums_list:
    x,y,z=proccess_func(k,num)
    ax.plot(x, y, z, label='parametric curve')
    k+=1
plt.show()