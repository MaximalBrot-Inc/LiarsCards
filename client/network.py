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
        pass

    def connect(self, domain, port):
        '''
        connect to the server
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((domain, port))
        self.s.sendall(b'Hello world, hatsune miku')
        

    def send(self, data):
        '''
        send data to the server
        '''
        pass

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
    
    def receive(self):
        '''
        receive data from the server
        '''
        

    def disconnect(self):
        '''
        disconnect from the server
        '''
        pass
    
if __name__ == '__main__':
    import main