import os
import json
import argparse
from progress.bar import Bar


def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

def load_data(step):
    s = 0
    filenames = []
    while True:
        s += step
        filename = f'./cash/results_{s}.pkl'
        if os.path.exists(filename):
            filenames.append(filename)
        else:
            break
    return filenames

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--cmap', type=str, default='viridis', help='Colormap name (default: viridis)')
    parser.add_argument('--vmax', type=float, default='1', help='vmax (default: 1)')
    args = parser.parse_args()

    
    # Загрузка конфигурации
    config = load_config('config.json')
    step = config.get('step')

    # Загрузка данных
    filenames = load_data(step)
    bar = Bar('Сохранение...', max=len(filenames))  # Создаем прогресс бар
    for filename in filenames:
        bar.next()  # Обновление прогресс-бара
        os.system(f'python ./modules/animate_saver_ones.py {filename} --cmap={args.cmap} --vmax={args.vmax}')
    
    bar.finish()
    os.system('python ./modules/collect_video.py')
if __name__ == '__main__':
    main()
