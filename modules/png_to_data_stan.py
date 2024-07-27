import numpy as np
from PIL import Image
import pickle
from scipy.sparse import csr_matrix

# Загружаем изображение
image_path = 'data.png'
image = Image.open(image_path)

# Преобразуем изображение в массив numpy
image_array = np.array(image)

# Создаем маску для серых пикселей, исключая белый
gray_mask = (
    (image_array[:, :, 0] == image_array[:, :, 1]) & 
    (image_array[:, :, 1] == image_array[:, :, 2]) & 
    (image_array[:, :, 0] != 255)
)

# Создаем новый двумерный массив, где серые пиксели заменяются на 1, остальные на 0
binary_array = np.zeros((image_array.shape[0], image_array.shape[1]), dtype=int)
binary_array[gray_mask] = 1

# Преобразование в разреженный формат CSR (чтобы нулевые значения не заносились в файл. Экономит место)
sparse_matrix = csr_matrix(binary_array)

# Сохраним результат в отдельный файл
with open('./cash/data_stan.pkl', 'wb') as file:
    pickle.dump(sparse_matrix, file)
