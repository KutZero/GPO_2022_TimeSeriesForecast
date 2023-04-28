""" Модуль для всяческой обработки данных перед обучением модели.

Функции:



Более подробнаую информацию можно получить так:

1) В Jupyter Notebook: "?[Имя модуля].[Имя функции]";
2) В общем виде: "print('[Имя модуля].[Имя функции].__doc__')";
3) В общем виде: "help([Имя модуля].[Имя функции])".
"""

import pandas as pd
import numpy as np

def to_list_of_64_values(x):
    # делим начальную строку на пары чисел
    # пары чисел тут - это просто строки
    x = str(x[1:-1]).split(',')
    x = np.array(x)

    x = x.astype(float)

    return x

# прочесть файл X_data_array-like.xlsx
def get_array_like_X_df(path: str):
    """Возвращает датафрейм, считанный из Excel файла.

    :param path: arg1
    :type path: string

    :rtype: DataFrame
    :return: Датафрейм с данными из файла
    """
    df = pd.read_excel(path,index_col=[0])
    df = df.apply(lambda x:
                  x.apply(to_list_of_64_values, convert_dtype=True))
    return df

# прочесть файл Y_data(binary_classification).xlsx
def get_Y_df(path: str):
    df = pd.read_excel(path,index_col=[0])
    return df

# кропы массива pandas имеют размер (PREP_image_size, PREP_image_size)
# после преобразования в numpy через to_numpy() размер тот-же,
# при том, что в каждой ячейке хранится массив из 64 чисел как объект
# для работы нужно преобразовать кроп к размеру (PREP_image_size, PREP_image_size, 64)
# чтобы каждый элемент массива был не объектом, а вещественным числом
def pandas_crop_to_image_like_numpy(df):
    x = df.to_numpy()
    return np.stack([np.stack([x[i,j] for i in range(x.shape[0])],axis=0)
        for j in range(x.shape[1])],axis=1)

# датафрейм размера 112 на 400 при размере кропа в 10
# преобразует в размер 120 на 400 (чтобы каждая сторона ровно
# делилась на размер кропа)
# новые строки добавляются за счет копирования старых
def reshape_df_for_future_crops(df, crop_size, crop_step):

    print('||||||||||||||||||')
    print('Df reshaping for exact splitting with crop_size')
    print('Original df size: ', df.shape)
    print('Crop windows height/width: ', crop_size)
    print('Crop windows step across rows and cols: ', crop_step)

    new_rows = crop_step - ((df.shape[0] - crop_size) % crop_step)
    new_cols = crop_step - ((df.shape[1] - crop_size) % crop_step)

    if new_rows != crop_step:
        df = pd.concat([df,
                        df.iloc[-1:-new_rows-1:-1]],
                        axis=0,ignore_index=True)
    if new_cols != crop_step:
        df = pd.concat([df,
                        df.iloc[:,-1:-new_cols-1:-1]],
                        axis=1,ignore_index=True)

    print('New df shape: ', df.shape)
    print('||||||||||||||||||\n')

    return df

# приведение к виду, который принимают на вход слои Conv2D
# (batch, channels, rows, cols) если data_format='channels_first'
# (batch, rows, cols, channels) если data_format='channels_last'
# тут выбран последний формат
# а так как "изображения" состоят из 64 измерений, то
# каналов либо 64, либо по 32
def reshape_X_df_to_image_like_numpy(df, crop_size, step = -1):

    print('||||||||||||||||||')
    print('X df reshaping to 4D')
    print('Original df size: ', df.shape)
    print('Crop windows height/width: ', crop_size)

    if step == -1:
        step = crop_size

    temp = np.concatenate([np.stack(
        [pandas_crop_to_image_like_numpy(
            df.iloc[i:i+crop_size,j:j+crop_size])
             for i in range(0,df.shape[0] - crop_size + 1, step)]
                , axis=0) for j in range(0,df.shape[1] - crop_size + 1, step)]
                    , axis=0)

    # поделим x выборку на значения времен и амплитуд
    X_time = temp[:,:,:,:32]
    X_amp = temp[:,:,:,32:]

    print('New X_time shape: ', X_time.shape)
    print('New X_amp shape: ', X_amp.shape)
    print('||||||||||||||||||\n')

    return (X_time,X_amp)

