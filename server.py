import socketserver
import sys
import json
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'database',
    'database': 'cse312_db'
}

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        recievedData = self.request.recv(1024)
        connection = mysql.connector.connect(**config)

        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == '__main__':
    host, port = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
