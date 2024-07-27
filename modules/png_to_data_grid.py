import numpy as np
from PIL import Image
import pickle
from scipy.sparse import csr_matrix

def image_to_red_array(image_path):
    # Открываем изображение
    img = Image.open(image_path)
    
    # Преобразуем изображение в RGB (на случай, если оно в другом формате)
    img = img.convert('RGB')
    
    # Получаем данные пикселей как numpy массив
    pixel_data = np.array(img)
    
    # Извлекаем компонент красного цвета (R) для каждого пикселя
    red_component = pixel_data[:, :, 0]
    
    # Создаем маску для белых пикселей (255, 255, 255)
    white_pixel_mask = (pixel_data[:, :, 0] == 255) & \
                       (pixel_data[:, :, 1] == 255) & \
                       (pixel_data[:, :, 2] == 255)
    
    # Создаем маску для черных пикселей (0, 0, 0)
    black_pixel_mask = (pixel_data[:, :, 0] == 0) & \
                       (pixel_data[:, :, 1] == 0) & \
                       (pixel_data[:, :, 2] == 0)
    
    # Создаем маску для серых пикселей (R == G == B, исключая черные и белые)
    gray_pixel_mask = (pixel_data[:, :, 0] == pixel_data[:, :, 1]) & \
                      (pixel_data[:, :, 1] == pixel_data[:, :, 2]) & \
                      ~white_pixel_mask & \
                      ~black_pixel_mask
    
    # Объединяем маски белых, черных и серых пикселей
    ignored_pixels_mask = white_pixel_mask | black_pixel_mask | gray_pixel_mask
    
    # Устанавливаем значения красной компоненты для игнорируемых пикселей в 0
    red_component[ignored_pixels_mask] = 0
    
    return red_component/255

# Путь к изображению
image_path = 'data.png'

# Получение массива красной составляющей, игнорируя белые пиксели
red_array = image_to_red_array(image_path)

# Преобразование в разреженный формат CSR (чтобы нулевые значения не заносились в файл. Экономит место)
sparse_matrix = csr_matrix(red_array)

# Сохраняем результат в отдельный файл
with open('./cash/data_grid.pkl', 'wb') as file:
    pickle.dump(sparse_matrix, file)
print('Инициализация завершена!')