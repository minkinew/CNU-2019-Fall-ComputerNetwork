from threading import Thread
import socket
import os

def send_recv(client_socket, address):
    data = ("HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" +"Computer Network" + "\n").encode('utf-8')
    print("[client {}] {}".format(os.getpid(), data.decode()))
    client_socket.send(data)
    client_socket.close()


def main(FLAGS):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('',FLAGS.port))
    serversocket.listen(5)
    clients = list()

    while True:
        client, address= serversocket.accept()
        print("accept client from", address)
        data = client.recv(1024).decode('utf-8')
        i = data.find('GET')
        j = data.find('\n')
        print(data[i:j])

        th = Thread(target=send_recv, args=(client, address))
        th.start()
        th.join()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddress', type=str, default='172.17.0.2')
    parser.add_argument('-p', '--port', type=int, default=80)
    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)

