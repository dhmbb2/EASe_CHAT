import socket
import threading
import pickle
import backend.utils as utils
import random
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import os
from collections import deque

class ServerMessageBuffer:
    def __init__(self, max_len):
        self.max_len = max_len
        # a little different from user message buffer
        # a buffer with key: username, value: a dict with username as value and a deque of messages as value
        self.buffer = {}
        self.lock = threading.Lock()
    
    def add_single_message(self, uto, ufrom, message):
        self.lock.acquire()
        if uto not in self.buffer:
            self.buffer[uto] = dict()
        if ufrom not in self.buffer[uto]:
            self.buffer[uto][ufrom] = deque(maxlen=self.max_len)
        self.buffer[uto][ufrom].append(message)
        self.lock.release()

    def add_messages(self, ufrom, buffer):
        self.lock.acquire()
        self.buffer[ufrom] = buffer
        self.lock.release()
    
    def get_messages(self, ufrom):
        self.lock.acquire()
        if ufrom not in self.buffer:
            self.lock.release()
            return dict()
        ret = self.buffer[ufrom].copy()
        self.lock.release()
        return ret

class Server:
    def __init__(self):
        # username : [password, is_online, conn]
        self.clients_meta = {}

        self.sender_server = 'mail.sjtu.edu.cn'
        self.email_sender = "Fill the email here"
        self.sender_password = "Fill your password here"

        self.HOST = "127.0.0.1"
        self.PORT = 11451
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen(5)
        self.message_buffer = ServerMessageBuffer(20)
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
        gt_auth_code = None

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
                self.message_buffer.add_messages(username, data.message_sync)
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
                ret = self.deal_with_auth(conn, data, gt_auth_code)
                print(ret)
                if isinstance(ret, int):
                    gt_auth_code = ret
                elif isinstance(ret, str):
                    username = ret
            # handle message request
            elif isinstance(data, utils.Message):
                if data.uto in self.clients_meta.keys():
                    print(f"get message: {data.message}")
                    if self.clients_meta[data.uto]["conn"] is not None:
                        socket_send(self.clients_meta[data.uto]["conn"], data)
                    else:
                        self.message_buffer.add_single_message(data.uto, data.ufrom, ((data.ufrom, data.time, data.message)))
            elif isinstance(data, utils.File):
                self.deal_with_file(conn, data)
            elif isinstance(data, utils.Request):
                if data.request == "get_user_list":
                    user_list = []
                    for key in self.clients_meta.keys():
                        user_list.append((key, self.clients_meta[key]["is_online"]))
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
            file_size = os.path.getsize(file_path)
            socket_send(conn, utils.Request("file_port", (new_port, file_size)))
            file_download_thread = threading.Thread(target=self.file_download_handler, args=(file_socket, file_path, file_size))
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
            # if the user is online, directly send the notification
            if self.clients_meta[data.uto]["conn"] is not None:
                socket_send(self.clients_meta[data.uto]["conn"], utils.File(data.uto, data.ufrom, data.time, data.file_name, data.length, False))
            else:
                self.message_buffer.add_single_message(data.uto, data.ufrom, ((data.ufrom, data.time, ("file", data.file_name, True))))
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

    def deal_with_auth(self, conn, data, auth_code):
        assert isinstance(data, utils.Auth)
        ## deal with auth code
        if data.is_code_mode:
            assert isinstance(auth_code, int)
            if auth_code == data.code:
                # successfully matched, return the username
                socket_send(conn, utils.SysWarning("Auth Code Matched"))
                self.clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
                socket_send(conn, utils.Request("get_message_list", self.message_buffer.get_messages(data.username)))
                print(self.clients_meta.keys())
                return data.username
            else:
                socket_send(conn, utils.SysWarning("Auth Code MisMatched"))
                return auth_code
        if data.sign_in:
            if not data.username in self.clients_meta.keys():
                socket_send(conn, utils.SysWarning("No such user!"))
                return None
            if data.password != self.clients_meta[data.username]["password"]:
                socket_send(conn, utils.SysWarning("Wrong password!"))
                return None
            if self.clients_meta[data.username]["is_online"]:
                socket_send(conn, utils.SysWarning("User already online!"))
                return None
            socket_send(conn, utils.SysWarning("Success"))
            self.clients_meta[data.username] = {"password": data.password, "is_online": True, "conn": conn}
            socket_send(conn, utils.Request("get_message_list", self.message_buffer.get_messages(data.username))) 
            print(self.clients_meta.keys())
            return data.username
        else:
            if data.username in self.clients_meta.keys():
                socket_send(conn, utils.SysWarning("User already exists!"))
                return None
            code = self.send_auth_code(data.username)
            if code != 0:
                socket_send(conn, utils.SysWarning("Sent successfully"))
                return code
            else: 
                socket_send(conn, utils.SysWarning("Sent failed"))
                return None

    def send_auth_code_test(self, username):
        code = random.randint(10000, 99999)
        return code


    def send_auth_code(self, username) -> int:
        receiver = username + "@sjtu.edu.cn"
        auth_code = random.randint(10000, 99999)
        message = '''
        <p>你的易思聊天注册验证码是：{} 喵～</p>
        <p>验证码很关键，请主人千万不要和别人分享喵~</p>
        '''.format(auth_code)
        msg = MIMEText(message, 'html', _charset="utf-8")
        msg["Subject"] = "Auth code for EASeChat"
        msg["from"] = "ease"
        msg["to"] = "主人大人"

        try:
            with SMTP_SSL(host=self.sender_server) as smtp:
                smtp.login(user = self.email_sender, password = self.sender_password)
                smtp.sendmail(self.email_sender, receiver, msg.as_string())
            print("auth code sent successfully")
            return auth_code
        except smtplib.SMTPException:
            return 0


                                   
def socket_send(conn, data):
    try:
        conn.send(pickle.dumps(data))
    except Exception as e:
        print(e)

            
if __name__ == "__main__":
    server = Server()
