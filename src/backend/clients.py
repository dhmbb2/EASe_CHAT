import socket
import threading
import pickle
import backend.utils as utils
import os
from queue import Queue


def init(in_queue: Queue, out_queue: Queue, HOST, PORT):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        csock.connect((HOST, PORT))
        print("connected to", (HOST, PORT))
    except ConnectionRefusedError as err:
        print(f"Connection refused: {err}")
        exit(1)

    auth_success = False
    while not auth_success:
        is_in, username, password = in_queue.get()
        if is_in:
            ret = sign_in(csock, username, password)
        else:
            ret = sign_up(csock, username, password)
        out_queue.put(ret)
        auth_success = ret[0]

    self_username = username
    print("Auth success")
    
    client_thread = threading.Thread(target=recv_handler, args=(csock,))
    client_thread.start()

    while True:
        try:
            data = input("Enter data: ")
            process_data(csock, data)
        except KeyboardInterrupt:
            csock.send(pickle.dumps(utils.closeConnection()))
            csock.close()
            exit(0)

def process_data(csock, data: str):
    if data == "close":
        csock.send(utils.closeConnection())
        return
    if data == "send":
        username = input("Enter username: ")
        message = input("Enter message: ")
        csock.send(pickle.dumps(utils.Message(username, message)))
        return
    if data == "file":
        username = input("Enter username: ")
        file_path = input("Enter file name: ")
        # send_file_thread = threading.Thread(target=send_file, args=(csock, username, file_path))
        # send_file_thread.start()
        send_file(csock, username, file_path)
    
def recv_handler(csock):
    while True:
        data = csock.recv(1024)
        data = pickle.loads(data)
        if isinstance(data, utils.Message):
            print(data.message)
        elif isinstance(data, utils.File):
            # handle_image()
            print("A file is sent to you from ", data.ufrom)
    
def sign_in(csock, username, password):
    csock.send(pickle.dumps(utils.Auth(username, password, True)))
    data = csock.recv(1024)
    if data == b'Failed':
        return (False, f"User {username} not found")
    else:
        data = pickle.loads(data)
        return (True, f"{data.username}, welcome!")
    
def sign_up(csock, username, password):
    csock.send(pickle.dumps(utils.Auth(username, password, False)))
    data = csock.recv(1024)
    if data == b'Failed':
        return (False, f"User {username} already exists")
    else:
        data = pickle.loads(data)
        return (True, f"Sign up successfully, {data.username}!")
    
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
