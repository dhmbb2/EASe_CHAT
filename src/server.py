import socket
import threading
import pickle
import backend.utils as utils
import os



class Server:
    def __init__(self):
        # username : [password, is_online, conn]
        self.clients_meta = {}

        self.HOST = "127.0.0.1"
        self.PORT = 11451
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen(5)
        print("listening on", (self.HOST, self.PORT))

        try:
            while True:
                conn, addr = self.lsock.accept()
                client_thread = threading.Thread(target=self.connection_handler, args=(conn, addr))
                client_thread.start()
        except KeyboardInterrupt:
            for client in self.clients_meta:
                client.send(pickle.dumps(utils.closeConnection()))
                client["conn"].close()
            self.lsock.close()
            exit(0)

    def connection_handler(self, conn, addr):

        username = None

        while True:
            data = conn.recv(1024)
            # handle abrupt connection close
            if not data:
                if username is None:
                    conn.close()
                    exit(0)
                print(f"Connection form {username} is closed")
                self.clients_meta[username]["is_online"] = False
                self.clients_meta[username]["conn"].close()
                self.clients_meta[username]["conn"] = None
                exit(0)
            data = pickle.loads(data)
            if isinstance(data, utils.closeConnection):
                print("recv this")
                if username is None:
                    conn.close()
                    exit(0)
                print(f"Connection form {username} is closed")
                self.clients_meta[username]["is_online"] = False
                self.clients_meta[username]["conn"] = None
                username = None
                if data.is_abrupt:
                    socket_send(conn, utils.closeConnection(True))
                    conn.close()
                    exit(0)
                socket_send(conn, utils.closeConnection(False))
            # handle authorization request
            elif isinstance(data, utils.Auth):
                print("AUTH ")
                if data.sign_in:
                    if not data.username in self.clients_meta.keys():
                        socket_send(conn, utils.SysWarning("No such user!"))
                        continue
                    if data.password != self.clients_meta[data.username]["password"]:
                        socket_send(conn, utils.SysWarning("Wrong password!"))
                        continue
                    if self.clients_meta[data.username]["is_online"]:
                        socket_send(conn, utils.SysWarning("User already online!"))
                        continue
                    socket_send(conn, utils.SysWarning("Success"))
                    self.clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
                else:
                    if data.username in self.clients_meta.keys():
                        socket_send(conn, utils.SysWarning("User already exists!"))
                        continue
                    socket_send(conn, utils.SysWarning("Success"))
                    self.clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
                username = data.username
                print(self.clients_meta.keys())
            # handle message request
            elif isinstance(data, utils.Message):
                if data.uto in self.clients_meta.keys():
                    print(f"get message: {data.message}")
                    socket_send(self.clients_meta[data.uto]["conn"], data)
            elif isinstance(data, utils.File):
                self.deal_with_file(conn, data)
            elif isinstance(data, utils.Request):
                if data.request == "get_user_list":
                    user_list = []
                    for key in self.clients_meta.keys():
                        if self.clients_meta[key]["is_online"]:
                            user_list.append(key)
                    socket_send(conn, utils.Request("get_user_list", user_list))
            else:
                conn.send(pickle.dumps(utils.SysWarning("Invalid request!")))
            
    def deal_with_file(self, conn, data):
        assert isinstance(data, utils.File), "data is of the wrong type"

        if data.ask_for_download:
            file_path = os.path.join(os.getcwd(), "FileCache", data.ufrom, data.uto, data.file_name)
            if not os.path.exists(file_path):
                socket_send(conn, utils.SysWarning("File not found!"))
                return
            # open a new port for file transfer
            new_port = utils.get_free_port()
            # wait for client to connect
            file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_socket.bind((self.HOST, new_port))
            file_socket.listen(1)
            # inform the client for the new port 
            socket_send(conn, utils.Request("file_port", new_port))
            file_download_thread = threading.Thread(target=self.file_download_handler, args=(file_socket, file_path, data.length))
            file_download_thread.start()
            return

        if data.uto in self.clients_meta.keys():
            # inform that there is file incoming
            # socket_send(self.clients_meta[data.uto][1], data.file_name)
            # receive file
            file_data = b''
            save_root = os.path.join(os.getcwd(), "FileCache", data.ufrom, data.uto)
            if not os.path.exists(save_root):
                os.makedirs(save_root)
            save_path = os.path.join(save_root, data.file_name)
            while len(file_data) < data.length:
                file_data += conn.recv(1024)
            print(f"File received: {data.file_name} with total bytes: {len(file_data)}")
            # cache the file
            with open(save_path, "wb") as file:
                file.write(file_data)
            socket_send(self.clients_meta[data.uto]["conn"], utils.File(data.uto, data.ufrom, data.time, data.file_name, data.length, False))
            print("Notification Sent")

    def file_download_handler(self, file_socket, file_path, file_size):
        conn, addr = file_socket.accept()
        with open(file_path, "rb") as file:
            bytes_sent = 0
            while bytes_sent < file_size:
                file_data = file.read(1024)
                if not file_data:
                    break
                conn.sendall(file_data)
                bytes_sent += len(file_data)
        print("File sent")
        conn.close()
        file_socket.close()
                                   
def socket_send(conn, data):
    try:
        conn.send(pickle.dumps(data))
    except Exception as e:
        print(e)

            
if __name__ == "__main__":
    server = Server()
