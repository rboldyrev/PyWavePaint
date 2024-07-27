import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.gridspec import GridSpec
import os
import threading
import matplotlib.colors as mcolors
import json
import sys

# Перенаправляем stderr в os.devnull
sys.stderr = open(os.devnull, 'w')
# Функция для загрузки конфигурационного файла
def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

# Загрузка конфигурации
config = load_config('config.json')

step = config.get('step')  # Шаг, через сколько сохранять массив

# Функция для загрузки данных из файлов
def load_data(step):
    grids = []
    filename = f'./cash/results_{step   }.pkl'
    with open(filename, 'rb') as file:
        sparse_matrix = pickle.load(file)
        for matrix in sparse_matrix:
            grids.append(matrix.toarray())
    return grids

# Загрузка данных
grids = load_data(step)

# Список цветовых карт
cmap_options = ['inferno', 'viridis', 'plasma', 'magma', 'cividis',
                'autumn', 'bone', 'cool', 'copper', 'gray']
cmap_index = 0  # Начальный индекс цветовой карты

# Создание фигуры и настроек GridSpec
fig = plt.figure(figsize=(10, 6))
gs = GridSpec(1, 2, width_ratios=[3, 1], wspace=0.3)

# Создание изображения
ax = plt.subplot(gs[0])
im = ax.imshow(grids[0], cmap=cmap_options[cmap_index])
im.set_clim(vmin=0, vmax=1)

ax.format_coord = None

# Чтение из файла исходного состояния стены
with open('./cash/data_stan.pkl', 'rb') as file:
    sparse_matrix_stan = pickle.load(file)
stan = sparse_matrix_stan.toarray()  # Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть (бесконечная масса)  
# Создаем цветовую карту от прозрачного до белого, для того чтобы нарисовать белую стену
colors = [(1, 1, 1, 0), (1, 1, 1, 1)]  # RGBA формат (красный, зеленый, синий, альфа-канал)
cmap_name = 'transparent_to_white'
cmap_wall = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
paint_wall = ax.matshow(stan, cmap=cmap_wall)

# Добавление ползунка для выбора кадра
ax_frame_slider = plt.axes([0.1, 0.03, 0.8, 0.01], facecolor='lightgoldenrodyellow')
slider = Slider(ax_frame_slider, 'Frame', 0, len(grids) - 1, valinit=0, valstep=1)

# Добавление ползунка для изменения значения vmax
ax_vmax_slider = plt.axes([0.05, 0.15, 0.005, 0.5], facecolor='lightgoldenrodyellow')
vmax_slider = Slider(ax_vmax_slider, 'Vmax', 0.001, 2, valinit=1, orientation='vertical')

# Функция для изменения цветовой карты
def change_cmap(event):
    global cmap_index
    cmap_index = (cmap_index + 1) % len(cmap_options)
    im.set_cmap(cmap_options[cmap_index])
    cmap_button.label.set_text(f'{cmap_options[cmap_index]}')
    fig.canvas.draw_idle()

# Добавление кнопки для переключения цветовой карты
ax_cmap_button = plt.axes([0.02, 0.8, 0.08, 0.05], facecolor='lightcyan')
cmap_button = Button(ax_cmap_button, f'{cmap_options[cmap_index]}')
cmap_button.on_clicked(change_cmap)

def update(val):
    frame = int(slider.val)
    vmax = vmax_slider.val
    im.set_array(grids[frame])
    im.set_clim(vmin=0, vmax=vmax)
    fig.canvas.draw_idle()

slider.on_changed(update)
vmax_slider.on_changed(update)

# Функция для сохранения анимации в GIF
def save_gif():
    # Команда для сохранения GIF
    #os.system(f'python ./modules/animate_saver.py animation.mp4 --cmap={cmap_options[cmap_index]} --vmax={vmax_slider.val}')
    os.system(f'python ./modules/animate_saver.py --cmap={cmap_options[cmap_index]} --vmax={vmax_slider.val}')
              
def on_save_button_click(event):
    # Закрываем окно графика
    plt.close()

    # Запускаем сохранение GIF в отдельном потоке
    threading.Thread(target=save_gif).start()

# Добавление кнопки для сохранения GIF
ax_save_button = plt.axes([0.02, 0.7, 0.08, 0.05], facecolor='lightgreen')
save_button = Button(ax_save_button, 'Save')
save_button.on_clicked(on_save_button_click)

plt.show()  # Не блокирует выполнение программы
