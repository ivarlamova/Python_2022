# Интерфейс для работы с файлами, возможности:
# чтение из файла, метод read возвращает строку с текущим содержанием файла
# запись в файл, метод write принимает в качестве аргумента строку с новым содержанием файла
# сложение объектов типа File, результатом сложения является объект класса File,
# при этом создается новый файл и файловый объект, в котором содержимое второго файла добавляется к содержимому первого файла.
# Новый файл должен создаваться в директории, полученной с помощью функции tempfile.gettempdir.
# Для получения нового пути можно использовать os.path.join.

import json
import tempfile
import os

class File:

    def __init__(self, filename):
        '''тут происходит инициализация класса (присваиваю путь)
        и проверка наличия папки в файловой системе (если нет - создаем)'''
        self.address = filename
        self.current_position = 0
        if not os.path.exists(self.address):
            self.f = open(self.address, 'w+')

    def __str__(self):
        '''на печать выводим адрес (имя) файла'''
        return self.address

    def __enter__(self):
        '''тк работа с файлом - тут его открываю'''
        return self.f

    def read (self):
        '''тут чтение файла'''
        with open(self.address, 'r') as file:
            return file.read()


    def write(self, new_text):
        '''запись в файл заданной строки'''
        with open(self.address, 'w') as file:
            return file.write(new_text)


    def __add__(self, obj):
        '''слияние двух файлов в третий (+ его создание)'''
        new_name = next(tempfile._get_candidate_names()) # тут задается рандомное имя временного файла через _get_candidate_names()
        a = type(self)(os.path.join(tempfile.gettempdir(), new_name)) # тут присваиваем тип объекта через type(self)
                                                                    # (у меня изначально было File(next_name), но программа работала некорректно (была ошибка с os.path.excists)
        try:
            a.write(self.read()+obj.read())
        except PermissionError:
            print(a.address)
        return a

    def __iter__(self):
        ''' запуск интератора, эта часть просто возвращает self ВСЕГДА'''
        return self

    def __next__(self):
        '''тут описание итерируемых данных (строк в нашем случае)'''
        with open(self.address, 'r') as f:
            f.seek(self.current_position) # просматриваем элемент на 0 позиции (по дефолту)

            line = f.readline() # считываем строку от 0 элемента
            if not line:
                self.current_position = 0
                raise StopIteration

            self.current_position = f.tell() # меняем рначальную позицию и начинаем цикл чтения

            return line

    def __exit__(self, *args):
        '''тк работа с файлом - а тут его закрываю'''
        self.f.close()



