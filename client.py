import socket
import sys
import json

HOST, PORT = "localhost", 9000


def print_board(players):
    players = []
    for player in players:
        # print spaces until the player
        for space in range(player.spaces):
            sys.stdout.write(' ')
        print(player.token)


def connect(sock):
    data = {'connect': True}
    sock.sendall(bytes(json.dumps(data) + "\n", "utf-8"))


if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        player_number = connect(sock)

        # Everytime we are asked for a move, lets give it to them
        request_count = 0
        while request_count < 1:
            received = str(sock.recv(1024), "utf-8")
            try:
                json_recv = json.loads(received)
                print("got this", json_recv)
            except Exception:
                print("Didnt receive json")
                print(received, '...nothing')
            request_count += 1
