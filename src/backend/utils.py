import socket, random

class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Message:
    def __init__(self, uto, ufrom, time, message):
        self.uto = uto
        self.ufrom = ufrom
        self.time = time
        self.message = message

class File:
    def __init__(self, uto, ufrom, time, file_name, length, ask_for_download=False):
        self.uto = uto
        self.ufrom = ufrom
        self.time = time
        self.file_name = file_name
        self.length = length
        self.ask_for_download = ask_for_download

class Auth(Credentials):
    def __init__(self, username, password, sign_in):
        super().__init__(username, password)
        self.sign_in = sign_in

class SysWarning:
    def __init__(self, message):
        self.message = message

class closeConnection:
    def __init__(self, is_abrupt) -> None:
        self.is_abrupt = is_abrupt

class Request:
    "Request can either be get_user_list, file_port "
    def __init__(self, request, object=None):
        self.request = request
        self.object = object

def generate_random_port():
    return random.randrange(1024, 60000)

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result

def get_free_port():
    port = generate_random_port()
    while check_port(port) == 0:
        port = generate_random_port()
    return port
