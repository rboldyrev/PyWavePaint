import numpy as np  
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from progress.bar import Bar
from scipy.sparse import csr_matrix
import json
import gc
import os

# Функция для загрузки конфигурационного файла
def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

# Функция для сохранения промежуточных результатов
def save_intermediate_results(grids, step):
    filename = f'./cash/results_{step}.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(grids, file)

# Загрузка конфигурации
config = load_config('config.json')

# Присвоение значений переменным
frames = config.get('frames')
k = config.get('k')
step = config.get('step') #шаг, через сколько сохранять массив
bar = Bar('Вычисление...', max=frames)  # Создаем прогресс бар

# Чтение из файла исходного волны
with open('./cash/data_grid.pkl', 'rb') as file:
    sparse_matrix_grid = pickle.load(file)

# Чтение из файла исходного стены
with open('./cash/data_stan.pkl', 'rb') as file:
    sparse_matrix_stan = pickle.load(file)

# Объявляем переменные 
progress_ = 0  # Начальный прогресс рендера анимации  
N = len(sparse_matrix_grid.toarray())  # Размер сетки, например N на N  

# Инициализируем массивы для хранения состояния каждого шага анимации
grids = []
speeds = []
forces = []

grids.append(np.zeros((N, N), dtype=np.float16))
speeds.append(np.zeros((N, N), dtype=np.float16))
forces.append(np.zeros((N, N), dtype=np.float16))

stan = sparse_matrix_stan.toarray()  # Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть (бесконечная масса)  

# Преобразование обратно в плотный формат (для проверки)
grids[0] = sparse_matrix_grid.toarray()

def get_grid(grids, speeds, forces):
    global progress_
    grid = np.copy(grids[progress_ % step])  
    speed = np.copy(speeds[progress_ % step])
    force = np.copy(forces[progress_ % step])  
    progress_ += 1  # Считаем прогресс на каждом шаге  
    force = k * (np.roll(grid, 1, axis=0) + np.roll(grid, 1, axis=1) +
                 np.roll(grid, -1, axis=0) + np.roll(grid, -1, axis=1) - 4 * grid)
    speed = speed + force
    grid = grid + speed * (1 - stan)

    grids.append(grid)
    speeds.append(speed)
    forces.append(force)
    gc.collect()


# Основная функция, которая вызывается на каждом шаге   
for i in range(frames):
    get_grid(grids, speeds, forces)
    if (i + 1) % step == 0:
        # Сохраняем промежуточные результаты каждые step кадров
        save_intermediate_results([csr_matrix(matrix) for matrix in grids], i + 1)
        grid_temp = grids[progress_ % step + step]
        speed_temp = speeds[progress_ % step + step]
        force_temp = forces[progress_ % step + step]
        # Очистка промежуточных результатов из памяти, чтобы освободить место
        grids = []
        speeds = []
        forces = []
        gc.collect()

        grids.append(grid_temp)
        speeds.append(speed_temp)
        forces.append(force_temp)
    bar.next()  # Обновление прогресс-бара

# Сохраняем оставшиеся данные
#save_intermediate_results([csr_matrix(matrix) for matrix in grids], frames + 1)

bar.finish()
