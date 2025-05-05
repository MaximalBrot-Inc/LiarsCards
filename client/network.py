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
        try:
            self.s.sendall(data.encode())
        except AttributeError:
            pickle_data = pickle.dumps(data)
            self.s.sendall(pickle_data)
            print("sending pickle data")

    def receive_first(self):
        '''
        receive data from the server
        '''
        uid = self.s.recv(2048).decode()
        self.uid = uid
        print(uid)
        dic = self.s.recv(2048).decode()
        a = []
        for i in dic.split(";"):
            a.append(tuple(i.split(",")))
        a.pop(-1)
        print(a)
        return uid, a
    
    def pre_game(self):
        dic = self.s.recv(2048)
        dic = dic.decode()
        try:
            dic = int(dic)
            print("uid:", dic)
            return dic
        except:
            a = []
            for i in dic.split(";"):
                print(i)
                a.append(tuple(i.split(",")))
            a.pop(-1)
            print("list:", a)
            return a
    
    def recv(self):
        '''
        receive data from the server
        '''
        data = self.s.recv(2048)
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            data = pickle.loads(data)

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