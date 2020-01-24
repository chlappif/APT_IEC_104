# APT_IEC_104
PFE project : prove the threat of APTs with IEC_104 protocol

##Deep Learning Part : 

When you retrieved the data from the system, the first thing to do it to run the __extractor.py__ code. Then, run the deep learning algorithm.


**EVERYTHING WAS DONE CORRECTLY ON THE RIGHT SIDE OF THE SYSTEM, AND THE CODE WAS JUST ADAPTED BUT NEVER RAN ON THE LEFT SIDE. THE EXTRACTOR FILE SHOULD BE ADAPTED FOR THE LEFT SIDE.**

One might need to adapt the names of the files containing the data, and the names of the directories. 

###extractor.py : 

Extract as JSON the Wireshark network capture. Sort by Rpi the data before extracting as JSON in Wireshark. The center Raspberry should always be contained in the left and right data files.

The extracted time parameter in this version of the extractor should be removed for non lstm data. It is just there to make sure to keep the order between data elements.

###Learning Algorithms :

Some booleans values should be adapted in the code to determine whether it should do a training session, or a testing session, or both.

Everything is explained in the code itself. 
