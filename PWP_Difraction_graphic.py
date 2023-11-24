import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

  
# Объявляем переменные  
progres = 0 #Начальный прогресс рендера анимации  
N = 1000 #Размер сетки, наример 400 на 400  
k = 0.5 #Коэффициент пружин  
temp = 0 #Переменная, которая является cщетчиком при выборе частоты создание волн  
a = N // 2 + 20 # Для определния положения источника волны 1
с = N // 2 - 20 # Для определния положения источника волны 2
  
x_max = round(N * 0.4) # Определяем границы оси x, при x = N // 2 -- полный экран
y_max = round(N * 0.3) # Определяем границы оси y, при y = N // 2 -- полный экран

amplitude = N * 1 # Амплитудное значение волны  
  

#Объявляем массивы  
speed = np.zeros((N, N)) #Скорость каждой частицы с координатами x,y  
grid = np.zeros((N, N))  #Значение компоненты z каждой частицы с координатами x,y  
stan = np.zeros((N, N)) #Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть(бесконечная масса)  
force = np.zeros((N, N))


# Создаем плоскую волну
grid[:,N//4] = amplitude 

# Вертикальная стена
wall_1 = round(N * 0.3)
stan[:,wall_1] = 1 

# Вертикальная стена
wall_2 = 0
stan[:,wall_2] = 1 

#Цикл создает щели порядка d
w = 5 #ширина щели
d = 3*15 #порядок дифракционной решетки
for i in range(N//d):
    stan[i * d - w//2:i * d + w//2,wall_1] = 0


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
    temp = temp + 1

    line2.set_ydata(np.abs(grid[:,im_wall]))

    return (mat, line2) 
  
fig, ax = plt.subplots(2, figsize=(6, 10))  
#ax.set_axis_off() #убираем оси




y = np.arange(0, N, 1)
im_wall = N//2
line2 = ax[1].plot(y, np.abs(grid[:,im_wall]), color = 'red')[0]
ax[1].set_xlabel(f'y, где x = {im_wall}, зеленый экран')
ax[1].set_ylabel('amplitude')
ax[1].set_ylim(0, 0.05 * amplitude)


title = plt.title('Визуализация дифракционной решетки \n при помощи программы PyWavePaint', fontsize=14, pad = 335) 
#Цветовая раскраска карты  
cmap = 'inferno'  
# Рисуем mat
mat = ax[0].matshow(grid, cmap=cmap)

# Создаем цветовую карту от прозрачного до белого, для того чтобы нарисовать белую стену
colors = [(1, 1, 1, 0), (1, 1, 1, 1)]  # RGBA формат (красный, зеленый, синий, альфа-канал)
cmap_name = 'transparent_to_white'
cmap_wall = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
paint_wall = ax[0].matshow(stan, cmap=cmap_wall)

# Создаем цветовую карту от прозрачного до зеленого, для того чтобы нарисовать экран
im_wall_massive = np.zeros((N, N)) #Массив, чтобы показать где находится экран
im_wall_massive[:,im_wall] = 1 

im_colors = [(0, 1, 0, 0), (0, 1, 0, 1)]  # RGBA формат (красный, зеленый, синий, альфа-канал)
im_cmap_name = 'transparent_to_green'
im_cmap_wall = mcolors.LinearSegmentedColormap.from_list(im_cmap_name, im_colors, N=256)
im_paint_wall = ax[0].matshow(im_wall_massive, cmap=im_cmap_wall)

fps = 30     
second = 20
dpi = 180
frame_all = fps * second  
  
#Основной цикл анимации  
ani = animation.FuncAnimation(fig, update, frames=range(frame_all), repeat=True)  
ani.save('PWP_Difraction_graphic.gif', fps=fps, dpi=dpi)
print('Done!')
