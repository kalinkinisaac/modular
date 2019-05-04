import atexit
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from api import Api


connections = {}
lock = Lock()


def get_connection(user_id):
    with lock:
        if user_id not in connections:
            connections[user_id] = Api()

        return connections[user_id]


@atexit.register
def close_connections():
    for connection in connections.values():
        connection.close()


manager = BaseManager(('', 37844), b'password')
manager.register('get_connection', get_connection)
server = manager.get_server()
server.serve_forever()
