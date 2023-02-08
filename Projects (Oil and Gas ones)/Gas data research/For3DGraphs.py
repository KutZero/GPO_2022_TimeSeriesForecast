import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from IPython.display import display
from pandas.plotting import autocorrelation_plot

def get_df(path: str):
    df = pd.read_csv(path, delimiter=';')
    return df


def draw_one_tube_by_magnitude(df):
    step_angle = float(360 / len(df))  # угол между двумя точками измерения на 1 датчике
    circles_num = len(df[0].split(sep=','))  # кол-во моментов измерения для 1 датчика
    dat_num = df.shape[0]  # кол-во точек измерения на датчике

    x0 = float(0)  # координата центра окружности
    y0 = float(0)  # координата центра окружности
    r = float(0)  # радиус окружности
    x = []
    y = []
    z = []

    print(dat_num)

    for j in range(circles_num):
        for i in range(dat_num):
            temp_str = df[i].split(sep=',')[
                j]  # строка время + амплитуда для одной из 114 точек 1 датчика для 1 момента времени
            print(temp_str, end='\t')

            z.append(j)

            r = abs(
                float(temp_str.split(sep=':')[1]))  # отдаление точки от цента (радиус окружности) только положительные

            x.append(x0 + r * math.cos(math.radians(step_angle * i)))
            y.append(y0 + r * math.sin(math.radians(step_angle * i)))

            print(f'x: {x[i]},\ty: {y[i]},\tz: {z[i]},\ti: {i}')

    return x, y, z

path_to_data = 'data\\Новые данные\\Run1\\run1_WM32_data.csv'

first_df = get_df(path_to_data)
col_df = first_df['detector_0']

x0,y0,z0 = draw_one_tube_by_magnitude(col_df)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x0, y0, z0, 'red')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
