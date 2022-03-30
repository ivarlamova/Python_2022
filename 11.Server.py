# Сервер принимает от клиентов команды put и get, разбирает их, формирует ответ

import socket
import asyncio
from collections import defaultdict
from copy import deepcopy

class StorageDriverError(ValueError):
    pass

class Storage:
    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._data[key][timestamp] = value

    def get(self, key):
        if key == "*":
            return deepcopy(self._data)
        if key in self._data:
            return {key: deepcopy(self._data.get(key))}
        return {}

class StorageManager:

    def __init__(self, storage):
        self.storage=storage

    def __call__(self, data):
        method, *args = data.split()

        if method == 'put':
            key, value, timestamp = args
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}

        elif method == "get":
            key = args.pop()
            if args:
                raise StorageDriverError
            return self.storage.get(key)
        else:
            raise StorageDriverError

    pass

class ClientServerProtocol(asyncio.Protocol):
    storage = Storage()
    sep = '\n'
    code_ok = 'ok'
    code_err = 'error'
    error_message = 'wrong command'

    def __init__(self):
        super().__init__()
        self.manager = StorageManager(self.storage)
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):

        self._buffer += data

        try:
            request = self._buffer.decode()
            if not request.endswith(self.sep):
                return

            self._buffer, message = b'', ''
            raw_data = self.manager(request.rstrip(self.sep))

            for key, values in raw_data.items():
                message += self.sep.join(f'{key} {value} {timestamp}' \
                                         for timestamp, value in sorted(values.items()))
                message += self.sep

            code = self.code_ok
        except (ValueError, UnicodeDecodeError, IndexError):
            message = self.error_message + self.sep
            code = self.code_err

        response = f'{code}{self.sep}{message}{self.sep}'
        self.transport.write(response.encode())

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    run_server('127.0.0.1', 8181)


'''
sock = socket.socket()
sock.bind(('127.0.0.1', 8888))
sock.listen(1)
conn, addr = sock.accept()

print('Соединение установлено:', addr)

# переменная response хранит строку возвращаемую сервером, если вам для
# тестирования клиента необходим другой ответ, измените ее
response = b'ok\npalm.cpu 10.5 1501864277\neardrum.cpu 15.3 1501864259\npalm.cpu 1.5 1501864297\npalm.cpu 2.5 1501864247\neardrum.cpu 15.3 1501864271\neardrum.cpu 15.3 1501864292\n\n'
#response = b'error\n\n'
while True:
    data = conn.recv(1024)
    if not data:
        break
    request = data.decode('utf-8')
    print(f'Получен запрос: {ascii(request)}')
    print(f'Отправлен ответ {ascii(response.decode("utf-8"))}')
    conn.send(response)

conn.close()
'''