""" Модуль для всяческой обработки данных перед обучением модели.

Функции:

Чтение датасета из Excel:
get_df([path])

Удалить выбросы с помощью IQR:
delete_outliers([df], [soft_mode = True])

Стандартизовать данные:
standartize_data([df])

Нормализовать данные:
normalize_data([df])

Удалить строки с пустыми значениями:
delete_NANs([df])

Удалить строки с нулевыми значениями:
delete_zeros([df])

Более подробнаую информацию можно получить так:

1) В Jupyter Notebook: "?[Имя модуля].[Имя функции]";
2) В общем виде: "print('[Имя модуля].[Имя функции].__doc__')";
3) В общем виде: "help([Имя модуля].[Имя функции])".
"""

import pandas as pd
import numpy as np

# чтение данных из файла Excel и возврат датафрейма
def get_df(path: str):
    """Возвращает датафрейм, считанный из Excel файла.

    :param path: arg1
    :type path: string

    :rtype: DataFrame
    :return: Датафрейм с данными из файла
    """
    file = pd.read_excel(path)
    file.rename(columns = {'Unnamed: 0' : 'Time Moment'}, inplace = True)
    df = file.drop(labels = [0], axis = 0) # удалить вторую строку оглавления

    columns = list(df.columns[1:])
    for col in columns: #настроить типы данных столбцов
        df[col] = df[col].astype(float)

    return df

# удалить выбросы из данных методом IQR
# soft_mode - рамки удаления выбросов, если True - удаляет только самые вопиющие выбросы
def delete_outliers(df: pd.DataFrame, soft_mode: bool = True):
    """Возвращает датафрейм, очищенный от выбросов IQR методом.

    :param df: arg1
    :type df: DataFrame
    :param soft_mode: arg2, defaults to True
    :type soft_mode: Boolean, optional

    :rtype: DataFrame
    :return: Датафрейм без выбросов
    """
    columns = list(df.columns[1:])
    dataset_size = df.shape

    if soft_mode:
        per1,per2 = 0.025, 0.975
    else:
        per1,per2 = 0.25, 0.75

    for col in columns:
        print('\n\tФильтрация по: ', col)
        row_before = df.shape[0]
        Q1 =  df[col].quantile(per1)
        Q3 = df[col].quantile(per2)
        IQR = Q3 - Q1
        df = df[(df[col] > (Q1-1.5*IQR)) & (df[col] < (Q3+1.5*IQR))]
        print('\tУдалено строк: ', row_before - df.shape[0], "\n")

    print("Размер датасета:\nдо обработки: ", dataset_size, "\nпосле: ", df.shape,
        "\nудалено строк: ", (dataset_size[0]-df.shape[0]))

    return df

# стандартизация данных (от -1 до 1)
def standartize_data(df: pd.DataFrame):
    """Возвращает стандартизированный датафрейм.

    :param df: arg1
    :type df: DataFrame

    :rtype: DataFrame
    :return: Стандартизированный датафрейм
    """
    columns = list(df.columns[1:])

    for col in columns:
        df[col] = df[col] / df[col].max()

    return df

# нормализация данных (от 0 до 1)
def normalize_data(df: pd.DataFrame):
    """Возвращает нормализованный датафрейм.

    :param df: arg1
    :type df: DataFrame

    :rtype: DataFrame
    :return: Нормализованный датафрейм
    """
    columns = list(df.columns[1:])

    for col in columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    return df

# удалить строки с пустыми значениями
def delete_NANs(df: pd.DataFrame):
    """Возвращает датафрейм, очищенный от NAN значений.

    :param df: arg1
    :type df: DataFrame

    :rtype: DataFrame
    :return: Датафрейм без NAN значений
    """
    dataset_size = df.shape
    df.dropna(inplace = True)
    print("Размер датасета:\nдо обработки: ", dataset_size, "\nпосле: ", df.shape,
        "\nудалено строк: ", (dataset_size[0]-df.shape[0]))

    return df

# удалить строки с нулевыми значениями
def delete_zeros(df: pd.DataFrame):
    """Возвращает датафрейм, очищенный от нулевых значений.

    :param df: arg1
    :type df: DataFrame

    :rtype: DataFrame
    :return: Датафрейм без нулевых значений
    """
    dataset_size = df.shape
    columns = list(df.columns[1:])

    for col in columns:
        df = df.loc[df[col] != 0]

    print("Размер датасета:\nдо обработки: ", dataset_size, "\nпосле: ", df.shape,
        "\nудалено строк: ", (dataset_size[0]-df.shape[0]))

    return df
