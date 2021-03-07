import socketserver
import json
import threading
import time
import client
import hive.game as hive

server_address = "localhost" #"192.168.0.22"


class HiveClientHandler(socketserver.BaseRequestHandler):
    server_players = 0

    def handle(self):
        """ Main handler. Understands all the actions for each request. """
        sock = self.request
        connected = True
        while connected:
            json_recv = client.receive_json(sock)

            # If the client wants something from us they will begin with a request
            if json_recv.get('request'):

                # Give the client and id so we can keep track of them
                if json_recv['request'] == 'connect':
                    reply = {'client_id': self.server_players}
                    client.send_json(sock, reply)
                    self.server_players += 1

                # Give the client the game and tell them which player they are
                elif json_recv['request'] == 'get_game':
                    # TODO: give the client the game
                    
                    reply = {
                             'game': json.dumps(server_game.export_json()),
                             'player_id': 0
                            }
                    client.send_json(sock, reply)


class HiveServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    host, port = server_address, client.PORT

    # Create a game for this server to use. Only one game can be played in one server like this.
    server_game = hive.Game()

    with HiveServer((host, port), HiveClientHandler) as server:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        while True:
            print(f"Server still alive. Process sleeping for 60secs")
            time.sleep(60)




"""
Client sends connect
{'request': 'connect'}
Server sends:
{'client_id': 0} # this is the id of the client and is unique in the server

Client sends request game
{'request': 'get_game'}
Server sends
# the game json and the player that client is in the game
{'game': game_json, 'player_id': player_id}

Server sends request move
{'request': 'move'}
Client sends
{'move': move_json}
Server sends
{'move': 'valid'}
"""