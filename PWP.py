import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
  
# Объявляем переменные  
progres = 0 #Начальный прогресс рендера анимации  
N = 400 #Размер сетки, наример 400 на 400  
k = 0.5 #Коэффициент пружин  
temp = 0 #Переменная, которая является cщетчиком при выборе частоты создание волн  
a = N // 2 + 20 # Для определения положения источника волны  
с = N // 2 - 20 # Для определения положения источнка волны 
  
amplitude = N # Амплитудное значение волны  
  
#Объявляем массивы  
speed = np.zeros((N, N)) #Скорость каждой частицы с координатами x,y  
grid = np.zeros((N, N))  #Значение компоненты z каждой частицы с координатами x,y  
stan = np.zeros((N, N)) #Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть(бесконечная масса)  
  
  
#Создаем источник волны 1  
grid[N // 2, a] = amplitude  
grid[N // 2 - 1, a] = amplitude  
grid[N // 2 + 1, a] = amplitude  
grid[N // 2, a + 1] = amplitude  
grid[N // 2, a - 1] = amplitude  
grid[N // 2 + 2, a] = amplitude  
grid[N // 2 + 2, a - 1] = amplitude  
grid[N // 2 + 2, a + 1] = amplitude  
grid[N // 2 - 2, a] = amplitude  
grid[N // 2 - 2, a + 1] = amplitude  
grid[N // 2 - 2, a - 1] = amplitude  
grid[N // 2, a + 2] = amplitude  
grid[N // 2 - 1, a + 2] = amplitude  
grid[N // 2 + 1, a + 2] = amplitude  
grid[N // 2, a - 2] = amplitude  
grid[N // 2 - 1, a - 2] = amplitude  
grid[N // 2 + 1, a - 2] = amplitude  
  
#Создаем источник волны 2  
grid[N // 2, с] = amplitude  
grid[N // 2 - 1, с] = amplitude  
grid[N // 2 + 1, с] = amplitude  
grid[N // 2, с + 1] = amplitude  
grid[N // 2, с - 1] = amplitude  
grid[N // 2 + 2, с] = amplitude  
grid[N // 2 + 2, с - 1] = amplitude  
grid[N // 2 + 2, с + 1] = amplitude  
grid[N // 2 - 2, с] = amplitude  
grid[N // 2 - 2, с + 1] = amplitude  
grid[N // 2 - 2, с - 1] = amplitude  
grid[N // 2, с + 2] = amplitude  
grid[N // 2 - 1, с + 2] = amplitude  
grid[N // 2 + 1, с + 2] = amplitude  
grid[N // 2, с - 2] = amplitude  
grid[N // 2 - 1, с - 2] = amplitude  
grid[N // 2 + 1, с - 2] = amplitude  
  
#Основная функция, котрая вызывается на каждом шагу  
def update(data):  
    global grid, speed, k, temp, progres, frame_all, amplitude  
    new_grid = np.copy(grid)  
    print('frame ' + str(progres) + '/' + str(frame_all))  
    temp += 1  
  
    progres += 1 #Считаем прогресс на каждом шаге  
  
    #Раз в 30 шагов вызываем волну    if temp == 30:  
    grid[N // 2, a] = amplitude  
    grid[N // 2 - 1, a] = amplitude  
    grid[N // 2 + 1, a] = amplitude  
    grid[N // 2, a + 1] = amplitude  
    grid[N // 2, a - 1] = amplitude  
    grid[N // 2 + 2, a] = amplitude  
    grid[N // 2 + 2, a - 1] = amplitude  
    grid[N // 2 + 2, a + 1] = amplitude  
    grid[N // 2 - 2, a] = amplitude  
    grid[N // 2 - 2, a + 1] = amplitude  
    grid[N // 2 - 2, a - 1] = amplitude  
    grid[N // 2, a + 2] = amplitude  
    grid[N // 2 - 1, a + 2] = amplitude  
    grid[N // 2 + 1, a + 2] = amplitude  
    grid[N // 2, a - 2] = amplitude  
    grid[N // 2 - 1, a - 2] = amplitude  
    grid[N // 2 + 1, a - 2] = amplitude  

    grid[N // 2, с] = amplitude  
    grid[N // 2 - 1, с] = amplitude  
    grid[N // 2 + 1, с] = amplitude  
    grid[N // 2, с + 1] = amplitude  
    grid[N // 2, с - 1] = amplitude  
    grid[N // 2 + 2, с] = amplitude  
    grid[N // 2 + 2, с - 1] = amplitude  
    grid[N // 2 + 2, с + 1] = amplitude  
    grid[N // 2 - 2, с] = amplitude  
    grid[N // 2 - 2, с + 1] = amplitude  
    grid[N // 2 - 2, с - 1] = amplitude  
    grid[N // 2, с + 2] = amplitude  
    grid[N // 2 - 1, с + 2] = amplitude  
    grid[N // 2 + 1, с + 2] = amplitude  
    grid[N // 2, с - 2] = amplitude  
    grid[N // 2 - 1, с - 2] = amplitude  
    grid[N // 2 + 1, с - 2] = amplitude  
    temp = 0  
  
    #Пробегаем по каждой частице, считаем в них физику  
    for i in range(N - 1):  
        for j in range(N - 1):  
            #Считаем силу, по формулам, которые выразили ранее  
            Force = k * (grid[i + 1, j] + grid[i, j + 1] + grid[i - 1, j] + grid[i, j - 1] - 4 * grid[i, j])  
            #Считаем скорость, по формулам, которые выразили ранее  
            speed[i, j] = speed[i, j] + Force  
            #Считаем скорость, по формулам, которые выразили ранее  
            new_grid[i, j] = grid[i, j] + speed[i, j] * (1 - stan[i, j])  
    grid = new_grid  
    mat.set_data(grid)  
    return [mat]  
  
fig, ax = plt.subplots()  
#Цветовая раскраска карты  
cmap = 'inferno'  
mat = ax.matshow(grid, cmap=cmap)  
fps = 1 
second = 2  
dpi = 500  
frame_all = fps * second  
  
#Основной цикл анимации  
ani = animation.FuncAnimation(fig, update, frames=range(frame_all), save_count=50, repeat=True, interval=2)  
ani.save('2 источника.mp4', fps=fps, dpi=dpi)  
print('Done!')