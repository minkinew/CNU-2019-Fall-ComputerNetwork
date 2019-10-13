import socket

def open_server_socket(IP):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM
    s_socket.bind((IP.ipaddress, IP.port))
    s_socket.listen()
    return s_socket


def accept_client(s_socket):
    while True:
        conn, addr = s_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        print("IP:{0}, data:{1} ".format(addr[0], data))
        if "favicon.ico" in data:
            continue
        html = file_read(data)
        conn.sendall(("HTTP/1.1 200 OK\n" + "\n" + html + "\n").encode('utf-8'))
        conn.close()


def main(FLAGS):
    server_socket = open_server_socket(FLAGS)
    accept_client(server_socket)


def file_read(data):
    a = data.find('GET')
    b = data.find('HTTP')
    a = a + 3
    path = data[a:b]
    path = path[2:-1]
    print("path : " + path)
    f = open(path, 'r')
    html = f.read()
    f.close()
    return html


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--ipaddress', type=str, default='172.17.0.2')
    parser.add_argument('-p', '--port', type=int, default=80)
    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)

