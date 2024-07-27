import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

# Путь к папке с видеофайлами
folder_path = './cash/'
folder_save = './'

# Получение списка всех MP4 файлов в папке
file_names = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

# Функция для извлечения числа из названия файла
def extract_number(file_name):
    # Разделяем строку и находим первое числовое значение
    number = ''.join(filter(str.isdigit, file_name))
    return int(number) if number else 0

def merge_video_audio(video_clip, audio_path, fadein_duration=5, fadeout_duration=5):
    # Загружаем аудио
    audio_clip = AudioFileClip(audio_path)

    # Применяем эффекты плавного включения и затухания
    audio_clip = audio_clip.audio_fadein(fadein_duration).audio_fadeout(fadeout_duration)
 
    # Обрезаем аудио, если оно длиннее видео
    if audio_clip.duration > video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    
    # Назначаем аудио дорожку к видео
    return video_clip.set_audio(audio_clip)

def crop_center_square(clip):
    # Получаем размеры видео
    width, height = clip.size
    
    # Вычисляем размеры квадрата (сторона квадрата будет равна меньшей стороне видео)
    side_length = ((1237 - 1.9 * 276)/1237) * width
    
    # Вычисляем координаты верхнего левого угла квадрата
    x_center = (276/1237) * width
    y_center = (111/928) * height
    
    # Обрезаем видео до центрального квадрата
    return clip.crop(x_center, y_center, x_center + side_length, y_center + side_length)

# Сортировка файлов по числовому значению в названии
file_names.sort(key=extract_number)

# Создание полного пути к каждому файлу
file_paths = [os.path.join(folder_path, f) for f in file_names]
print("Sorted files:", file_names)

# Загрузка видеофайлов
clips = []
for file in file_paths:
    try:
        clip = VideoFileClip(file)
        clip = clip.resize(height=2000)  # Reduce resolution to 720p
        clips.append(clip)
    except Exception as e:
        print(f"Error loading {file}: {e}")

# Check if any clips are loaded
if not clips:
    print("No video clips were loaded. Exiting.")
    exit()

# Объединение видеофайлов
try:
    final_clip = concatenate_videoclips(clips)
except Exception as e:
    print(f"Error concatenating clips: {e}")
    exit()

audio_file = "audio.mp3"
video_clip = merge_video_audio(final_clip, audio_file)

full_clip = crop_center_square(video_clip)

# Сохранение объединенного видео
output_path = os.path.join(folder_save, 'result.mp4')
try:
    full_clip.write_videofile(output_path, codec='libx264', fps=24, bitrate="5000k", audio_codec='aac', preset='medium', threads=4)
except Exception as e:
    print(f"Error writing final video: {e}")
finally:
    # Clean up and close all clips
    for clip in clips:
        clip.close()
