import socket
FLAGS = None
class ClientSocket():
    
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def socket_send_recv(self, FLAGS):
        data = "GET /polls/ HTTP/1.1\r\nHost: localhost:2345\r\n\r\n"
        self.socket.connect((FLAGS.ip, FLAGS.port))
        self.socket.sendall(data.encode('utf-8'))
        data = self.socket.recv(1024*16)
        print(data)
        

    def main(self, FLAGS):
        self.socket_send_recv(FLAGS)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=2345)
    FLAGS, _ = parser.parse_known_args()

    client_socket = ClientSocket()
    
    client_socket.main(FLAGS)
