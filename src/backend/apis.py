from backend.clients import Client
from queue import Queue
from threading import Thread

class ClientManager:
    def __init__(self, HOST=None, PORT=None):
        self.out_queue = Queue()
        self.in_queue = Queue()
        client_thread = Thread(target=Client(self.out_queue, self.in_queue, HOST, PORT))
        client_thread.start()

    def sign_api(self, is_in, user_name, password) -> tuple[bool, str]:
        self.out_queue.put((is_in, user_name, password))
        return self.in_queue.get()
    
    def get_user_list_api(self) -> list:
        self.out_queue.put("user_lists")
        return self.in_queue.get()