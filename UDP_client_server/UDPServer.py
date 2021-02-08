import argparse
import random
import socket

def main(port_number):
    buffer_size = 1024
    msg_from_server = "PONG"
    bytes_to_send = str.encode(msg_from_server)

    # Create a datagram socket
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    server_socket.bind(('127.0.0.1', int(port_number)))
    print("[server]: ready to accept data...")

    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = server_socket.recvfrom(buffer_size)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        if random.random() < .3: # simulate 30% packet loss
            print("[server]: dropped packet")
        else:# Sending a reply to client
            print("[client]: {}".format(message))
            server_socket.sendto(bytes_to_send, address)
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("PORT_NUMBER", help="Port number")
    args = parser.parse_args()

    main(args.PORT_NUMBER)