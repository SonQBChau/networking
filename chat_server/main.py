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
import queue
import argparse

LIMIT = 1 # The server will support up to 10 “registered” client connections

#############################################
# REGISTER THE CLIENT AND ALLOW RECEIVE 
# ANY “SERVICES” PROVIDED BY THE SERVER.
#############################################
def join_server (database, client_name, client_number, connection):
    result = False
    client_obj = {"name": client_name,
            "number":client_number, 
            "connection":connection}
    if (len(database) < LIMIT  ):
        if( search_by_connection(connection, database) == None):
            print('Client {}: JOIN {}'.format(client_number, client_name))
            database.append(client_obj)
            result = True
        else:
            print('Already added')
    else:
        print('Client {}: Database Full. Disconnecting User.\n'.format(client_number))
        message = ('Too Many Users. Disconnecting User.')
        broadcast_to_one(message, connection)
    
    return result

######################################################
# LIST OF CLIENT CURRENTLY SUBSCRIBED TO THE SERVICE
######################################################
def call_list (connected_list, connection):
    str1 = ('USERNAME \t FD\n')
    str2 = ('-' * 20 + '\n')
    str3 = ''
    for c in connected_list:
        str3 += ('{} \t\t {} \n'.format(c['name'], c['number']))

    combined_str = str1 + str2 + str3 + str2
    broadcast_to_one(combined_str, connection)

######################################################
# BROADCAST A MESSAGE TO ALL OTHER REGISTERED CLIENTS
######################################################
def broadcast_to_all ( mesg, from_client, database):
    c = search_by_connection(from_client, database)
    message = ('FROM {}: {}'.format(c['name'], mesg))
    for client in database:
        conn = client['connection']
        if conn != from_client:
            conn.send(message.encode())	

############################################################
# SEND AN INDIVIDUAL MESSAGE TO ANOTHER REGISTERED CLIENT
############################################################
def send_mesg(mesg, from_client, to_client, database):
    
    receiver = search_by_name(to_client, database)
    if(receiver != None):
        message = ('FROM {}: {}'.format(receiver['name'], mesg))
        broadcast_to_one(message, receiver['connection'])
    else:
        print("Unable to Locate Recipient {} in Database." 
        "Discarding MESG.".format(to_client))
        message = ('Unknown Recipient {}. MESG Discarded.'.format(to_client))
        broadcast_to_one(message, from_client)

#########################################
# DISCONNECT THE CLIENT FROM THE SERVICE
# REMOVE THE DATABASE ENTRY
#########################################
def quit_server(connected_list,client_number, connection):
    c = search_by_connection(connection, connected_list)
    if( c != None):
            connected_list.remove(c)
    else:
        print('Unable to Locate Client {} in Database.'.format(client_number))

# SEARCH A CLIENT'S SOCKET FILE IN THE DATA BASE
def search_by_connection(connection, database):
    for c in database:
        if c['connection'] == connection:
            return c
    return None

# SEARCH A CLIENT'S NAME IN THE DATA BASE
def search_by_name(name, database):
    for c in database:
        if c['name'] == name:
            return c
    return None

# BROADCAST A MESSAGE TO ONE
def broadcast_to_one(message, connection):
    connection.send(message.encode())

# MAKE NEW CONNECTION IN SEPARATE THREAD
def threaded_client(connection, database, client_number):
    if(len(database) < LIMIT):
        print('Client {}: Connection Accepted'.format(client_number))
        print('Client {}: Connection Handler Assigned'.format(client_number))
        while True:
            # receive commands from user
            data = connection.recv(2048)
            string_data = data.decode('utf-8')
            # the first 4 chars is the command
            command = string_data[0:4].upper()
            extra_data = string_data[5:-1]

            if(command == 'JOIN'):
                client_name = extra_data.strip()
                result = join_server(database, client_name, client_number, connection)
                if(result == False):
                    break
            elif(command== 'QUIT'):
                    print('Client {}: QUIT'.format(client_number))
                    quit_server(database,client_number, connection)
                    print('Client {}: Disconneting User'.format(client_number))
                    break
            else:
                # check if user register before perform any commands
                if(search_by_connection(connection, database) != None):
                    if(command == 'LIST'):
                        print('Client {}: LIST'.format(client_number))
                        call_list(database, connection)
                    elif(command== 'MESG'):
                        from_client = connection
                        to_client, mesg = extra_data.split(" ", 1)
                        send_mesg(mesg, from_client, to_client, database)
                    elif(command == 'BCST'):
                        message = extra_data
                        broadcast_to_all(message, connection, database)
                
                    else:
                        print('Unknown Message')
                else:
                    print("Unable to Locate Client {} in database."
                    "Discarding {}".format(client_number, command))
    else:
        print('Error: Too Many Clients Connected')
       

    connection.close()

def main(port_number):
    connected_clients = []
    client_count = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = int(port_number)
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Waiting for Incoming Connections...')
    server_socket.listen(10) 

    while True:
        client, address = server_socket.accept()
        client_count += 1
        # When a client connects, a new thread will be spawned
        start_new_thread(threaded_client, (client,connected_clients,client_count, ))
        
    ServerSocket.close()
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.port_number)
