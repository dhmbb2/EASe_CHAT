import socket
import threading
import pickle
import backend.utils as utils
import os
from queue import Queue
import json

MessageCache_root = "MessageCache"

class MessageBuffer:
    def __init__(self, max_len):
        self.max_len = max_len
        # a buffer with key: username, value: a deque of messages with max_len
        self.buffer = {}
        self.lock = threading.Lock()
    
    def add_message(self, ufrom, user, time, message):
        self.lock.acquire()
        if ufrom not in self.buffer:
            self.buffer[ufrom] = []
        self.buffer[ufrom].append((user, time, message))
        self.lock.release()
    
    def get_messages(self, username):
        self.lock.acquire()
        if username not in self.buffer:
            self.lock.release()
            return []
        ret = self.buffer[username]
        self.lock.release()
        return ret

class Client:
    def __init__(self, in_queue: Queue, out_queue: Queue, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        # channel to communicate with frontend thread
        self.in_queue = in_queue
        self.out_queue = out_queue

    def __call__(self):
        # channel to communicate with receiving thread
        self.recv_queue = Queue()
        self.message_buffer = MessageBuffer(20)
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.csock.connect((self.HOST, self.PORT))
            print("connected to", (self.HOST, self.PORT))
        except ConnectionRefusedError as err:
            print(f"Connection refused: {err}")
            exit(1)

        auth_success = False
        while not auth_success:
            is_in, username, password = self.in_queue.get()
            if is_in:
                ret = self.sign_in(username, password)
            else:
                ret = self.sign_up(username, password)
            self.out_queue.put(ret)
            auth_success = ret[0]

        self_username = username
        print("Auth success")
        
        # start client threading
        client_thread = threading.Thread(target=recv_handler, args=(self.csock, self.message_buffer, self.recv_queue))
        client_thread.start()

        while True:
            option = self.in_queue.get()
            assert isinstance(option, str), "mode is of the wrong type"

            if option == "message_list":
                username = self.in_queue.get()
                self.out_queue.put(self.get_messages(self_username, username))
            elif option == "user_list":
                self.out_queue.put(self.get_user_list())
    

    def sign_in(self, username, password):
        # send the message
        self.csock.send(pickle.dumps(utils.Auth(username, password, True)))
        data = self.csock.recv(1024)
        if data == b"Success":
            return (True, "Sign in successfully!")
        else:
            return (False, str(data))
        
        
    def sign_up(self, username, password):
        self.csock.send(pickle.dumps(utils.Auth(username, password, False)))
        data = self.csock.recv(1024)
        if data == b"Success":
            return (True, "Sign up successfully!")
        else:
            return (False, str(data))
        
    def get_messages(self, username):
        return self.message_buffer.get_messages(username)
    
    def get_user_list(self):
        self.csock.send(pickle.dumps(utils.Request("get_user_list")))


    # while True:
    #     try:
    #         data = input("Enter data: ")
    #         process_data(csock, data)
    #     except KeyboardInterrupt:
    #         csock.send(pickle.dumps(utils.closeConnection()))
    #         csock.close()
    #         exit(0)

    # def process_data(self, data: str):
    #     if data == "close":
    #         self.csock.send(utils.closeConnection())
    #         return
    #     if data == "send":
    #         username = input("Enter username: ")
    #         message = input("Enter message: ")
    #         csock.send(pickle.dumps(utils.Message(username, message)))
    #         return
    #     if data == "file":
    #         username = input("Enter username: ")
    #         file_path = input("Enter file name: ")
    #         # send_file_thread = threading.Thread(target=send_file, args=(csock, username, file_path))
    #         # send_file_thread.start()
    #         send_file(csock, username, file_path)
    
def recv_handler(csock, buffer, recv_queue):
    while True:
        data = csock.recv(1024)
        data = pickle.loads(data)
        if isinstance(data, utils.Message):
            buffer.add_message(data.ufrom, data.ufrom, data.time, data.message)
        elif isinstance(data, utils.Request):
            if data.request == "get_user_list":
                recv_queue.put(data.object)
        elif isinstance(data, utils.File):
            # handle_image()
            print("A file is sent to you from ", data.ufrom)

    


    
def handle_image(csock, header):
    length = header.length
    name = header.file_name
    data = b''
    while len(data) < length:
        data += csock.recv(1024)

    with open(name, 'wb') as file:
        file.write(data)
    print("File received")
               
def send_file(csock, username, file_path):
    global self_username

    file_size = os.path.getsize(file_path)
    _, file_name = os.path.split(file_path)
    csock.send(pickle.dumps(utils.File(username, self_username, file_name, file_size)))
    
    with open(file_path, 'rb') as f:    
        bytes_sent = 0
        while bytes_sent < file_size:
            file_data = f.read(1024)
            if not file_data:
                break  # 文件读取完毕
            csock.sendall(file_data)
            bytes_sent += len(file_data)
    print("File sent")
