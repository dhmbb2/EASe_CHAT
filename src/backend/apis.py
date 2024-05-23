from backend.clients import Client
from queue import Queue
from threading import Thread

class ClientManager:
    def __init__(self, HOST="127.0.0.1", PORT=11451):
        self.out_queue = Queue()
        self.in_queue = Queue()
        client_thread = Thread(target=Client(self.out_queue, self.in_queue, HOST, PORT))
        client_thread.start()

    def sign_api(self, is_in, user_name, password) -> tuple[bool, str]:
        self.out_queue.put(("sign", is_in, user_name, password))
        return self.in_queue.get()
    
    def get_user_list_api(self) -> list:
        self.out_queue.put(("user_list",))
        return self.in_queue.get()

    def get_message_api(self, username) -> list:
        self.out_queue.put(("message_list", username))
        return self.in_queue.get()
    
    def send_message_api(self, package) -> None:
        self.out_queue.put(("send_message", package))

    def xx_api(self) -> None:
        self.out_queue.put(("xx",))

    def sign_out_api(self) -> None:
        self.out_queue.put(("sign_out",))

    def download_file_api(self, target, file_path) -> None:
        self.out_queue.put(("download_file", target, file_path))