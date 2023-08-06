![Language](https://img.shields.io/badge/English-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)


Small utils for python

***

## Installation

### Package Installation from PyPi

```bash
$ pip install utilspy-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/utilspy).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install -r requirements.txt
$ pip install .
```

***

## Utils

- ### add_ext
Add extension to path.

Support Windows and Linux paths.

```python
from utilspy_g4 import add_ext

path = '/test/test.png'
ext = '2'
new_path = add_ext(path, ext)     # new_path = '/test/test.2.png'
```

- ### compare_frames
Compare 2 frames.

```python
from utilspy_g4 import compare_frames

is_equal = compare_frames('path_to_frame_1.png', 'path_to_frame_2.png')
```

- ### del_ext
Del extension from path.

Support Windows and Linux paths.

```python
from utilspy_g4 import del_ext

path = '/test/test.png'
new_path = del_ext(path)     # new_path = '/test/test'

path = '/test/test.2.png'
new_path = del_ext(path)     # new_path = '/test/test.2'

path = '/test/test.2.png'
new_path = del_ext(path, 2)     # new_path = '/test/test'
```

- ### templated_remove_files
Remove files by template

```python
from utilspy_g4 import templated_remove_files

templated_remove_files('/tmp/test_*.txt')
```

- ### get_ext
Get extension from path.

Support Windows and Linux paths.

```python
from utilspy_g4 import get_ext

path = '/test/test.png'
ext = get_ext(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = get_ext(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = get_ext(path, 2)     # ext = 'jpeg'

path = '/test/test.jpeg.png'
ext = get_ext(path, 0)     # ext = ''
```

- ### concat_video
Concat 2 video files with same codecs and params.
It use ffmpeg. Install [ffmpeg](https://ffmpeg.org) and add it to PATH.

```python
from utilspy_g4 import concat_video

concat_video('path_to_video_1.ts', 'path_to_video_2.ts', 'path_to_output_video.ts')
```

- ### int_to_2str
Convert integer to 2 chars string with 0.

```python
from utilspy_g4 import int_to_2str

time = f'{int_to_2str(2)}:{int_to_2str(23)}:{int_to_2str(5)}' # time = '02-23-05'
```

- ### get_files_count
Get files count from template.

Support Windows and Linux paths.

```python
from utilspy_g4 import get_files_count

get_files_count('/tmp/test_*.txt')
```

[Changelog](https://github.com/Genzo4/utilspy/blob/main/CHANGELOG.md)

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)

Небольшие утилитки для Python.

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install utilspy-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/utilspy).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install -r requirements.txt
$ pip install .
```

***

## Утилиты

- ### add_ext
Добавляет дополнительное расширение файла перед его последним расширением.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import add_ext

path = '/test/test.png'
ext = '2'
newPath = add_ext(path, ext)     # newPath = '/test/test.2.png'
```

- ### compare_frames
Сравнение двух кадров (изображений).

```python
from utilspy_g4 import compare_frames

is_equal = compare_frames('path_to_frame_1.png', 'path_to_frame_2.png')
```

- ### del_ext
Удаляет одно или несколько расширений файла

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import del_ext

path = '/test/test.png'
new_path = del_ext(path)     # newPath = '/test/test'

path = '/test/test.2.png'
new_path = del_ext(path)     # newPath = '/test/test.2'

path = '/test/test.2.png'
new_path = del_ext(path, 2)     # newPath = '/test/test'
```

- ### templated_remove_files
Удаление файлов по шаблону

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import templated_remove_files

templated_remove_files('/tmp/test_*.txt')
```

- ### get_ext
Возвращает расширение файла.
Можно указать какое по счёту расширение надо вернуть.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import get_ext

path = '/test/test.png'
ext = get_ext(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = get_ext(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = get_ext(path, 2)     # ext = 'jpeg'

path = '/test/test.jpeg.png'
ext = get_ext(path, 0)     # ext = ''
```

- ### concat_video
Объединение двух видео файлов с одинаковыми кодеками и параметрами в один файл.
Используется ffmpeg. Для использования установите [ffmpeg](https://ffmpeg.org) 
и пропишите его в PATH.

```python
from utilspy_g4 import concat_video

concat_video('path_to_video_1.ts', 'path_to_video_2.ts', 'path_to_output_video.ts')
```

- ### int_to_2str
Преобразует число в строку из двух символов.
Если число состоит из одной цифры, то спереди добавляется '0'.

```python
from utilspy_g4 import int_to_2str

time = f'{int_to_2str(2)}:{int_to_2str(23)}:{int_to_2str(5)}' # time = '02-23-05'
```

- ### get_files_count
Возвращает количество файлов в папке по шаблону.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import get_files_count

get_files_count('/tmp/test_*.txt')
```

***

[Changelog](https://github.com/Genzo4/utilspy/blob/main/CHANGELOG.md)
