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
import socket 
import time

# get port name from the built-in list
# return 'svc name unavail' otherwise
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
        print('udp scan is slow, please wait....')
        for port in range(port_low, port_high+1):
            udp_scan(host_ip, port)
    else:
        print('invalid protocol: {}. Specify "tcp" or "udp"'.format(protocol))
        
# perform tcp scan for each port
# return only open port
def tcp_scan(ip, port):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(1)
    try:
        service_name = get_port_name(port, 'tcp')
        if not tcp.connect((ip, port)): # only print open port like sample
            print("Port {} open: {}".format(port, service_name)) 
    except Exception as e: # ignore refused connection
        pass
    finally: # close port when done
        tcp.close()


# perform udp scan for each port
# return 
def udp_scan(ip, port):
    retries = 3 # UDP loss may occur so we send mutiple times
    port_open = False
    port_filter_open = False
 
    for i in range(retries): 
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # adjust timeout will detect more or less false positive
        # 1 second works best for me
        udp.settimeout(1)
        try:
            # if receive packet, the port is open
            udp.connect((ip, port)) 
            udp.send(bytes(0))
            udp.recv(1024)
            port_open = True 
            break
        
        except socket.timeout:
            # if socket timeout, the port maybe open 
            # since server does not send anything back  
            # after playing with timeout and sleep, I found that
            # second packet most likely indicate the port open or close
            if i == 1:
                port_filter_open = True
            continue

        except socket.error:
            # if socket error, port is closed
            if i == 1:
                port_open = False
            continue 
        finally:   
            udp.close()
            time.sleep(0.1)
        
       
    service_name = get_port_name(port, 'udp')

    # print out open and closed ports and filtered out unwanted outputs
    if  port_open:
        print("Port {} open: {}".format(port, service_name)) 
    elif port_filter_open and service_name != 'svc name unavail':
        print("Port {} open: {}".format(port, service_name)) 
    elif not port_filter_open and service_name != 'svc name unavail':
        print("Port {} closed: {}".format(port, service_name)) 
    elif not port_open and service_name != 'svc name unavail':
        print("Port {} closed: {}".format(port, service_name)) 
        


    # udp.close() 


    

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