# приведение к нужному виду бинарных масок
def reshape_Y_df_to_image_like_numpy(df, crop_size, step = -1):

    print('||||||||||||||||||')
    print('Y df reshaping to 3D')
    print('Original df size: ', df.shape)
    print('Crop windows height/width: ', crop_size)

    if step == -1:
        step = crop_size

    Y_res = np.concatenate([np.stack(
        [df.iloc[i:i+crop_size,j:j+crop_size].to_numpy().astype('float32')
             for i in range(0,df.shape[0] - crop_size + 1, step)]
                , axis=0) for j in range(0,df.shape[1] - crop_size + 1, step)]
                    , axis=0)


    Y_res = np.expand_dims(Y_res,axis=3)

    print('New numpy shape: ', Y_res.shape)
    print('||||||||||||||||||\n')

    return Y_res

# преобразовать массив кропов numpy Y выборки размера (batch,rows,cols)
# в матрицу размера (rows,cols)
def reshape_3D_Y_numpy_to_2D(arr, rows_count, cols_count, crop_size):

    print('||||||||||||||||||')
    print('Y arr reshaping to 2D')
    print('Original arr size: ', arr.shape)
    print('Crop windows height/width: ', crop_size)

    crops_per_rows_count = int(rows_count/crop_size) # кол-во строк / размер кропа
    crops_per_cols_count = int(cols_count/crop_size) # кол-во столбцов / размер кропа

    temp  = np.concatenate([
                np.concatenate([arr[i + (j*crops_per_rows_count)]
                             for i in range(crops_per_rows_count)],axis=0)
                                 for j in range(crops_per_cols_count)],axis=1)

    print('New numpy shape: ', temp.shape)
    print('||||||||||||||||||\n')

    return temp

# вернет бинарную 1D маску, где 1 - для кропов с дефектами
# 0 - для кропов без дефектов
def calculate_crops_with_defects_positions(Y_arr, crop_size):

    print('||||||||||||||||||')
    print('Defects nums calculating')
    # Найдем на каких картинках есть дефекты
    defects_nums = list()
    for i in range(Y_arr.shape[0]):
        if np.sum(Y_arr[i] > 0) >= 1:
            defects_nums.append(True)
        else:
            defects_nums.append(False)

    defects_nums = np.array(defects_nums, dtype='bool')

    print(f'Для карт высотой и шириной в {crop_size}',
          f'и общим кличеством: {Y_arr.shape[0]}',
            f'дефекты присутствуеют на {np.sum(defects_nums)} картах',
              sep='\n')
    print('||||||||||||||||||\n')

    return defects_nums

