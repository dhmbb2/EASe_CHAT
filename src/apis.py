from clients import init
from queue import Queue
from threading import Thread

class ClientManager:
    def __init__(self):
        self.out_queue = Queue()
        self.in_queue = Queue()
        client_thread = Thread(target=init, args=(self.out_queue, self.in_queue))

    def sign_api(self, is_in, user_name, password) -> tuple[bool, str]:
        self.in_queue.put((is_in, user_name, password))
        return self.out_queue.get()