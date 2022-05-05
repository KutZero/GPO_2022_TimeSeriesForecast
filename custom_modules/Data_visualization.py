import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.plotting import autocorrelation_plot

def module_description():
    print('Функции:\n')

    print('Нарисовать 4 графика данных по времени - draw_4_graphs(df)')
    print('[df] - датасет для обработки\n')

    print('Нарисовать 4 box-plot графика - draw_4_box_plot_graphs(df)')
    print('[df] - датасет для обработки\n')

    print('Нарисовать 4 графика автокорреляции (коррелограммы) - draw_4_autocorrelation_graphs(df)')
    print('[df] - датасет для обработки\n')

    print('Нарисовать 4 графика частоты встречающихся значений - draw_4_frewuencis_graphs(df)')
    print('[df] - датасет для обработки\n')

    print('Нарисовать 6 графиков зависимости данных друг от друга (без повторений) - draw_6_relations_graphs(df)')
    print('[df] - датасет для обработки\n')

    print('Вывести общее описание данных - describe_data(df)')
    print('[df] - датасет для обработки\n')

# вывести 4 графика зависимости значений столбца относительно времени (по графику на столбец)
def draw_4_graphs(df):
    plt.figure(figsize=(22, 20))
    i = 1
    columns = list(df.columns[1:])

    for col in columns:
        plt.subplot(4, 1, i)
        plt.plot(df['Time Moment'] , df[col], '-')
        plt.xlabel('Time Moment')
        plt.ylabel(col)
        plt.title(col)
        i+=1

    plt.show()

# вывести 4 графика box-plot (по графику на столбец)
def draw_4_box_plot_graphs(df):
    plt.figure(figsize=(22, 20))
    i = 1
    columns = list(df.columns[1:])

    for col in columns:
        plt.subplot(4, 1, i)
        df.boxplot(column = col, vert = False)
        plt.title(col)
        i+=1

    plt.show()

# вывести 4 графика автокорреляции (по графику на столбец)
def draw_4_autocorrelation_graphs(df):
    plt.figure(figsize=(22, 20))
    i = 1
    columns = list(df.columns[1:])

    for col in columns:
        plt.subplot(4, 1, i)
        autocorrelation_plot(df[col])
        plt.xlabel('Time Moment')
        plt.ylabel(col)
        plt.title(col)
        i+=1

    plt.show()

# нарисовать по 1 графику для каждого столбца, кроме даты, с частотой появления различных значений
def draw_4_frewuencis_graphs(df):
    columns = list(df.columns[1:])
    i = 1
    plt.figure(figsize=(16, 10))

    for col in columns:
        plt.subplot(2, 2, i)
        df[col].plot(kind='hist', density=1, bins=20, stacked=False, alpha=.5, color='grey')
        plt.title(col)
        i+=1

    plt.show()

# нарисовать 6 графиков зависимости каждого столбца от каждого (без повторений)
def draw_6_relations_graphs(df):
    columns = list(df.columns[1:])

    plt.figure(figsize=(16, 16))

    i = 1
    j = 1
    first_col = columns[0]

    for first_col in columns[:-1]:
        for col in columns[j:]:
            plt.subplot(3, 2, i)
            plt.plot(df[first_col] , df[col], 'bx')
            plt.title(first_col[10:] +  " + " +  col[10:])
            plt.xlabel(first_col)
            plt.ylabel(col)
            i+=1
        j+=1

    plt.show()

# описаниие данных
def describe_data(df):

    # вывод общего вида датафрейма
    display(df)

    # вывод списка типов данных столбцов
    print("\n", df.dtypes)

    # вывод списка типов данных столбцов
    print("\n", df.shape)

    # вывод общей инфы о каждой колонке
    print("Общее описание данных")
    display(df.describe())

    # вывод матрицы коэффициентов корреляции по Пирсону
    print("Таблица коэффициентов корреляции")
    display(df.corr(method='pearson'))
