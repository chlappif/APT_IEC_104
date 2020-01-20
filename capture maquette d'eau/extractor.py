#!/usr/bin/python
# -*- coding: utf-8 -*-


"""Code to extract the data set from previous data packets.
##INPUT : fichiers wireshark en format json.
OUTPUT : Deux fichiers (un pour la Rasperry Gauche (192.168.10.11) ; un pour la Raspeerry Droite (192.168.110.11)) contenant les datasets à créer. 
Chaque élément de donnée est représenté par une ligne avec : la donnée du message reçu par la resperry, la dernière valeur relevée sur le sensor, et la dernière valeur commandée par l'ordinateur. """

import json


def data_extraction(ipsource, ipdest, sourcefile, destfile):
	with open(sourcefile, 'r') as file:
		data = file.read()
	json_data = json.loads(data)

	file2 = open(destfile, "w+")
	demand1 = [0]  # Liste des values passées du monitor (l'ordinateur) à la Rasbperry
	values1 = [18]  # Liste des relevés passés du sensor
	for trame in json_data:
		#Échanges directs
		if trame["_source"]["layers"]["ip"]["ip.src"] == ipsource:
			apci = trame["_source"]["layers"]["104apci"]
			asdu = trame["_source"]["layers"]["104asdu"]

			string = apci["104apci.apdulen"] + "," + apci[
				"104apci.type"]
			string = string + "," + asdu["104asdu.typeid"] + "," + asdu["104asdu.sq"] + "," + asdu[
				"104asdu.numix"] + "," + asdu["104asdu.causetx"] + "," + asdu["104asdu.nega"] + "," + asdu[
						 "104asdu.test"] + "," + asdu["104asdu.oa"] + "," + asdu["104asdu.addr"] + ","
			gaga = False
			if "IOA: 2" in asdu:
				value = asdu["IOA: 2"]["104asdu.normval"]
				if value[0] == "-":
					value = "1"
				else:
					value = "-1"
				demand1.append(value)

		if trame["_source"]["layers"]["ip"]["ip.src"] == ipdest and trame["_source"]["layers"]["104asdu"][
			"104asdu.causetx"] == "5" and gaga == False and string != "0":
			if "IOA: 1" in trame["_source"]["layers"]["104asdu"]:
				yolo = "IOA: 1"
			elif "IOA: 2" in trame["_source"]["layers"]["104asdu"]:
				yolo = "IOA: 2"
			string = string + str(demand1[-1]) + "," + str(values1[-1]) + "," + \
					 trame["_source"]["layers"]["104asdu"][yolo]["104asdu.float"] + "\n"
			values1.append(trame["_source"]["layers"]["104asdu"][yolo]["104asdu.float"])
			file2.write(string)
			string="0"

		#Echanges indirect par la Rpi Centrale
		if trame["_source"]["layers"]["ip"]["ip.src"] == "192.168.20.10":
			gaga=True
			apci = trame["_source"]["layers"]["104apci"]
			asdu = trame["_source"]["layers"]["104asdu"]

			string = apci["104apci.apdulen"] + "," + apci[
				"104apci.type"]
			string = string + "," + asdu["104asdu.typeid"] + "," + asdu["104asdu.sq"] + "," + asdu[
				"104asdu.numix"] + "," + asdu["104asdu.causetx"] + "," + asdu["104asdu.nega"] + "," + asdu[
						 "104asdu.test"] + "," + asdu["104asdu.oa"] + "," + asdu["104asdu.addr"] + ","

		if trame["_source"]["layers"]["ip"]["ip.src"] == "192.168.20.11" and trame["_source"]["layers"]["104asdu"]["104asdu.typeid"] == "11" and gaga == True and string != "0":
			if "IOA: 1" in trame["_source"]["layers"]["104asdu"]:
				string = string + str(demand1[-1]) + "," + str(values1[-1]) + "," + \
						 trame["_source"]["layers"]["104asdu"]["IOA: 1"]["104asdu.scalval"] + "\n"
				values1.append(trame["_source"]["layers"]["104asdu"]["IOA: 1"]["104asdu.scalval"])
				file2.write(string)
				string="0"

	file2.close()
	return None

