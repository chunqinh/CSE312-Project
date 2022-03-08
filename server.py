import socketserver
import sys
import json
from pymongo import MongoClient


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        return


if __name__ == '__main__':
    host, port = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
