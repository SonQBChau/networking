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



def scan_range(host_ip, port_low, port_high):
    for port in range(port_low, port_high+1):
        tcp_scan(host_ip, port)
        


def tcp_scan(ip, port):
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        service_name = socket.getservbyport(port, 'tcp')
        if not tcp.connect_ex((ip, port)):
            print("Port {} open: {}".format(port, service_name)) 
        else:
            print("Port {} closed: {}".format(port, service_name)) 
        tcp.close()
    except OSError:
        print("svc name unavail")
    except Exception:
        pass


  

        
   
   

def main(hostname, protocol, portlow, porthigh):
    socket.setdefaulttimeout(1)
    print ("scanning host={}, protocol={}, ports: {} -> {}".format(hostname, protocol, portlow, porthigh))
    host_ip = socket.gethostbyname(hostname)
    scan_range(host_ip, int(portlow), int(porthigh))

    '''

    print ("scanning host={}, protocol={}, ports: {} -> {}".format(hostname, protocol, portlow, porthigh))
    host_ip = socket.gethostbyname('localhost')
    #print("host name IP is: {}".format(target))

    if protocol  == 'tcp':
        for port in range(int(portlow), int(porthigh)+1): 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            # time out set to 1 second
            socket.setdefaulttimeout(1) 
            service_name = 'svc name unavail'
            try:
                #check if the service available 
                service_name = socket.getservbyport(port, protocol)
            except:
                pass
            # check for connection open or  not
            result = s.connect_ex((host_ip,port)) 
            if result == 0: 
                print("Port {} open: {}".format(port, service_name)) 
            else:
                print("Port {} closed: {}".format(port, service_name)) 
            s.close() 
     
            
       
    elif protocol  == 'udp':
        # scan ports from low to high
        for port in range(int(portlow), int(porthigh)+1): 
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # time out set to 1 second
                socket.setdefaulttimeout(1) 
                service_name = 'svc name unavail'
                try:
                    #check if the service available 
                    service_name = socket.getservbyport(port, protocol)
                except:
                    pass
                # check for connection open or  not
                result = s.connect_ex((host_ip,port)) 
                if result == 0: 
                    print("Port {} open: {}".format(port, service_name)) 
                else:
                    print("Port {} closed: {}".format(port, service_name)) 
                s.close() 
            except KeyboardInterrupt: 
                print("Exitting Program !!!!") 
                sys.exit() 
            except socket.gaierror: 
                    print("Hostname Could Not Be Resolved !!!!") 
                    sys.exit() 
            except socket.error: 
                    print("Server not responding !!!!") 
                    sys.exit() 
    else:
        print("unknown protocol")
   
    '''


  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="host name of the machine you want to run the port scanner e.g. cse05")
    parser.add_argument("protocol", help="TCP or UDP")
    parser.add_argument("portlow", help="lower range, inclusively, of ports to scan e.g. 1")
    parser.add_argument("porthigh", help="upper range, inclusively, of ports to scan e.g. 120")
    args = parser.parse_args()

    main(args.hostname, args.protocol, args.portlow, args.porthigh)