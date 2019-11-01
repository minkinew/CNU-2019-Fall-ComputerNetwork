import select
import socket
import os

def send_recv(client, address):
    msg = ("HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" +"Computer Network" + "\n").encode('utf-8')
    print("[client {}] {}".format(os.getpid(), msg.decode()))
    client.send(msg)
    client.close()


def main(FLAGS):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('',FLAGS.port))
    serversocket.listen(5)
    clients = list()
    selectlist = [serversocket]

    while True:
        readfds, writefds, exceptfds = select.select(selectlist, [], [])
        for a in readfds:
            if a == serversocket:
                client, address = serversocket.accept()
                selectlist.append(client)
            else:
                data = a.recv(1024).decode('utf-8')
                if data:
                    msg = ("HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" +"Computer Network" + "\n").encode('utf-8')
                    a.send(msg)
                    a.close()
                    selectlist.remove(a)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddress', type=str, default='172.17.0.2')
    parser.add_argument('-p', '--port', type=int, default=80)
    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)

