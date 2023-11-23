import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
  
# Объявляем переменные  
progres = 0 #Начальный прогресс рендера анимации  
N = 400 #Размер сетки, наример 400 на 400  
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
  
#Создаем волну 1
for i in range(-2, 3):
    for j in range(-2, 3):
        grid[np.roll(N // 2, i), np.roll(a, j)] = amplitude 
#Создаем волну 2
for i in range(-2, 3):
    for j in range(-2, 3):
        grid[np.roll(N // 2, i), np.roll(с, j)] = amplitude
  
#Основная функция, котрая вызывается на каждом шагу  
def update(data):   
    global grid, speed, k, temp, progres, frame_all, amplitude  
    new_grid = np.copy(grid)  
    print('frame ' + str(progres) + '/' + str(frame_all))  
    temp += 1  
  
    progres += 1 #Считаем прогресс на каждом шаге  
  
    #Раз в 30 шагов вызываем волну
    if temp == 30:  
        for i in range(-2, 3):
            for j in range(-2, 3):
                grid[np.roll(N // 2, i), np.roll(a, j)] = amplitude 

        for i in range(-2, 3):
            for j in range(-2, 3):
                grid[np.roll(N // 2, i), np.roll(с, j)] = amplitude
        temp = 0  

    force = k * (np.roll(grid, 1, axis=0) + np.roll(grid, 1, axis=1) +
             np.roll(grid, -1, axis=0) + np.roll(grid, -1, axis=1) - 4 * grid)
    speed = speed + force
    grid = grid + speed * (1 - stan) 
    mat.set_data(grid)  
    mat.set_clim(vmin=0, vmax=75)
    return [mat]  
  
fig, ax = plt.subplots()  
ax.set_axis_off() #убираем оси
    
ax.set_xlim(N//2 - x_max, N//2 + x_max)
ax.set_ylim(N//2- y_max, N//2 + y_max)

#Цветовая раскраска карты  
cmap = 'inferno'  
mat = ax.matshow(grid, cmap=cmap)  
fps = 15  
second = 30
dpi = 200 
frame_all = fps * second  
  
#Основной цикл анимации  
ani = animation.FuncAnimation(fig, update, frames=range(frame_all), save_count=50, repeat=True)  
ani.save('result_color_map.gif', fps=fps, dpi=dpi)
print('Done!')