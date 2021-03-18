from socket import *
import argparse

def main(port_number):
    serverPort = int(port_number)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.port_number)