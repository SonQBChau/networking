#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 04/01/2021
# Description: Socket server that serve as a
# chat room
#############################################
import socket
from _thread import *
import argparse

LIMIT = 10 # The server will support up to 10 “registered” client connections

#############################################
# REGISTER THE CLIENT AND ALLOW RECEIVE 
# ANY “SERVICES” PROVIDED BY THE SERVER.
#############################################
def join_server (database, client_name, file_descriptor, connection):
    result = False
    client_obj = {"name": client_name,
            "number":file_descriptor, 
            "connection":connection}
    if (len(database) < LIMIT  ):
        # check if socket client already exist
        registed_client = search_by_connection(connection, database)
        if( registed_client == None):
            # check if username already exist
            if( search_by_name(client_name, database) == None):
                print('Client ({}): JOIN {}'.format(file_descriptor, client_name))
                message = ('JOIN {} Request Accepted \n'.format(client_name))
                broadcast_to_one(message, connection)
                database.append(client_obj)
                result = True
            else:
                message = ('This username ({}) already taken. Discarding JOIN.\n'
                .format(client_name))
                broadcast_to_one(message, connection)
                result = True
        else:
            print('Client ({}): User Already Registered.'
            ' Discarding JOIN.'.format(file_descriptor))
            message = ('User Already Registered:'
            ' Username ({}), FD ({}) \n'
            .format(registed_client['name'], registed_client['number']))
            broadcast_to_one(message, connection)
            result = True

    else:
        print('Client ({}): Database Full. Disconnecting User.'.format(file_descriptor))
        message = ('Too Many Users. Disconnecting User.\n')
        broadcast_to_one(message, connection)
    
    return result

######################################################
# LIST OF CLIENT CURRENTLY SUBSCRIBED TO THE SERVICE
######################################################
def call_list (database, connection):
    str1 = ('{:15s} {:5s}\n'.format('USERNAME', 'FD'))
    str2 = ('-' * 25 + '\n')
    str3 = ''
    for c in database:
        str3 += ('{:15s} {:<5d}\n'.format(c['name'], c['number']))
    combined_str = str1 + str2 + str3 + str2 # pretty print
    broadcast_to_one(combined_str, connection)

############################################################
# SEND AN INDIVIDUAL MESSAGE TO ANOTHER REGISTERED CLIENT
############################################################
def send_mesg(mesg, from_client, to_client, database, client_name):
    receiver = search_by_name(to_client, database)
    if(receiver != None):
        message = ('FROM {}: {}\n'.format(client_name, mesg))
        broadcast_to_one(message, receiver['connection'])
    else:
        print("Unable to Locate Recipient {} in Database. " 
        "Discarding MESG.".format(to_client))
        message = ('Unknown Recipient ({}). MESG Discarded.\n'.format(to_client))
        broadcast_to_one(message, from_client)

######################################################
# BROADCAST A MESSAGE TO ALL OTHER REGISTERED CLIENTS
######################################################
def broadcast_to_all ( mesg, from_client, database):
    c = search_by_connection(from_client, database)
    message = ('FROM {}: {}\n'.format(c['name'], mesg))
    for client in database:
        conn = client['connection']
        if conn != from_client:
            conn.send(message.encode())	

#########################################
# DISCONNECT THE CLIENT FROM THE SERVICE
# REMOVE THE DATABASE ENTRY
#########################################
def quit_server(database,file_descriptor, connection):
    c = search_by_connection(connection, database)
    if( c != None):
        database.remove(c)
        print('Client ({}): Disconneting User'.format(file_descriptor))
    else:
        print('Unable to Locate Client ({}) in Database.'
        ' Disconnecting User. \n'
        .format(file_descriptor))

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
def threaded_client(connection, database, file_descriptor):
    if(len(database) < LIMIT):
        print('Client ({}): Connection Accepted'.format(file_descriptor))
        print('Client ({}): Connection Handler Assigned'.format(file_descriptor))
        while True:
            # receive commands from user
            data = connection.recv(2048)
            string_data = data.decode('ascii')
            # the first 4 chars is the command
            command = string_data[0:4].upper()
            extra_data = string_data[5:-1]

            # JOIN and QUIT command do not need to register
            if(command == 'JOIN'):
                client_name = extra_data.strip()
                result = join_server(database, client_name, file_descriptor, connection)
                if(result == False):
                    break
            elif(command== 'QUIT'):
                    print('Client ({}): QUIT'.format(file_descriptor))
                    quit_server(database,file_descriptor, connection)
                    break # this will close connection
            else:
                # check if user registered before perform any commands
                if(search_by_connection(connection, database) != None):
                    if(command == 'LIST'):
                        print('Client ({}): LIST'.format(file_descriptor))
                        call_list(database, connection)
                    elif(command== 'MESG'):
                        from_client = connection
                        to_client, mesg = extra_data.split(" ", 1)
                        send_mesg(mesg, from_client, to_client, database, client_name)
                    elif(command == 'BCST'):
                        message = extra_data
                        broadcast_to_all(message, connection, database)
                    else:
                        print('Client ({}): Unrecognizable Message.'
                        ' Discarding UNKNOWN Message.'.format(file_descriptor))
                        message = ('Unknown Message. Discarding UNKNOWN Message.\n')
                        broadcast_to_one(message, connection)
                else:
                    print("Unable to Locate Client ({}) in database."
                    " Discarding {}.".format(file_descriptor, command))
                    message = ('Unregistered User. Use "JOIN <username>" to Register.\n')
                    broadcast_to_one(message, connection)
    else:
        print('Error: Too Many Clients Connected')
       
    connection.close()

def main(port_number):
    database = []
    # client_count = 0
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
        file_descriptor = client.fileno()
        # When a client connects, a new thread will be spawned
        start_new_thread(threaded_client, (client,database, file_descriptor, ))
        
    ServerSocket.close()
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.port_number)
