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
import sys 
import socket 
from contextlib import closing
import errno
import select
import struct

# attempt to get port name
def get_port_name(port, protocol):
    service_name = 'svc name unavail'
    try: # attempt to get port name
        service_name = socket.getservbyport(port, protocol)
    except:
        pass
    return service_name

# run specific protocol on port range
def scan_ports(host_ip, protocol,port_low, port_high):
    if protocol.lower() == 'tcp':
        for port in range(port_low, port_high+1):
            tcp_scan(host_ip, port)
    elif protocol.lower() == 'udp':
        for port in range(port_low, port_high+1):
            udp_scan(host_ip, port)
    else:
        print('invalid protocol: {}. Specify "tcp" or "udp"'.format(protocol))
        
# perform tcp scan for each port
def tcp_scan(ip, port):
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(1)
    try:
        service_name = get_port_name(port, 'tcp')
        if not tcp.connect((ip, port)): # port is open
            print("Port {} open: {}".format(port, service_name)) 
    except Exception as e: # ignore refused connection
        pass
    finally: # close port when done
        tcp.close()
    
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # time out set to 1 second
    socket.setdefaulttimeout(1) 
    service_name = 'svc name unavail'
    try:
        #check if the service available 
        service_name = socket.getservbyport(port, 'tcp')
    except:
        pass
    # check for connection open or  not
    result = s.connect_ex((ip,port)) 
    if result == 0: 
        print("Port {} open: {}".format(port, service_name)) 
    else:
        print("Port {} closed: {}".format(port, service_name)) 
    s.close() 
    '''

    

# perform udp scan
def udp_scan(ip, port):
    service_name = 'svc name unavail'
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(1)
    

    portOpen = False
    have_name = False
    bytes_to_send = str.encode('hello')
    port_open = False
 
    for _ in range(5): # UDP packet loss may occur so we send twice to make sure
        try:
            udp.connect( (ip, port)) 
            udp.send(bytes(0))
            udp.recv(1024)
            print("Port {} open: {}".format(port, service_name)) 
            break

        except socket.timeout:
            try:
                service_name = socket.getservbyport(port, 'udp')
            except:
                pass
            print("Port {} open filtered: {}".format(port, service_name)) 
            break

        except socket.error:
            # print("Port {} closed: {}".format(port, service_name)) 
            continue
        finally:   
            udp.close()
    if not port_open:
            try:
                service_name = socket.getservbyport(port, 'udp')
            except:
                pass
            print("Port {} closed: {}".format(port, service_name)) 


    udp.close() 


    

def main(hostname, protocol, portlow, porthigh):
    print ("scanning host={}, protocol={}, ports: {} -> {}".
    format(hostname, protocol, portlow, porthigh))
    # check valid hostname
    try:
        host_ip = socket.gethostbyname(hostname)
        scan_ports(host_ip, protocol, int(portlow), int(porthigh))
    except socket.gaierror:
        print('host {} not exist'.format(hostname))

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="host name of the machine you want to run the port scanner e.g. cse05")
    parser.add_argument("protocol", help="TCP or UDP")
    parser.add_argument("portlow", help="lower range, inclusively, of ports to scan e.g. 1")
    parser.add_argument("porthigh", help="upper range, inclusively, of ports to scan e.g. 120")
    args = parser.parse_args()

    main(args.hostname, args.protocol, args.portlow, args.porthigh)