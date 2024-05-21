class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Message:
    def __init__(self, target, message):
        self.target = target
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
    def __init__(self) -> None:
        pass