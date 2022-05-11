"""
  The real stuff. 
"""

import socket
import struct
import sys
import textwrap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t'
DATA_TAB_2 = '\t\t'
DATA_TAB_3 = '\t\t\t'
DATA_TAB_4 = '\t\t\t\t'


# create a network socket using the default constructor

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    except socket.error:
        print('Socket could not be created.')
        sys.exit(1)

    # while loop runs infinitely to capture any incoming packets
    while True:

        # listen on port 65565
        raw_data, address = sock.recvfrom(65565)
        destination_mac, src_mac, ethernet_proto = struct.unpack('! 6s 6s H', raw_data[:14])

        # packet parameters
        destination_mac = get_mac_address(destination_mac)
        src_mac = get_mac_address(src_mac)
        ethernet_proto = socket.htons(ethernet_proto)
        data = raw_data[14:]

        print('\nEthernet frame:')
        print(TAB_1 + 'Destination: {}, Source: {}, Ethernet Protocol: {}'.format(destination_mac, src_mac,
                                                                                  ethernet_proto))

        # 8 for IPV4
        # analyse only IPv4 packets (I know IPv6 is the real deal but this should work for now)
        if ethernet_proto == 8:
            version, header_len, ttl, proto, src, target, data = ipv4_packet(data)
            print(TAB_1 + 'IPV4 Packet:')
            print(TAB_2 + f'version: {version}, Header Length: {header_len}, TTl: {ttl}')
            print(TAB_3 + f'Protocol : {proto} , Source: {src}, Target: {target}')

            if proto == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print(TAB_1 + 'ICMP Packet: ')
                print(TAB_2 + f'Type: {icmp_type}, Code: {code}, Checksum: {checksum}')
                print(TAB_2 + f'Data: {data}')
                print(format_multi_line(DATA_TAB_3, data))

            # TCP
            elif proto == 6:
                src_prt, dest_port, sequence, ack, offset, flg_ack, flg_fin, flg_syn, flg_rst, flg_urg, flg_psh, data = \
                    tcp_packet(data)
                print(TAB_1 + 'TCP Segment:')
                print(TAB_2 + f'Source Port: {src_prt}, Destination port:{dest_port}, Sequence: {sequence}')
                print(TAB_2 + f'Acknowledgment: {ack}')
                print(TAB_2 + 'Flags:')
                print(TAB_3 + f'URG: {flg_urg}, ACK: {flg_ack}, PSH: {flg_psh}, SYN: {flg_syn}, FIN: {flg_fin}')
                print(TAB_2 + 'Data:')
                print(format_multi_line(DATA_TAB_3, data))

            # UDP
            elif proto == 17:
                src_prt, dst_port, size, data = udp_packet(data)
                print(TAB_1 + 'UDP Segment:')
                print(TAB_2 + f'Source port: {src_prt}, Destination port: {dst_port}, Length: {size}')

            # Other
            else:
                print(TAB_1 + 'Data:')
                print(format_multi_line(DATA_TAB_2, data))
        else:
            print(TAB_1 + 'Data:')
            print(format_multi_line(DATA_TAB_2, data))


def get_mac_address(bytes_string):
    bytes_string = map('{:02x}'.format, bytes_string)
    destination_mac = ':'.join(bytes_string).upper()
    return destination_mac


# Unpacks the ICMP packet

def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]


# Unpack the TCP packet

def tcp_packet(data):
    src_prt, dest_port, sequence, ack, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flg_urg = (offset_reserved_flags & 32) >> 5
    flg_ack = (offset_reserved_flags & 16) >> 4
    flg_psh = (offset_reserved_flags & 8) >> 3
    flg_rst = (offset_reserved_flags & 4) >> 2
    flg_syn = (offset_reserved_flags & 2) >> 1
    flg_fin = (offset_reserved_flags & 1)
    return src_prt, dest_port, sequence, ack, offset, flg_ack, flg_fin, \
           flg_syn, flg_rst, flg_urg, flg_psh, data[offset:]


# unpack IPv4 packet

def ipv4_packet(data):
    version_header_len = data[0]
    version = version_header_len >> 4
    header_len = (version_header_len & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_len, ttl, proto, ipv4(src), ipv4(target), data[header_len:]


# return properly formatted IPv4 address
def ipv4(addr):
    return '.'.join(map(str, addr))


# upacks the UDP packet

def udp_packet(data):
    src_prt, dst_port, size = struct.unpack('! H H 2X H', data[:8])
    return src_prt, dst_port, size, data[8:]


# Formats Multi-line data

def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02X}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])
