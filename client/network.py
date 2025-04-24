"""
networking of the clients
"""
import socket
class Network(socket.socket):
    '''
    networking of the clients
    '''
    def __init__(self):
        '''
        constructor
        '''

    def connect(self, domain, port):
        '''
        connect to the server
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((domain, port))
        self.s.sendall(b'Gurrr,skin2')
        

    def send(self, data):
        '''
        send data to the server
        '''
        self.s.sendall(data.encode())

    def receive_first(self):
        '''
        receive data from the server
        '''
        uid = self.s.recv(2048).decode()
        print(uid)
        dic = self.s.recv(2048).decode()
        safsafd = dic.split(";")
        lst = []
        for i in safsafd:
            lst.append(i)
        print(lst)
        return uid, lst
    
    def pre_game(self):
        dic = self.s.recv(2048).decode()
        if len(dic) == 1 or dic == "first":
            return dic
        
        a = []
        for i in dic.split(";"):
            a.append(tuple(map(int, i.split(","))))
        print(a)
        return a
    
    def recv(self):
        '''
        receive data from the server
        '''
        data = self.s.recv(2048).decode()
        if not data:
            return None
        return data

    def disconnect(self):
        '''
        disconnect from the server
        '''
        self.s.close()
    
if __name__ == '__main__':
    import main