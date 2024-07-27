import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import pickle
import matplotlib.colors as mcolors
# Функция для создания и сохранения анимации
def save_animation(array, cmap, output_file, vmax):
    fig, ax = plt.subplots()  # Используем только один subplot
    ims = []

    # Чтение из файла исходного стенда
    with open('./cash/data_stan.pkl', 'rb') as file:
        sparse_matrix_stan = pickle.load(file)
    stan = sparse_matrix_stan.toarray()  # Если 0, то частица может двигаться, если 1, то частицу невозможно сдвинуть (бесконечная масса)  

    # Создаем цветовую карту от прозрачного до белого, для того чтобы нарисовать белую стену
    colors = [(1, 1, 1, 0), (1, 1, 1, 1)]  # RGBA формат (красный, зеленый, синий, альфа-канал)
    cmap_name = 'transparent_to_white'
    cmap_wall = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

    # Создаем изображение для стены
    ax.imshow(stan, cmap=cmap_wall, interpolation='none', alpha=1.0)
    ax.set_xlim(0, stan.shape[1])
    ax.set_ylim(stan.shape[0], 0)  # Инвертируем ось Y для правильного отображения изображения

    # Определение координат точек для стен
    wall_points = np.argwhere(stan == 1)  # Получение координат точек, где значение 1

    # Создаем объект scatter для стен
    wall_scatter = ax.scatter(wall_points[:, 1], wall_points[:, 0], c='white', s=1, zorder=5)

    for frame in array:
        im = ax.imshow(frame, animated=True, cmap=cmap)
        im.set_clim(vmin=0, vmax=vmax)
        ims.append([im, wall_scatter])  # Добавляем scatter в список изображений

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
    ani.save(output_file, writer='ffmpeg', dpi=350)


# Функция для генерации примера двумерного массива
def generate_example_array(shape=(30, 30)):
    return np.random.rand(100, *shape)

# Основная функция для обработки аргументов командной строки
def main():
    parser = argparse.ArgumentParser(description='Generate and save animated visualization of a 2D array')
    #parser.add_argument('output_file', type=str, help='Output file name (e.g., animation.mp4)')
    parser.add_argument('data', type=str, default='1', help='Output file name result_100.pkl)')
    parser.add_argument('--cmap', type=str, default='viridis', help='Colormap name (default: viridis)')
    parser.add_argument('--vmax', type=float, default='1', help='vmax (default: 1)')
    args = parser.parse_args()
    
    # Чтение из файла исходного состояния
    with open(args.data, 'rb') as file:
        sparse_matrix = pickle.load(file)

    # Преобразование обратно в плотный формат
    grids = [matrix.toarray() for matrix in sparse_matrix]


    output_file = args.data[:-4] + '.mp4'
    # Сохраняем анимацию с заданным cmap
    save_animation(grids, args.cmap, output_file, args.vmax)



if __name__ == '__main__':
    main()
