# Протокол поддерживает два вида запросов к серверу со стороны клиента:
# отправка данных для сохранения их на сервере
# получения сохраненных данных

import socket
import bisect
import time

class ClientError(Exception):
    pass

class Client:

    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except self.error as err:
            raise ClientError ('Smth wrong with client connection', err)

    def put(self, key, value, timestamp = None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            self.connection.sendall(f"put {key} {value} {timestamp}\n".encode('utf-8'))
        except socket.error as err:
            raise ClientError ("Client can't send a request for put command", err)
        try:
            data = self.connection.recv(1024)
        except socket.error as err:
            raise ClientError ("Client can't take an information from server", err)
        status, data1 = data.decode("utf-8").split('\n', 1)
        if status != 'ok':
            raise ClientError('Server returns error')



    def get(self, key):
        try:
            self.connection.sendall(f"get {key}\n".encode())
        except socket.error as err:
            raise ClientError ("Client can't send a key for get command", err)
        try:
            data = self.connection.recv(1024)
        except socket.error as err:
            raise ClientError ("Client can't take an information from server", err)

        data_dict = dict()
        data_dict_key = dict()
        status, data1 = data.decode("utf-8").split('\n', 1)
        if status != 'ok':
            raise ClientError('Server returns error')
        if data1 == '\n':
            return data_dict
        data2, tail = data1.split('\n\n', 1)
        try:
            for line in data2.splitlines():
                all_key, value, timestamp = line.split()
                if all_key not in data_dict:
                    data_dict[all_key]=[]
                tuple1=(int(timestamp), float(value))
                data_dict[all_key].append(tuple1)
                data_dict[all_key].sort()
                #bisect.insort(data_dict[key], ((int(timestamp), float(value))))
            if key != '*':
                #data_dict_key[key] = []
                data_dict_key[key]= data_dict[key]
                return data_dict_key
            if key == '*':
                return data_dict

        except Exception as err:
            raise ClientError ("Invalid data from server", err)



    def close (self):
        try:
            self.connection.close()
        except self.error as err:
            raise ClientError ('Smth wrong with closing in Client', err)



    #sock.sendall(b'ping')
