import os
import socket

import config
from handler import Handler

class Server:
    def __init__(self, root, ncpu):
        self.root = root
        self.ncpu = ncpu
        self.workers = []


    def start(self):
        print('Server start')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((config.HOST, config.PORT))                            
        server_socket.listen(config.LISTENERS)                                    


        for worker in range(self.ncpu):
            pid = os.fork()
            if pid:
                self.workers.append(pid)
            else:
                print('Run worker: {}'.format(os.getpid()))
                while True:
                    client_socket, client_address = server_socket.accept()        
                    request = client_socket.recv(config.REQ_SIZE)                 

                    
                    if request.strip() == 0:
                        client_socket.close()
                        continue

                    handler = Handler(self.root, request)
                    response = handler.get_response()
                    client_socket.sendall(response)

                    client_socket.close()

        server_socket.close()


        for pid in self.workers:
            os.waitpid(pid, 0)
