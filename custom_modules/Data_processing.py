import pandas as pd
#import numpy as np

#описание модуля
def module_description():
    print('Функции:\n')

    print('Чтение датасета из Excel - get_df([path])')
    print('[path] - строка, путь к файлу\n')

    print('Удалить выбросы с помощью IQR - delete_outliers([df], [soft_mode = True])')
    print('[df] - датасет для обработки')
    print('[soft_mode = True] - режим, True - мягкое удаление выбросов',
    '\n если False - грубое удаление выбросов\n')

    print('Стандартизовать данные - standartize_data(df)')
    print('[df] - датасет для обработки\n')

    print('Нормализовать данные - normalize_data(df)')
    print('[df] - датасет для обработки\n')

    print('Удалить строки с пустыми значениями - delete_NANs(df)')
    print('[df] - датасет для обработки\n')

    print('Удалить строки с нулевыми значениями - delete_zeros(df)')
    print('[df] - датасет для обработки\n')

# чтение данных из файла Excel и возврат датафрейма
def get_df(path):
    file = pd.read_excel(path)
    file.rename(columns = {'Unnamed: 0' : 'Time Moment'}, inplace = True)
    df = file.drop(labels = [0], axis = 0) # удалить вторую строку оглавления

    columns = list(df.columns[1:])
    for col in columns: #настроить типы данных столбцов
        df[col] = df[col].astype(float)
    return df

# удалить выбросы из данных методом IQR
# soft_mode - рамки удаления выбросов, если True - удаляет только самые вопиющие выбросы
def delete_outliers(df, soft_mode = True):
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

    print("Размер датасета до обработки: ", dataset_size, " .После: ", df.shape)
    return df

# стандартизация данных (от -1 до 1)
def standartize_data(df):
    columns = list(df.columns[1:])

    for col in columns:
        df[col] = df[col] / df[col].max()

    return df

# нормализация данных (от 0 до 1)
def normalize_data(df):
    columns = list(df.columns[1:])

    for col in columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    return df

# удалить строки с пустыми значениями
def delete_NANs(df):
    dataset_size = df.shape
    df.dropna(inplace = True)
    print("Размер датасета до обработки: ", dataset_size, " .После: ", df.shape)
    return df

# удалить строки с нулевыми значениями
def delete_zeros(df):
    dataset_size = df.shape
    columns = list(df.columns[1:])

    for col in columns:
        df = df.loc[df[col] != 0]
    print("Размер датасета до обработки: ", dataset_size, " .После: ", df.shape)
    return df
