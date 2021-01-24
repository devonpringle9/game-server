import socketserver
import json

server_address = "localhost" #"192.168.0.22"
server_port = 9000


class MyServer(socketserver.BaseRequestHandler):

    server_players = 0

    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        try:
            json_recv = json.loads(self.data)
            if json_recv.get('connect'):
                reply = {'your_player_number': self.server_players}
                server_players += 1
                self.request.sendall(json.dumps(reply).encode('utf-8'))
        except Exception as e:
            print("wasnt json", e, 'was the error', self.data)


        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

if __name__ == "__main__":
    host, port = server_address, server_port

    with socketserver.TCPServer((host, port), MyServer) as server:
        server.serve_forever()




"""
Client sends:
{"connect": true}
Server sends:
{'your_player_number': 0} # this is the id of the client and is unique in the server
Server sends:
json of the game + whos turn it is
"""