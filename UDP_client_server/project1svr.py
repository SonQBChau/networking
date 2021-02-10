#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 02/07/2021
# Description: Server UDP program accept 1 
# argument port number, simulate 30% packet loss
# through random number, print PING when receive
# message from client then send a message back
# Use Ctrl-C or Ctrl-Break to terminate the program
#############################################
import argparse
import random
import socket

def main(port_number):
    buffer_size = 1024
    msg_from_server = "PONG"
    bytes_to_send = str.encode(msg_from_server)

    # Create a UDP socket at server side
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', int(port_number))) #0.0.0.0 means all ip can connect to it
    print("[server]: ready to accept data...")

    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = server_socket.recvfrom(buffer_size)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print("[message]: {}".format(message))

        if random.random() < .3: # simulate 30% packet loss
            print("[server]: dropped packet")
        else:# Sending a reply to client
            print("[client]: {}".format(message))
            server_socket.sendto(bytes_to_send, address)
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.port_number)