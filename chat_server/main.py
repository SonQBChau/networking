#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 03/30/2021
# Description: Socket server that serve as a
# chat room
#############################################
import socket
import os
from _thread import *
import argparse

# function to return the list of current connections
def list_server (connected_list):
    print('USERNAME \t FD')
    print('-' * 10)
    for c in connected_list:
        print(c['name'] + '\t' + c['number'])
    print('-' * 10)




#Function to send message to all connected clients
def broadcast_to_all ( message, connected_list):
	for socket in connected_list:
			socket.send(message)	

def search(client_name, connected_list):
    for c in connected_list:
        if c['name'] == client_name:
            return True
    return False

def join_server (connected_list, client_name,client_number):
    if (len(connected_list) <= 10  ):
        if( not search(client_name, connected_list)):
            print('Added to the list')
            connected_list.append({"name": client_name,"number":client_number})
            print(connected_list)
        else:
            print('Already added')
    else:
        print('Too Many Users')


# make connection in separate thread
def threaded_client(connection, connected_clients, client_number):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        # receive commands from user
        data = connection.recv(2048)
        string_data = data.decode('utf-8')
        # the first 4 chars is the command
        command = string_data[0:4].upper()
        extra_data = string_data[4:-1]
        if(command == 'JOIN'):
            client_name = extra_data.strip()
            if(client_name != ''):
                join_server(connected_clients, client_name, client_number)
            else:
                print('Missing name')

        elif(command == 'LIST'):
            print('LIST')
        elif(command== 'MESG'):
            print('MESG')
        elif(command == 'BCST'):
            print('BCST')
        elif(command== 'QUIT'):
            print('QUIT')
        else:
            print('Unknown Message')

        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

def main(port_number):
    connected_clients = []
    client_count = 1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = int(port_number)
    thread_count = 0
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Waiting for Incoming Connections...')
    server_socket.listen(10) # only accept maximum 10 connections

    while True:
        client, address = server_socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (client,connected_clients,client_count, ))
        thread_count += 1
        client_count += 1
        print('Thread Number: ' + str(thread_count))
    ServerSocket.close()
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.port_number)
