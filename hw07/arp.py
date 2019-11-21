import socket
import struct
from phue import Bridge
import subprocess

class hue:
    def __init__(self) :
        self.bridge = Bridge('192.168.0.118')
        self.bridge.connect()
        self.light = self.bridge.lights

    def power_control(self,bulb_num, power) :
        try :
            if power == "on" :
                self.light[int(bulb_num)-1].on = True
            else :
                self.light[int(bulb_num)-1].on = False
        except Exception as e :
            print("error a occur with ", e)

    def brightness_control(self,bulb_num,brightness) :
        try :
            self.light[int(bulb_num)-1].brightness = int(brightness)
        except Exception as e :
            print("error a occur with ", e)

    def color_control(self,bulb_num,colors_x,colors_y) :
        try :
            self.light[int(bulb_num)-1].xy = [float(colors_x),float(colors_y)]
        except Exception as e :
            print("error a occur with ", e)

def main() :
    for i in range(500) :
        raw_socket = socket.socket(socket.PF_PACKET,
                                   socket.SOCK_RAW,
                                   socket.htons(0x0800))
        raw_socket.bind(("wlp1s0", socket.htons(0x800))) 
        
        protocol = 0x0806 # Protocol (ARP : 0x0806)
        dest_mac = bytes.fromhex('ffffffffff') # Destination(Broadcast)
        source_mac = bytes.fromhex('0c96e67b1a7b') # Source
        eth_header = struct.pack("!6s6sH", dest_mac, source_mac, protocol)
        
        hardware_type = 1 # Hardware type (1) 
        protocol_type = 0x0800 # Protocol type
        hardware_size = 6 # Hardware size
        protocol_size = 4 # Protocol size
        opcode = 1 # request

        sender_mac = bytes.fromhex('ace01000075b') # Sender MAC address
        target_mac = bytes.fromhex('000000000000') # Target MAC address
        sender_ip = socket.inet_aton("192.168.0.120") # Sender IP address
        ip_start = "192.168.0."
        ip_end = str(i)
        ip_addr = ip_start + ip_end
        target_ip = socket.inet_aton(ip_addr) # Target IP
        
        print( str(i+1) + "번째 ip : " + str(ip_addr))
        arp_header = struct.pack("!HHBBH6s4s6s4s",
                                 hardware_type, protocol_type, hardware_size,
                                 protocol_size, opcode, sender_mac, sender_ip,
                                 target_mac, target_ip)
        
        packet = eth_header + arp_header
        raw_socket.send(packet)
        

        try :
            recv_socket = socket.socket(socket.PF_PACKET,
                                        socket.SOCK_RAW,
                                        socket.htons(0x0806))
            
            recv_socket.settimeout(0.1)
            data = recv_socket.recv(1024)
            phone_mac_addr = bytes.fromhex('5077053C4547') # Phone MAC address
            proto = bytes.fromhex('0806')
            if phone_mac_addr == data[6:12] and proto :
                h = hue()
                h.power_control(0, "on")
                h.power_control(1, "on")
                h.power_control(2, "on")

                ip = data[28:32]
                ip = struct.unpack('!1B1B1B1B', ip)
                return (str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3]))
        except socket.timeout :
            pass
        
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
