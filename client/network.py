"""
networking of the clients
"""
import socket
import pickle
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
        a = []
        for i in dic.split(";"):
            a.append(tuple(i.split(",")))
        a.pop(-1)
        print(a)
        return uid, a
    
    def pre_game(self):
        print("pre_game")
        print("\n"*3)
        dic = self.s.recv(2048)
        print(dic)
        dic = dic.decode()
        print("pre_game")
        if dic == "sleep" or dic == "first":
            return dic

        a = []
        for i in dic.split(";"):
            print(i)
            a.append(tuple(i.split(",")))
        a.pop(-1)
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
    
    def recv_cards(self):
        
        return pickle.loads(self.s.recv(2048))

    def disconnect(self):
        '''
        disconnect from the server
        '''
        self.s.close()
    
if __name__ == '__main__':
    import main