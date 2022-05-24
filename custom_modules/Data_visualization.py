""" Модуль для визуализации данных.

Функции:

Нарисовать 4 графика данных по времени:
draw_4_graphs([df])

Нарисовать 4 box-plot графика:
draw_4_box_plot_graphs([df])

Нарисовать 4 графика автокорреляции (коррелограммы):
draw_4_autocorrelation_graphs([df])

Нарисовать 4 графика частоты встречающихся значений:
draw_4_frewuencis_graphs([df])

Нарисовать 4 графика для двух датафреймов с наложением (по графику на столбец):
draw_4_graphs_with_overlay_for_2_df([df1], [df2])

Нарисовать 6 графиков зависимости данных друг от друга (без повторений):
draw_6_relations_graphs([df])

Вывести общее описание данных:
describe_data([df])

Более подробнаую информацию можно получить так:

1) В Jupyter Notebook: "?[Имя модуля].[Имя функции]";
2) В общем виде: "print('[Имя модуля].[Имя функции].__doc__')";
3) В общем виде: "help([Имя модуля].[Имя функции])".
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.plotting import autocorrelation_plot

# вывести 4 графика зависимости значений столбца относительно времени (по графику на столбец)
def draw_4_graphs(df: pd.DataFrame):
    """Рисует 4 графика для каждого значащего столбца датафрейма.

    :param df: arg1
    :type df: DataFrame
    """
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
def draw_4_box_plot_graphs(df: pd.DataFrame):
    """Рисует 4 box-plot графика для каждого значащего столбца датафрейма.

    :param df: arg1
    :type df: DataFrame
    """
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
def draw_4_autocorrelation_graphs(df: pd.DataFrame):
    """Рисует 4 графика автокорреляции (коррелограммы) для каждого значащего столбца датафрейма.

    :param df: arg1
    :type df: DataFrame
    """
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
def draw_4_frewuencis_graphs(df: pd.DataFrame):
    """Рисует 4 графика частоты встречающихся значений для каждого значащего столбца датафрейма.

    :param df: arg1
    :type df: DataFrame
    """
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
def draw_6_relations_graphs(df: pd.DataFrame):
    """Рисует 6 графиков зависимости каждого значащего столбца от каждого для датафрейма.

    :param df: arg1
    :type df: DataFrame
    """
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

# вывсести 4 графика для двух датафреймов с наложением (по графику на столбец)
def draw_4_graphs_with_overlay_for_2_df(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Рисует 4 графика для двух датафреймов с наложением (по графику на столбец).
    Первый параметр - начальные данные, второй - обработанные данные.

    :param df1: arg1
    :type df1: DataFrame
    :param df2: arg2
    :type df2: DataFrame
    """
    plt.figure(figsize=(22, 20))
    columns = list(df1.columns[1:])

    i = 1
    # Проверка, имеют ли датафреймы одинаковые столбцы
    if (columns != list(df2.columns[1:])):
        return 0

    for col in columns:
        plt.subplot(4, 1, i)
        plt.plot(df1['Time Moment'] , df1[col], '-', label = "Начальные данные")
        plt.plot(df2['Time Moment'] , df2[col], '-', label = "Обработанные данные")
        plt.xlabel('Time Moment')
        plt.ylabel(col)
        plt.title(col)
        plt.legend()
        i+=1

    plt.show()

# описаниие данных
def describe_data(df: pd.DataFrame):
    """Выводит общее описание данных.

    А именно:
    1) Общий вид датафрейма как таблица
    2) Список типов столбцов
    3) Размерность датафрейма
    4) Таблицу с общим описанием столбцов
    5) Матрицу линейных коэффициентов корреляции

    :param df: arg1
    :type df: DataFrame
    """

    # вывод общего вида датафрейма
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\Общий вид датафрейма")
    display(df)

    # вывод списка типов данных столбцов
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\Список типов столбцов")
    print("\n", df.dtypes)

    # вывод общей инфы о каждой колонке
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\Общее описание данных")
    display(df.describe())

    # вывод матрицы коэффициентов корреляции по Пирсону
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\Таблица коэффициентов корреляции")
    display(df.corr(method='pearson'))
