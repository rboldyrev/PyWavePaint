import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
import matplotlib.colors as mcolors
  
# Объявляем переменные  
progres = 0 #Начальный прогресс рендера анимации  
N = 1000 #Размер сетки, наример 400 на 400  
k = 0.5 #Коэффициент пружин  
temp = 0 #Переменная, которая является cщетчиком при выборе частоты создание волн  
a = N // 2 + 20 # Для определния положения источника волны 1
с = N // 2 - 20 # Для определния положения источника волны 2
  
x_max = N // 4 # Определяем границы оси x, при x = N // 2 -- полный экран
y_max = N // 4 # Определяем границы оси y, при y = N // 2 -- полный экран

amplitude = N * 1 # Амплитудное значение волны  
  
#Объявляем массивы  
speed = np.zeros((N, N)) #Скорость каждой частицы с координатами x,y  
grid = np.zeros((N, N))  #Значение компоненты z каждой частицы с координатами x,y  
stan = np.zeros((N, N)) #Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть(бесконечная масса)  
force = np.zeros((N, N))

# Создаем плоскую волну
grid[:,N//4] = amplitude 

# Вертикальная стена с одним отверстием
wall_1 = N//2 - N // 8
stan[:,wall_1] = 1 
stan[N//2 - 5:N//2 + 5,wall_1] = 0
 

# Вертикальная стена с двумя отверстиями
wall_2 = N//2
stan[:,wall_2] = 1 
stan[N//2 + 10:N//2 + 20,wall_2] = 0
stan[N//2 - 20:N//2 - 10,wall_2] = 0


#Основная функция, котрая вызывается на каждом шагу  
def update(data):   
    global grid, speed, k, temp, progres, frame_all, amplitude  
    new_grid = np.copy(grid)  
    print('frame ' + str(progres) + '/' + str(frame_all))  
    progres += 1 #Считаем прогресс на каждом шаге  
  
    force = k * (np.roll(grid, 1, axis=0) + np.roll(grid, 1, axis=1) +
             np.roll(grid, -1, axis=0) + np.roll(grid, -1, axis=1) - 4 * grid)
    speed = speed + force
    grid = grid + speed * (1 - stan) 
    mat.set_data(grid)  
    mat.set_clim(vmin=0, vmax=20)
    return [mat]  
  
fig, ax = plt.subplots()  
ax.set_axis_off() #убираем оси
    
ax.set_xlim(N//2 - x_max, N//2 + x_max)
ax.set_ylim(N//2- y_max, N//2 + y_max)

#Цветовая раскраска карты  
cmap = 'inferno'  
mat = ax.matshow(grid, cmap=cmap) 

# Рисуем mat
mat = ax.matshow(grid, cmap=cmap)

# Создаем цветовую карту от прозрачного до белого, для того чтобы нарисовать белую стену
colors = [(1, 1, 1, 0), (1, 1, 1, 1)]  # RGBA формат (красный, зеленый, синий, альфа-канал)
cmap_name = 'transparent_to_white'
cmap_wall = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
paint_wall = ax.matshow(stan, cmap=cmap_wall)

fps = 20  
second = 30
dpi = 101
frame_all = fps * second  
  
#Основной цикл анимации  
ani = animation.FuncAnimation(fig, update, frames=range(frame_all), save_count=50, repeat=True)  
ani.save('PWP_Jung_exp.gif', fps=fps, dpi=dpi)
print('Done!')