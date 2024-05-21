import socket
import threading
import pickle
import backend.utils as utils
import os

HOST = "127.0.0.1"
PORT = 11451

clients = []
clients_meta = {}
guid = 0

def init():
    global clients
    global guid

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen(5)
    print("listening on", (HOST, PORT))

    try:
        while True:
                conn, addr = lsock.accept()
                clients.append(conn)

                client_thread = threading.Thread(target=connection_handler, args=(conn, addr))
                client_thread.start()
                guid += 1
    except KeyboardInterrupt:
        for client in clients:
            client.send(pickle.dumps(utils.closeConnection()))
            client.close()
        lsock.close()
        exit(0)

def connection_handler(conn, addr):
    global clients
    global clients_meta
    # global guid

    username = None

    while True:
        data = conn.recv(1024)
        data = pickle.loads(data)
        if isinstance(data, utils.closeConnection):
            clients.remove(conn)
            clients_meta.pop(username)
            conn.close()
            exit(0)
        elif isinstance(data, utils.Auth):
            if data.sign_in:
                if data.username in clients_meta.keys():
                    conn.send(pickle.dumps(utils.SysWarning(f"Current user: {clients_meta.keys()}")))
                else:
                    conn.send(b"Failed")
            else:
                if data.username in clients_meta.keys():
                    conn.send(b"Failed")
                    continue
                # lock here
                # id = guid
                clients_meta[data.username] = (data.password, conn)
                # guid += 1
                username = data.username
                # unlock here
                conn.send(pickle.dumps(utils.SysWarning(f"Current user: {clients_meta.keys()}")))
            print(clients_meta)
        elif isinstance(data, utils.Message):
            if data.target in clients_meta.keys():
                clients_meta[data.target][1].send(pickle.dumps(utils.Message(data.target, data.message)))
                conn.send(pickle.dumps(utils.SysWarning("Message sent!")))
            else:
                conn.send(pickle.dumps(utils.SysWarning("User not found!")))
        elif isinstance(data, utils.File):
            if data.uto in clients_meta.keys():
                # inform that there is file incoming
                socket_send(clients_meta[data.uto][1], data.file_name)
                # receive file
                file_data = b''
                save_root = os.path.join(os.getcwd(), "FileCache", data.ufrom)
                if not os.path.exists(save_root):
                    os.makedirs(save_root)
                save_path = os.path.join(save_root, data.file_name)
                print(data.length)
                while len(file_data) < data.length:
                    file_data += conn.recv(1024)
                    print(len(file_data))
                # cache the file
                with open(save_path, "wb") as file:
                    file.write(file_data)

        else:
            conn.send(pickle.dumps(utils.SysWarning("Invalid request!")))
                                   
def socket_send(conn, data):
    try:
        conn.send(pickle.dumps(data))
    except Exception as e:
        print(e)
            
if __name__ == "__main__":
    init()
