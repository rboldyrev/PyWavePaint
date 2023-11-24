import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
from mpl_toolkits.mplot3d import Axes3D
  
# Объявляем переменные  
progres = 0 #Начальный прогресс рендера анимации  
N = 100 #Размер сетки, наример 400 на 400  
k = 0.4 #Коэффициент пружин  
temp = 0 #Переменная, которая является cщетчиком при выборе частоты создание волн  
a = N // 2 + 20 # Для определния положения источника волны 1
с = N // 2 - 20 # Для определния положения источника волны 2

x_max = N//2  # Определяем границы оси x, при x = N // 2 -- полный экран
y_max = N//2  # Определяем границы оси y, при y = N // 2 -- полный экран
z_max = N//2   # Пределы оси Z

amplitude = 50 # Амплитудное значение волны  
  
#Объявляем массивы  
speed = np.zeros((N, N)) #Скорость каждой частицы с координатами x,y  
grid = np.zeros((N, N))  #Значение компоненты z каждой частицы с координатами x,y  
stan = np.zeros((N, N)) #Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть(бесконечная масса)  
force = np.zeros((N, N))
  
#Создаем волну 1
for i in range(-4, 5):
    for j in range(-2, 3):
        grid[np.roll(N // 2, i), np.roll(a, j)] = amplitude 
#Создаем волну 2
for i in range(-4, 5):
    for j in range(-2, 3):
        grid[np.roll(N // 2, i), np.roll(с, j)] = amplitude
  
#Основная функция, котрая вызывается на каждом шагу  
def update(data):
    global grid, speed, k, temp, progres, frame_all, amplitude, mat
    ax.cla()
    ax.set_axis_off() #убираем оси
    
    ax.set_xlim(N//2 - x_max, N//2 + x_max)
    ax.set_ylim(N//2- y_max, N//2 + y_max)
    ax.set_zlim(0, z_max)


    mat.remove()
    print('frame ' + str(progres) + '/' + str(frame_all))  
  
    progres += 1 #Считаем прогресс на каждом шаге  

    force = k * (np.roll(grid, 1, axis=0) + np.roll(grid, 1, axis=1) +
             np.roll(grid, -1, axis=0) + np.roll(grid, -1, axis=1) - 4 * grid)
    speed = speed + force
    grid = grid + speed * (1 - stan) 
    mat = ax.plot_surface(x, y, grid, cmap='inferno')
    mat.set_clim(vmin=-3, vmax=3)
    return  mat  
  
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off() #убираем оси
#Цветовая раскраска карты   
x, y = np.meshgrid(np.arange(N), np.arange(N))
mat = ax.plot_surface(x, y, grid, cmap='inferno') 
fps = 15  
second = 20
dpi = 250 
frame_all = fps * second  
  
#Основной цикл анимации  
ani = animation.FuncAnimation(fig, update, frames=range(frame_all), save_count=50, repeat=True)  
ani.save('PWP_3d.gif', fps=fps, dpi=dpi)
print('Done!')