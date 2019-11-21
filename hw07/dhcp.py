import socket
import struct
from phue import Bridge
import subprocess

class hue:
    def __init__(self) :
        self.bridge = Bridge('192.168.0.118')
        self.bridge.connect()
        self.light = self.bridge.lights

    def power_control(self, bulb_num, power):
        try :
            if power == "on" :
                self.light[int(bulb_num)-1].on = True
            else :
                self.light[int(bulb_num)-1].on = False
        except Exception as e :
            print("error a occur with ", e)

    def brightness_control(self, bulb_num, brightness):
        try :
            self.light[int(bulb_num)-1].brightness = int(brightness)
        except Exception as e :
            print("error a occur with ", e)

    def color_control(self, bulb_num, colors_x, colors_y) :
        try :
            self.light[int(bulb_num)-1].xy = [float(colors_x),float(colors_y)]
        except Exception as e :
            print("error a occur with ", e)


def main() :
    raw_socket = socket.socket(socket.AF_PACKET,
                               socket.SOCK_RAW,
                               socket.ntohs(0x0003))
    while True :
        recv_packet = raw_socket.recvfrom(5000)
        ethernet_protocol = struct.unpack('!6s6sH', (recv_packet[0])[:14])[2]

        if ethernet_protocol == 0x800 :
            ip_protocol = struct.unpack('!BBHHHBBH4s4s', recv_packet[0][14:34])[6]

            if ip_protocol == 17 :
                udp_src_port = struct.unpack('!H', (recv_packet[0])[34:34+2])[0]

                if udp_src_port == 68 :
                    if (str(recv_packet[0][0:14])).find(r'xf8\xe6\x1a\xc8\x8eq') :
                        h = hue()
                        h.power_control(0, "on")
                        h.power_control(1, "on")
                        h.power_control(2, "on")
                        
                        print("DHCP Data : ", recv_packet[0][42:])
                        ip = recv_packet[0][296:300]
                        ip = struct.unpack('!1B1B1B1B',ip)
                        return str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3])

if __name__ == '__main__' :
    ip_addr = main()
    while True :
        status, result = subprocess.getstatusoutput("ping -c1 -w2 " + ip_addr)
        if status == 0 :
            print("respond OK")
        else :
            print("NOT respond")
            h = hue()
            h.power_control(0, "off")
            h.power_control(1, "off")
            h.power_control(2, "off")