def preprocess_data(X_time, X_amp, Y_mask, crop_size, X_time_max=0, X_amp_max=0):
    # стндартизуем данные
    # удалим кропы, в которых нет дефектов

    print('||||||||||||||||||')
    print('Data preprocessing')

    print('Orig X_time shape: ', X_time.shape)
    print('Orig X_amp shape: ', X_amp.shape)
    print('Orig Y_mask shape: ', Y_mask.shape)


    print('||||||||||||||||||')
    print('Data standartization')

    # стандартизуем данные
    if ((X_time_max == 0) and (X_amp_max == 0)):
        X_time_max = X_time.max()
        X_amp_max = X_amp.max()

    print(f'X_time_max: {X_time_max}')
    print(f'X_amp_max: {X_amp_max}')
    print()

    X_time = X_time / X_time_max
    X_amp = X_amp / X_amp_max

    print(f'X_time_max after standartization: {X_time.max()}')
    print(f'X_time_min after standartization: {X_time.min()}')
    print()

    print(f'X_amp_max after standartization: {X_amp.max()}')
    print(f'X_amp_min after standartization: {X_amp.min()}')

    print('||||||||||||||||||\n')

    print('||||||||||||||||||')
    print('Data with and witout defects splitting')

    # удалим кропы не содержищие дефекты
    defects_nums = calculate_crops_with_defects_positions(Y_mask, crop_size)

    X_time_def = X_time[defects_nums]
    X_amp_def = X_amp[defects_nums]
    Y_mask_def = Y_mask[defects_nums]
    Y_binary_def = np.ones(Y_mask_def.shape[0])

    X_time_non_def = X_time[~defects_nums]
    X_amp_non_def = X_amp[~defects_nums]
    Y_mask_non_def = Y_mask[~defects_nums]
    Y_binary_non_def = np.zeros(Y_mask_non_def.shape[0])


    print('X_time_def shape: ', X_time_def.shape)
    print('X_time_non_def shape: ', X_time_non_def.shape)
    print()

    print('X_amp_def shape: ', X_amp_def.shape)
    print('X_amp_non_def shape: ', X_amp_non_def.shape)
    print()

    print('Y_mask_def shape: ', Y_mask_def.shape)
    print('Y_mask_non_def shape: ', Y_mask_non_def.shape)
    print()

    print('Y_binary_def shape: ', Y_binary_def.shape)
    print('Y_binary_non_def shape: ', Y_binary_non_def.shape)

    print('||||||||||||||||||\n')
    print('||||||||||||||||||\n')

    return (X_time_def,X_time_non_def),\
        (X_amp_def,X_amp_non_def),\
        (Y_mask_def,Y_mask_non_def),\
        (Y_binary_def,Y_binary_non_def)

# применить аугментации к данным
# повернуть каждую картинку на 90 градусов 3 раза как пример
# для увеличения кол-ва данных для обучения
def augment_data(arr):
    print('||||||||||||||||||')
    print('Data augmentation')

    print('Orig arr shape: ', arr.shape)

    arr = np.concatenate([arr,
                            np.rot90(arr,1,[1,2]),
                            np.rot90(arr,2,[1,2]),
                            np.rot90(arr,3,[1,2])],axis=0)


    print('||||||||||||\nAfter 4 steps of 90 degree rotate')
    print('arr shape: ', arr.shape)

    arr = np.concatenate([arr,np.flip(arr,2)],axis=0)

    print('||||||||||||\nAfter horizontal full mirroring')
    print('arr shape: ', arr.shape)

    arr = np.concatenate([arr,np.flip(arr,1)],axis=0)

    print('||||||||||||\nAfter vertical full mirroring')
    print('arr shape: ', arr.shape)

    arr = np.concatenate([arr,np.roll(arr,int(arr.shape[1]/2),axis=1)],axis=0)

    print('||||||||||||\nAfter vertical half shifting')
    print('arr shape: ', arr.shape)

    arr = np.concatenate([arr,np.roll(arr,int(arr.shape[2]/2),axis=2)],axis=0)

    print('||||||||||||\nAfter horizontal half shifting')
    print('X_time_arr shape: ', arr.shape)

    print('||||||||||||||||||\n')
    return arr

# подаем на вход 3 numpy array
# X_time_arr, X_amp_arr, Y_arr
# они делятся на 3 выборки и функция возвращает
# X_time_train, X_time_val, X_time_test
# X_amp_train, X_amp_val, X_amp_test
# Y_train, Y_val, Y_test
def split_data_to_train_test_val_datasets(arr, val_percent):
    print('||||||||||||||||||')
    print('Data spliting to test, val and train datasets')

    for item in arr:
        print('Orig item shape: ', item.shape)
    print('')

    arr_train = np.concatenate([item[int(item.shape[0] * val_percent):] for item in arr], axis=0)
    arr_val = np.concatenate([item[:int(item.shape[0] * val_percent)] for item in arr], axis=0)

    print('Result arr_train shape: ', arr_train.shape)
    print('Result arr_val shape: ', arr_val.shape)

    print('')

    print('||||||||||||||||||\n')

    return arr_train,arr_val
