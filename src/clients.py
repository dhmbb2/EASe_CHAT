import socket
import threading
import pickle
import utils
import os

HOST = "127.0.0.1"
PORT = 11452
self_username = None

def init():
    global self_username

    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        csock.connect((HOST, PORT))
        print("connected to", (HOST, PORT))
    except ConnectionRefusedError as err:
        print(f"Connection refused: {err}")
        exit(1)

    auth_success = False
    while not auth_success:
        mode = input("Choose sign_up or sign_in:")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if mode == "sign_in":
            auth_success = sign_in(csock, username, password)
        else:
            auth_success = sign_up(csock, username, password)

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
        print("User not found")
        return False
    else:
        data = pickle.loads(data)
        print(data.message)
        return True
    
def sign_up(csock, username, password):
    csock.send(pickle.dumps(utils.Auth(username, password, False)))
    data = csock.recv(1024)
    if data == b'Failed':
        print("User already exists")
        return False
    else:
        data = pickle.loads(data)
        print(data.message)
        return True
    
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

if __name__ == "__main__":
    init()