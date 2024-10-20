import socket
import argparse

def start_udp_server(host='0.0.0.0', port=12345):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the designated host and port
    udp_socket.bind((host, port))
    
    print(f"Listening for UDP packets on {host}:{port}...")
    
    try:
        while True:
            # Receive data from the socket
            data, addr = udp_socket.recvfrom(1024)  # buffer size is 1024 bytes
            
            # Print received data and sender's address
            print(f"Received message from {addr}: {data}")
    
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    
    finally:
        udp_socket.close()

def main():

    # Argument parser for command-line input
    parser = argparse.ArgumentParser(description='host UDP server open')
    
    parser.add_argument('--ip', type=str, help='Destination IP address for UDP transmission.', default = '127.0.0.1')
    parser.add_argument('--port', type=int, help='Destination port for UDP transmission.', default = 1044)

    # Parse the arguments
    args = parser.parse_args()
    
    # start_udp_server()
    start_udp_server(host=args.ip, port=args.port)


if __name__ == "__main__":
    main()
