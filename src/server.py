import socket
import threading
import pickle
import backend.utils as utils
import os

HOST = "127.0.0.1"
PORT = 11451


# username : [password, is_online, conn]
clients_meta = {}
guid = 0

def init():
    global guid

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen(5)
    print("listening on", (HOST, PORT))

    try:
        while True:
                conn, addr = lsock.accept()
                client_thread = threading.Thread(target=connection_handler, args=(conn, addr))
                client_thread.start()
                guid += 1
    except KeyboardInterrupt:
        for client in clients_meta:
            client.send(pickle.dumps(utils.closeConnection()))
            client["conn"].close()
        lsock.close()
        exit(0)

def connection_handler(conn, addr):
    global clients_meta
    # global guid

    username = None

    while True:
        data = conn.recv(1024)
        # handle abrupt connection close
        if not data:
            if username is None:
                conn.close()
                exit(0)
            print(f"Connection form {username} is closed")
            clients_meta[username]["is_online"] = False
            clients_meta[username]["conn"].close()
            clients_meta[username]["conn"] = None
            exit(0)
        data = pickle.loads(data)
        if isinstance(data, utils.closeConnection):
            if username is None:
                conn.close()
                exit(0)
            print(f"Connection form {username} is closed")
            clients_meta[username]["is_online"] = False
            clients_meta[username]["conn"] = None
            if data.is_abrupt:
                conn.close()
                exit(0)
        # handle authorization request
        elif isinstance(data, utils.Auth):
            if data.sign_in:
                if not data.username in clients_meta.keys():
                    socket_send(conn, utils.SysWarning("No such user!"))
                    continue
                if data.password != clients_meta[data.username]["password"]:
                    socket_send(conn, utils.SysWarning("Wrong password!"))
                    continue
                if clients_meta[data.username]["is_online"]:
                    socket_send(conn, utils.SysWarning("User already online!"))
                    continue
                socket_send(conn, utils.SysWarning("Success"))
                clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
            else:
                if data.username in clients_meta.keys():
                    socket_send(conn, utils.SysWarning("User already exists!"))
                    continue
                socket_send(conn, utils.SysWarning("Success"))
                clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
                username = data.username
            print(clients_meta.keys())
        # handle message request
        elif isinstance(data, utils.Message):
            if data.uto in clients_meta.keys():
                print(f"get message: {data.message}")
                socket_send(clients_meta[data.uto]["conn"], data)
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
        elif isinstance(data, utils.Request):
            if data.request == "get_user_list":
                user_list = []
                for key in clients_meta.keys():
                    if clients_meta[key]["is_online"]:
                        user_list.append(key)
                socket_send(conn, utils.Request("get_user_list", user_list))
        else:
            conn.send(pickle.dumps(utils.SysWarning("Invalid request!")))
                                   
def socket_send(conn, data):
    try:
        conn.send(pickle.dumps(data))
    except Exception as e:
        print(e)
            
if __name__ == "__main__":
    init()
