#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 03/07/2021
# Description: network port scanner that will 
# report the status of services and their associated 
# ports for the TCP and UDP protocols for a given port range
# given a host name of a machine and a list of ports to scan. 
# The scanner will connect to each port using sockets with 
# the specified protocol (i.e., TCP or UDP) to determine 
# whether or not the port is open based on the success of a 
# connection request and then close the socket before 
# moving on to the next port to scan
#############################################
import argparse

def main(hostname, protocol, portlow, porthigh):
    print(hostname)
    print(protocol)
    print(portlow)
    print(porthigh)
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="host name of the machine you want to run the port scanner e.g. cse05")
    parser.add_argument("protocol", help="TCP or UDP")
    parser.add_argument("portlow", help="lower range, inclusively, of ports to scan e.g. 1")
    parser.add_argument("porthigh", help="upper range, inclusively, of ports to scan e.g. 120")
    args = parser.parse_args()

    main(args.hostname, args.protocol, args.portlow, args.porthigh)