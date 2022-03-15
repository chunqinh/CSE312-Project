import socketserver
import sys
import json
from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse312_project"]
user_collection = db["users"]
user_id_collection = db["user_id"]


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recievedData = self.request.recv(1024)

        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == '__main__':
    host, port = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
