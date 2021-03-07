import socket
import sys
import json
import hive.game as hive
import time

DEBUG = 1
HOST, PORT = "localhost", 9002


def receive_json(sock, recv_size=1024):
    """ Wrapper for receiving a json from the server """
    try:
        received = str(sock.recv(recv_size), 'utf-8')
    except Exception as e:
        raise Exception(f"Got an error when trying to receive: {e}")
        return None

    json_recv = None
    try:
        json_recv = json.loads(received)
        if DEBUG: print("Received json:", json_recv, type(json_recv))
    except Exception as e:
        raise Exception(f"Didnt receive valid json: {received}")

    return json_recv

def send_json(sock, json_to_send):
    """ Wrapper for easily sending a json (dict) """
    print("Sending:", json_to_send)
    sock.sendall(bytes(json.dumps(json_to_send) + "\n", "utf-8"))


def print_board(players):
    players = []
    for player in players:
        # print spaces until the player
        for space in range(player.spaces):
            sys.stdout.write(' ')
        print(player.token)


def connect_to_game_server(sock):
    """ Connect to the server to know we want to play and get an id from the server """
    data = {'request': 'connect'}
    send_json(sock, data)
    received_json = receive_json(sock)
    return received_json['client_id']


def request_game(sock):
    """ Get the game json and this client's player in the game """
    data = {'request': 'get_game'}
    send_json(sock, data)
    received_json = receive_json(sock, recv_size=16384)

    json.loads(received_json['game'])

    
    return json.loads(json.loads(received_json['game'])), received_json['player_id']



if __name__ == "__main__":

    # A game for this client to use
    game = hive.Game()

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        player_number = connect_to_game_server(sock)
        print(f"You are connected with client_id: {player_number}")

        # Get the game to create a game instance
        game_json, player_id = request_game(sock)

        game.import_json(game_json)


        # Everytime we are asked for a move, lets give it to them
        # request_count = 0
        # while request_count < 4:
        #     print(connect_to_game_server(sock))
        #     request_count += 1
        #     time.sleep(1)
        # time.sleep(4)
