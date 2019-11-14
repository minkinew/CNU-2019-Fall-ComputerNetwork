import socket
from phue import Bridge

class hue:
    def __init__(self):
        self.bridge = Bridge('192.168.0.100')
        self.bridge.connect()
        self.lights = self.bridge.lights

    def power_control(self, bulb_num, power): # 전원제어
        try:
            if power == "on":
                self.lights[int(bulb_num)-1].on = True
            else:
                self.lights[int(bulb_num)-1].on = False
        except Exception as e:
            print("error a occur with" , e)


    def brightness_control(self, bulb_num, brightness): # 밝기제어
        try:
            self.lights[int(bulb_num)-1].brightness = int(brightness)
        except Exception as e:
            print("error occur with" , e)


    def color_control(self,bulb_num, colors_x, colors_y): # 색깔제어
        try:
            self.lights[int(bulb_num)-1].xy = [float(colors_x), float(colors_y)]
        except Exception as e:
            print("error occur with ", e)

def open_server_socket(IP):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM
    s_socket.bind((IP.ipaddress, IP.port))
    s_socket.listen()
    return s_socket


def accept_client(s_socket):
    h = hue()
    while True:
        html=''
        conn, addr = s_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        s = data.split('\r\n')[0].split(' ')[0]
        print("IP:{0}, data:{1} ".format(addr[0], data))
       
        if "favicon.ico" in data:
            continue
        
        print(s)

        if s == "POST":
            s = data.split('\r\n')[14]
            print(" : " + s)
            s = s.split('&')
            s0 = s[0].split('=')
            s1 = s[1].split('=')
            s2 = s[2].split('=')
            s3 = s[3].split('=')
            print(" : " + s0[1] + ":" + s1[1] + ":" + s2[1] + ":" + s3[1] + ":")
            i = str(s0[0])
            i = i[-1]
            h.power_control(i, s0[1])
            h.brightness_control(i, s1[1])
            h.color_control(i, s2[1], s3[1])
    
        if True:
            f = open('index.html','r')
            html = str(f.read())
            print("HTML : ",html)
        
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
