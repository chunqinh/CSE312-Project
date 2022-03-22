import socketserver
import sys
import json
import mysql.connector


# Mysql configuration
config = {
    'user': 'root',
    'password': 'root',
    # 'host': 'database',
    # 'port' : 3306,
    'database': 'cse312_db'
    }

connection = mysql.connector.connect(**config)

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recievedData = self.request.recv(1024)
        

        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == '__main__':
    host, port = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
