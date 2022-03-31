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
        recievedData = self.request.recv(2048)
        print(recievedData)

        # connection = mysql.connector.connect(**config)

        if "GET".encode() in recievedData and "/ ".encode() in recievedData:
            print("hello")
            file_size_html = os.path.getsize('cse312-html/login.html')
            file_html = open("cse312-html/login.html", "r")
            read_html = file_html.read()
            frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_html) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
            self.request.sendall(frontend.encode())
        
        elif "GET".encode() in recievedData and "/css".encode() in recievedData:
                file_size_css = os.path.getsize('cse312-html/login.css')
                file_css = open("cse312-html/login.css", "r")
                read_css = file_css.read()
                style = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_css) + "\r\nContent-Type: text/css;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_css
                self.request.sendall(style.encode())

        # elif "POST".encode() in recievedData and "/login".encode() in recievedData:
        #     print("hello")
        #     username = recievedData # in db
        #     password = recievedData # in db
        #     cursor = connection.cursor()
        #     cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        #     account = cursor.fetchone()
        #     if not account:
        #         invaild = "Wrong Password or Account doesn't exist"
        #         self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + len(invaild) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
        #     else:
        #         self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /dashboard \r\n\r\n".encode())

        print(recievedData)

        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
server = socketserver.ThreadingTCPServer((host,port), TCPHandler)
server.serve_forever()
