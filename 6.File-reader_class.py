# Конструктор класса FileReader принимает один параметр: путь до файла на диске.
# В классе FileReader должен быть реализован метод read, возвращающий строку - содержимое файла,
# путь к которому был указан при создании экземпляра класса.

import json

class FileReader:

    def __init__(self, url):
        self.url = str(url)

    def __str__(self):
        return self.url

    def read(self):
        try:
            with open(self.url, 'r') as file:
                data = file.read()
                return data
                file.close()
        except (FileNotFoundError, UnboundLocalError):
            data = ''
            return data
        else:
            data = ''
            return data


