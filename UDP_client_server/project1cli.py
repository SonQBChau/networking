#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 02/07/2021
# Description: Client UDP program to send and
# receive packet, calculate round trip time,
# assume packet loss in 1 second and print
# the summary status
#############################################
import argparse
import socket
import timeit
from statistics import mean


def main(host_name, port_number):
    client_msg = "PING"
    bytes_to_send = str.encode(client_msg)
    buffer_size = 1024
    trials = 10
    no_msg_received = 0
    no_msg_loss = 0
    rtt_list = []

    # Create a UDP socket at client side
    client_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # time out set to 1 second
    client_socket.settimeout(1)

    for trial in range(0, trials):
        print("{}: Sent...".format(trial+1), end=" ")
        try:
            start = timeit.default_timer()  # start timing
            # Send to server using created UDP socket
            client_socket.sendto(bytes_to_send, (host_name, int(port_number)))
            msg_from_server = client_socket.recvfrom(buffer_size) # receive back from server
            stop = timeit.default_timer()  # stop timing
            rtt = (stop - start) * 1000
            print("RTT={:.6f} ms".format(rtt))
            rtt_list.append(rtt)
            no_msg_received += 1

        except:
            print("Request time out!")
            no_msg_loss += 1

    print("The number of messages sent: {}".format(trials))
    print("The number of messages received: {}".format(no_msg_received))
    print("The message loss rate: {:.0%}".format(no_msg_loss/trials))
    print("The maximum RRT: {:.6f} ms".format(max(rtt_list)))
    print("The minimum RRT: {:.6f} ms".format(min(rtt_list)))
    print("The average RRT: {:.6f} ms".format(mean(rtt_list)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host_name", help="For example: cse05")
    parser.add_argument("port_number", help="For example: 8001")
    args = parser.parse_args()

    main(args.host_name, args.port_number)
