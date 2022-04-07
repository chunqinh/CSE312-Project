import socketserver
import sys
import json
import os
import mysql.connector


class TCPHandler(socketserver.BaseRequestHandler):
    
    config = {
    'user': 'root',
    'password': 'root',
    'host': 'database',
    'database': '312project_db'
    }

    def handle(self):
        recievedData = self.request.recv(2048).strip()
        print(recievedData)

        if "GET".encode() in recievedData and "/signup".encode() in recievedData:
            file_size_html = os.path.getsize('cse312-html/signup.html')
            file_html = open("cse312-html/signup.html", "r")
            read_html = file_html.read()
            frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(read_html.encode())) + "\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n" + read_html
            self.request.sendall(frontend.encode())

        elif "GET".encode() in recievedData and "/ ".encode() in recievedData:
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

        elif "POST".encode() in recievedData and "/signup".encode() in recievedData:
            print(recievedData)
            header = recievedData.find(b'\r\n\r\n')
            head = recievedData[0:header]
            new_line = head.split(b'\r\n')
            start_boundary = b'boundary'
            for x in new_line:
                if start_boundary in x:
                    start = x.find(start_boundary)
                    need_boundary = x[start + len(start_boundary) + 1:]  # boundary=
            boundary = b"--" + need_boundary  # -- + boundary
            body = recievedData[header + len(b'\r\n\r\n'):]
            print(body)
            body_lst = body.split(boundary + b'\r\n')  # split using boundary
            start_username = b'"username"\r\n\r\n'
            start_password = b'"password"\r\n\r\n'
            start_password2 = b'"password2"\r\n\r\n'
            insert_username = ''
            insert_password = ''
            password2 = ''
            for x in body_lst:
                if start_username in x:
                    start_index_username = x.find(start_username)
                    need_username = x[start_index_username + len(start_username):]
                    size_username = len(need_username)
                    insert_username = need_username[:size_username - len(b'\r\n')].decode()

                elif start_password in x:
                    start_index_password = x.find(start_password)
                    need_password = x[start_index_password + len(start_password):]
                    size_password = len(need_password)
                    insert_password = need_password[:size_password - len(b'\r\n')].decode()

                elif start_password2 in x:
                    start_index_password2 = x.find(start_password2)
                    need_password2 = x[start_index_password2 + len(start_password2):]
                    size_password2 = len(need_password2)
                    last_boundary = b'\r\n' + boundary + b'--'  # \r\n-- + boundary + --
                    password2 = need_password2[:size_password2 - len(last_boundary)].decode()

            print(insert_username)
            print(insert_password)
            print(password2)

            if insert_password != password2:
                self.request.sendall("HTTP/1.1 403 Forbidden\r\nContent Length: 22\r\nContent-Type: text/html\r\nX-Content-Type-Options: nosniff\r\n\r\nPasswords do not match".encode())

            connection = mysql.connector.connect(**TCPHandler.config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user(username, password) VALUES(%s,%s)", (insert_username, insert_password))
            connection.commit()
            cursor.close()
            invaild = "Wrong Password or Account doesn't exist"
            self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + str(len(invaild)) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
                

        elif "POST".encode() in recievedData and "/login".encode() in recievedData:
            print(recievedData)
            print("hello")
            header = recievedData.find(b'\r\n\r\n')
            head = recievedData[0:header]
            new_line = head.split(b'\r\n')
            start_boundary = b'boundary'
            for x in new_line:
                if start_boundary in x:
                    start = x.find(start_boundary)
                    need_boundary = x[start + len(start_boundary)+1:] #boundary=
            boundary = b"--" + need_boundary # -- + boundary
            body = recievedData[header + len(b'\r\n\r\n'):]
            print(body)
            body_lst = body.split(boundary + b'\r\n') # split using boundary
            start_username = b'"username"\r\n\r\n'
            start_password = b'"password"\r\n\r\n'
            username = ''
            password =''
            for x in body_lst:
                if start_username in x:
                    start_index_username = x.find(start_username)
                    need_username = x[start_index_username + len(start_username):]
                    size_username = len(need_username)
                    username = need_username[:size_username - len(b'\r\n')].decode()
                    
                elif start_password in x:
                    start_index_password = x.find(start_password)
                    need_password = x[start_index_password + len(start_password):]
                    size_password = len(need_password)
                    last_boundary = b'\r\n' + boundary + b'--' # \r\n-- + boundary + --
                    password = need_password[:size_password - len(last_boundary)].decode()
                    
            
            print(username)
            print(password)
            connection = mysql.connector.connect(**TCPHandler.config)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            print(account)
            if not account:
                invaild = "Wrong Password or Account doesn't exist"
                self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + str(len(invaild)) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
            else:
                self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: / \r\n\r\n".encode())


        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
server = socketserver.ThreadingTCPServer((host,port), TCPHandler)
server.serve_forever()
