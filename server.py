import socketserver
import sys
import json
import os
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

        if "POST".encode() in recievedData and "/login".encode() in recievedData:
            print("hello")

            # file_size_html = os.path.getsize('cse312-html/login.html')
            # file_html = open("cse312-html/login.html", "r")
            # read_html = file_html.read()
            # print(read_html)
            # frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_html) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
            # self.request.sendall(frontend.encode())
        #get the username and password from request
            #check in the database if that is in it
            #if not return a message with invaild password or else redirect to dashboard


        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == '__main__':
    host, port = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
