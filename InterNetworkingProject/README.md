# Packet Parser
I recently began learning Socket programming and, like many others, was introduced to [Wireshark](https://www.wireshark.org/). Wireshark is a network traffic analysis and monitoring software suite that uses a packet sniffer as its foundation. This is a Python-based attempt at creating a rudimentary packet sniffer.

## What is the purpose of a packet parser?
Any traditional network transports data in packets created by one server (or computer) and forwarded to one or more other servers on the same network. One might want to examine the traffic produced by such a network for security concerns or just to be curious. This entails "sniffing" or detecting packets as they pass across the network and decoding their contents. The result is a packet sniffer.

You should learn about [sockets](https://medium.com/swlh/understanding-socket-connections-in-computer-networking-bac304812b5c) and the [structure of an IPv4 network packet](https://en.wikipedia.org/wiki/IPv4#Packet structure) to comprehend the code. The [Socket API](https://docs.python.org/3/library/socket.html) is used in the software.

##Features of the tool
Only IPv4 packets are captured by the present Python implementation, which offers the following information:
- Destination and Source MAC address
- Ethernet Protocol 
- Protocol used (e.g. TCP Packet == 6, UDP == 17)
- TTL (Time-to-Live)
- Header length

## To run:
The software currently requires a Linux system with Python3 installed. Although a packet sniffer should not be OS-specific, that development is still ongoing. You'll also need root privileges to launch it. 
I'm using the following command: 
"""
sudo python3 Packet_parser.py
"""