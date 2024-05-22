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
    def __init__(self, uto, ufrom ,file_name, length):
        self.uto = uto
        self.ufrom = ufrom
        self.file_name = file_name
        self.length = length

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
    "Request can either be get_user_list "
    def __init__(self, request, object=None):
        self.request = request
        self.object = object