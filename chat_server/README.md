The program consist of a server that will implement a service (like a chat
room) using a simple text protocol that clients can use (through telnet) to message other clients on the service.

This project is written in python3. 

##### To run it on CSE server, follow the instruction:
1. Put prog3svr.py on any server, let say cse01

2. Type the following commands in the terminal:
* For Server cse01:
    ```python3 prog3svr.py 8001```
* For Client cse02:
    ```telnet cse01 8001```

##### Usage (can be in lowercase or uppercase):
```JOIN username ```
When a client wants to join (i.e., register for) the service, it first connects to
the server using the telnet command with the hostname of the server CSE
machine and the port number, and then sends a JOIN request with the
username. Usernames will only consist of alphanumeric characters and
will not contain spaces or other “special” or control characters. You may
assume that the user follows this requirement for alphanumeric
characters, so no validation is needed. The server will store this username
as well as the client’s socket file descriptor in the “database”. Note that
although a client may “connect” to the server, it MUST register for the
service with the JOIN command before the client may receive any
“services” provided by the server. If the database is “full” (i.e., 10 clients
have registered for the service), then the server will print out a status
message and send a “Too Many Users” message to the client. Once a
client has already registered with a JOIN request, any subsequent JOIN
requests from the same registered client will be discarded with a status
message sent back to the client.

```LIST ```
If a registered client wants to know who is currently subscribed to the
service, the client will issue a LIST request. Upon receipt of the LIST
request, the server will send a list of all registered clients on individual
lines and return this list (newlines and all) to the client. Note that the client
must be registered for the service to receive any “services”, such as this
one, provided by the server. If the client who is not registered for this
service sends a LIST request, the server will print out a status message
and send an “Unregistered User” message to the client with the JOIN
request instructions.

```MESG username some_message_text ```
If a registered client wants to send an individual message to another
registered client, the client will issue the MESG request with the username
of a registered client followed by whatever message he/she wants to send
to the other registered client. The server will then act as a relay and
forward this message to the registered user. Note that the client must be
registered for the service to receive any “services”, such as this one,
provided by the server. If the client who is not registered for this service
sends a MESG request, the server will print out a status message and send
an “Unregistered User” message to the client with the JOIN request
instructions. If a registered client sends a MESG request to an unregistered
client, the server will print out a status message and send an “Unknown
Recipient” message to the client.

```BCST some_message_text ```
If a registered client wants to broadcast a message to all other registered
clients, the client will issue the BCST request followed by whatever
message he/she wants to send to the other registered clients. The server
will then act as a relay and forward this message to the registered users
(but not the sender). Note that the client must be registered for the service
to receive any “services”, such as this one, provided by the server. If the
client who is not registered for this service sends a BCST request, the
server will print out a status message and send an “Unregistered User”
message to the client with the JOIN request instructions.

```QUIT ```
When a connected client wants to leave the service, the client will issue a
QUIT request, at which time the server will disconnect the client from the
service. The database entry for registered clients should be removed after
the client has been disconnected. Note that an unregistered client will still
be disconnected from the service (i.e., their connection closed) with a
status message at the server, though no data needs to be removed form
the database since there is none for that client.

###### Unrecognizable Messages
• If a registered client sends an unrecognizable request (i.e., one not
supported by this protocol), the server will print out a status message and
send an “Unknown Message” message to the client.
• Note that the client must be registered for the service to receive any
“services” provided by the server. If the client who is not registered for this
service sends an unrecognizable message, the server will print out a
status message and send an “Unregistered User” message to the client
with the JOIN request instructions.