def data_extraction_lstm(ipsource, ipdest, sourcefile, destfile):
	with open(sourcefile, 'r') as file:
		data = file.read()
	json_data = json.loads(data)

	file2 = open(destfile, "w+")
	demand1 = [0]  # Liste des values passées du monitor (l'ordinateur) à la Rasbperry
	values1 = [18]  # Liste des relevés passés du sensor
	for trame in json_data:
		#Échanges directs
		if trame["_source"]["layers"]["ip"]["ip.src"] == ipsource:
			apci = trame["_source"]["layers"]["104apci"]
			asdu = trame["_source"]["layers"]["104asdu"]

			string = trame["_source"]["layers"]["frame"]["frame.time_epoch"] + "," + apci["104apci.apdulen"] + "," + apci[
				"104apci.type"]
			string = string + "," + asdu["104asdu.typeid"] + "," + asdu["104asdu.sq"] + "," + asdu[
				"104asdu.numix"] + "," + asdu["104asdu.causetx"] + "," + asdu["104asdu.nega"] + "," + asdu[
						 "104asdu.test"] + "," + asdu["104asdu.oa"] + "," + asdu["104asdu.addr"] + ","
			gaga = False
			if "IOA: 2" in asdu:
				value = asdu["IOA: 2"]["104asdu.normval"]
				if value[0] == "-":
					value = "1"
				else:
					value = "-1"
				demand1.append(value)

		if trame["_source"]["layers"]["ip"]["ip.src"] == ipdest and trame["_source"]["layers"]["104asdu"][
			"104asdu.causetx"] == "5" and gaga == False and string != "0":
			if "IOA: 1" in trame["_source"]["layers"]["104asdu"]:
				yolo = "IOA: 1"
			elif "IOA: 2" in trame["_source"]["layers"]["104asdu"]:
				yolo = "IOA: 2"
			string = string + str(demand1[-1]) + "," + str(values1[-1]) + "," + \
					 trame["_source"]["layers"]["104asdu"][yolo]["104asdu.float"] + "\n"
			values1.append(trame["_source"]["layers"]["104asdu"][yolo]["104asdu.float"])
			file2.write(string)
			string="0"

		#Echanges indirect par la Rpi Centrale
		if trame["_source"]["layers"]["ip"]["ip.src"] == "192.168.20.10":
			gaga=True

			apci = trame["_source"]["layers"]["104apci"]
			asdu = trame["_source"]["layers"]["104asdu"]

			string = trame["_source"]["layers"]["frame"]["frame.time_epoch"] + "," + apci["104apci.apdulen"] + "," + apci[
				"104apci.type"]
			string = string + "," + asdu["104asdu.typeid"] + "," + asdu["104asdu.sq"] + "," + asdu[
				"104asdu.numix"] + "," + asdu["104asdu.causetx"] + "," + asdu["104asdu.nega"] + "," + asdu[
						 "104asdu.test"] + "," + asdu["104asdu.oa"] + "," + asdu["104asdu.addr"] + ","

		if trame["_source"]["layers"]["ip"]["ip.src"] == "192.168.20.11" and trame["_source"]["layers"]["104asdu"]["104asdu.typeid"] == "11" and gaga == True and string != "0":
			if "IOA: 1" in trame["_source"]["layers"]["104asdu"]:
				string = string + str(demand1[-1]) + "," + str(values1[-1]) + "," + \
						 trame["_source"]["layers"]["104asdu"]["IOA: 1"]["104asdu.scalval"] + "\n"
				values1.append(trame["_source"]["layers"]["104asdu"]["IOA: 1"]["104asdu.scalval"])
				file2.write(string)
				string="0"

	file2.close()
	return None

""" CAPTURE N°1 
data_extraction("192.168.10.10", "192.168.10.11", "./Capture Data/raspig1.json", "Capture Data/left_raspi_data1.txt")
data_extraction("192.168.110.10", "192.168.110.11", "./Capture Data/raspid1.json", "Capture Data/right_raspi_data1.txt")
 CAPTURE N°2 """
# data_extraction("192.168.10.10", "192.168.10.11", "./Capture\ Data/raspig2.json", "Capture\ Data/left_raspi_data2.txt")
# data_extraction("192.168.110.10", "192.168.110.11", "./Capture\ Data/raspid2.json", "Capture\ Data/right_raspi_data2.txt")
""" CAPTURE N°3 
data_extraction("192.168.10.10", "192.168.10.11", "./Capture Data/raspig3.json", "Capture Data/left_raspi_data3.txt")
data_extraction("192.168.110.10", "192.168.110.11", "./Capture Data/raspid3.json", "Capture Data/right_raspi_data3.txt")

 CAPTURE N°4 
data_extraction("192.168.10.10", "192.168.10.11", "./Capture Data/raspig4.json", "Capture Data/left_raspi_data4.txt")
data_extraction("192.168.110.10", "192.168.110.11", "./Capture Data/raspid4.json", "Capture Data/right_raspi_data4.txt")
"""

#test :
data_extraction_lstm("192.168.110.10", "192.168.110.11", "./Capture Data/raspid_grosse.json", "Capture Data/right_lstm_raspi_data_grosse.txt")