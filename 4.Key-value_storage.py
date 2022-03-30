# Реализация key-values хранилища.
# Данные сохраняются в файле storage.data.
# Добавление новых данных в хранилище и получение текущих значений осуществляется с помощью утилиты командной строки storage.py

import json
import tempfile
import argparse
import os

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, help='key of the dictionary')
parser.add_argument('--value', type=str, help='value in the dictionary')
args = parser.parse_args()


if os.path.isfile(storage_path):
    with open(storage_path, 'r') as fp: # Чтение файла 'data.json' и преобразование данных JSON в объекты Python
        data = json.load(fp)
        if args.key:
            if args.value:
                if bool(data) is True:
                    if args.key in data.keys():
                        data[args.key].append(args.value)
                        #print("THERE ARE IS VALUE", data[args.key])
                    else:
                        data[args.key] = []
                        data[args.key].append(args.value)
                        #print("NEW VALUE", data[args.key])
                    with open(storage_path, 'w') as write_file:
                        json.dump(data, write_file)
                else:
                    data[args.key]=[]
                    data[args.key].append(args.value)
                    with open(storage_path, 'w') as write_file:
                        json.dump(data, write_file)
            else:
                if bool(data) is True:
                    # тут нужно переписать на чтение файла
                    if args.key in data.keys():
                        with open(storage_path, 'r') as read_file:
                            data1 = json.load(read_file)
                            print(', '.join(data1[args.key]))
                    else:
                        print(None)
                else:
                    print(None)
        else:
            with open(storage_path, 'w') as write_file:
                json.dump(data, write_file)

else:
    saver = {}
    if args.key:
        #saver[args.key]=[]
        if args.value:
            saver[args.key] = []
            saver[args.key].append(args.value)
            with open(storage_path, 'w') as write_file:
                json.dump(saver, write_file)
        else:
            with open(storage_path, 'w') as write_file:
                json.dump(saver, write_file)
    else:
        with open(storage_path, 'w') as write_file:
            json.dump(saver, write_file)
