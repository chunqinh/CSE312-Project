import socketserver
import sys
import json
import os
import hashlib
import base64
import mysql.connector


class TCPHandler(socketserver.BaseRequestHandler):
    username = ''

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'database',
        'database': '312project_db'
    }

    websocket_connections = []

    def handle(self):
        recievedData = self.request.recv(2048).strip()
        print(recievedData)
        splitData = recievedData.decode().split(' ')

        # signup page
        if splitData[0] == "GET":
            if splitData[1] == "/signup":
                # print("---------------------------------------------",splitData[1])
                # if ".css" in splitData[1]:
                #     print("---------------------------------------------",splitData[1])
                #     self.send_css_response(splitData)
                # file_size_html = os.path.getsize('cse312-html/signup.html')
                file_html = open("cse312-html/signup.html", "r")
                read_html = file_html.read()
                frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_html.encode())) + "\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n" + read_html
                self.request.sendall(frontend.encode())

            # load css 
            elif ".css" in splitData[1]:

                css_path = 'cse312-html' + splitData[1]
                # file_size_css = os.path.getsize(css_path)
                file_css = open(css_path, "r")
                read_css = file_css.read()
                style = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_css.encode())) + "\r\nContent-Type: text/css;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_css
                self.request.sendall(style.encode())

            # empty homepage
            elif splitData[1] == "/homepage":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color FROM user WHERE username = %s', (TCPHandler.username,))
                info = cursor.fetchone()
                color = info[0]
                content = TCPHandler.render_template("cse312-html/homepage-empty.html",
                                                     {"username": TCPHandler.username, "username color": color})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

            # profile page
            elif splitData[1] == "/profile":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color, bio FROM user WHERE username = %s', (TCPHandler.username,))
                info = cursor.fetchone()
                bio = info[1]
                color = info[0]

                content = TCPHandler.render_template("cse312-html/profile.html", {"bio": escape_html(bio), "username color": color,
                                                                                  "username": TCPHandler.username})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

            elif splitData[1] == "/profile_edit":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color FROM user WHERE username = %s', (TCPHandler.username,))
                info = cursor.fetchone()
                color = info[0]
                content = TCPHandler.render_template("cse312-html/profile_edit.html",
                                                     {"username": TCPHandler.username, "username color": color})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

                # file_size_html = os.path.getsize('cse312-html/profile_edit.html')
                # file_html = open("cse312-html/profile_edit.html", "r")
                # read_html = file_html.read()
                # frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_html) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
                # self.request.sendall(frontend.encode())

            elif splitData[1] == "/websocket":
                key = getWebsocketKey(recievedData.decode())
                key += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11".encode()
                key = hashlib.sha1(key).hexdigest()
                key = base64.b64encode(bytes.fromhex(key))
                self.request.sendall("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                                     "Sec-WebSocket-Accept: ".encode() + key + "\r\n\r\n".encode())

                TCPHandler.websocket_connections.append(self)
                while True:
                    ws_data = self.request.recv(1024)
                    frame_data = []
                    for i in ws_data:
                        frame_data.append(bin(i)[2:])
                    mask = frame_data[2:6]
                    decoded_message = []
                    mask_bit = 0
                    for i in range(6, len(frame_data)):
                        decoded_message.append(bin(int(mask[mask_bit], 2) ^ int(frame_data[i], 2))[2:])
                        mask_bit += 1
                        if mask_bit == 4:
                            mask_bit = 0
                    message = ""
                    for i in decoded_message:
                        message += chr(int(i, 2))
                    json_message = json.loads(message)
                    ws_frame = b''
                    text_byte = 129
                    ws_frame += text_byte.to_bytes(1, "big")
                    payload_byte = '01111110'
                    ws_frame += int(payload_byte, 2).to_bytes(1, "big")
                    new_payload = bin(len(json.dumps(json_message).encode()))[2:]
                    new_payload_byte = int(new_payload, 2)
                    ws_frame += new_payload_byte.to_bytes(2, "big")
                    ws_frame += json.dumps(json_message).encode()
                    print(ws_frame)
                    for connection in TCPHandler.websocket_connections:
                        connection.request.sendall(ws_frame)


            # login page
            elif splitData[1] == "/":
                # file_size_html = os.path.getsize('cse312-html/login.html')
                file_html = open("cse312-html/login.html", "r")
                read_html = file_html.read()
                frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_html.encode())) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
                self.request.sendall(frontend.encode())




        # signup
        elif splitData[0] == "POST":
            if splitData[1] == "/signup":

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

                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s',
                               (insert_username, insert_password))
                account = cursor.fetchone()
                if insert_password != password2:
                    self.request.sendall(
                        "HTTP/1.1 403 Forbidden\r\nContent Length: 22\r\nContent-Type: text/html\r\nX-Content-Type-Options: nosniff\r\n\r\nPasswords do not match".encode())
                elif account:
                    taken = "Username or Password already exists"
                    self.request.sendall(("HTTP/1.1 403 Forbidden\r\nContent-Length: " + str(
                        len(taken)) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + taken).encode())
                else:
                    cursor.execute("INSERT INTO user(username, password) VALUES(%s,%s)",
                                   (insert_username, insert_password))
                    connection.commit()
                    cursor.close()

                    # file_size_html = os.path.getsize('cse312-html/profile.html')
                    # file_html = open("cse312-html/profile.html", "r")
                    # read_html = file_html.read()
                    # frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_html) + "\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n" + read_html
                    # self.request.sendall(frontend.encode())
                    self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: / \r\n\r\n".encode())

            # login
            elif splitData[1] == "/login":
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
                body_lst = body.split(boundary + b'\r\n')  # split using boundary
                start_username = b'"username"\r\n\r\n'
                start_password = b'"password"\r\n\r\n'
                insert_username = ''
                insert_password = ''
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
                        last_boundary = b'\r\n' + boundary + b'--'  # \r\n-- + boundary + --
                        insert_password = need_password[:size_password - len(last_boundary)].decode()

                print(insert_username)
                print(insert_password)
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s',
                               (insert_username, insert_password))
                account = cursor.fetchone()
                if not account:
                    invaild = "Wrong Password or Account doesn't exist"
                    self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + str(
                        len(invaild)) + "\r\nContent-Type: text/html;\r\nX-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
                else:
                    TCPHandler.username = insert_username
                    self.request.sendall(
                        "HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /homepage \r\n\r\n".encode())

            # profile edit post 
            elif splitData[1] == "/profile_edit":
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
                body_lst = body.split(boundary + b'\r\n')  # split using boundary
                start_bio = b'"bio"\r\n\r\n'
                start_color = b'"color"\r\n\r\n'
                new_bio = ''
                new_color = ''
                for x in body_lst:
                    if start_bio in x:
                        start_index_bio = x.find(start_bio)
                        need_bio = x[start_index_bio + len(start_bio):]
                        size_bio = len(need_bio)
                        new_bio = need_bio[:size_bio - len(b'\r\n')].decode()

                    elif start_color in x:
                        start_index_color = x.find(start_color)
                        need_color = x[start_index_color + len(start_color):]
                        size_color = len(need_color)
                        last_boundary = b'\r\n' + boundary + b'--'  # \r\n-- + boundary + --
                        new_color = need_color[:size_color - len(last_boundary)].decode()

                print(new_bio)
                print(new_color)

                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute("UPDATE user SET bio = %s,username_color = %s WHERE username = %s",
                               (new_bio, new_color, TCPHandler.username))
                connection.commit()
                cursor.close()
                self.request.sendall(
                    "HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /profile \r\n\r\n".encode())

            sys.stdout.flush()
            sys.stderr.flush()

    # def send_css_response(self, splitData):
    #     print("---------------------------------------------",splitData[1])
    #     css_path = 'cse312-html' + splitData[1]
    #     file_size_css = os.path.getsize(css_path)
    #     file_css = open(css_path, "r")
    #     read_css = file_css.read()
    #     style = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_css) + "\r\nContent-Type: text/css;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_css
    #     self.request.sendall(style.encode())

    # functions to generate html template
    def render_template(html_filename, data):
        file_html = open(html_filename, "r")
        read_html = file_html.read()

        template = read_html
        template = TCPHandler.replace_placeholders(template, data)
        # template = TCPHandler.render_loop(template, data)

        return template

    def replace_placeholders(template, data):

        replaced_template = template
        for placeholder in data.keys():
            if isinstance(data[placeholder], str):
                replaced_template = replaced_template.replace("{{" + placeholder + "}}", data[placeholder])
        return replaced_template

    def render_loop(template, data):
        if "loop_data" in data:
            loop_start_tag = "{{loop}}"
            loop_end_tag = "{{end_loop}}"

            start_index = template.find(loop_start_tag)
            end_index = template.find(loop_end_tag)

            loop_template = template[start_index + len(loop_start_tag): end_index]
            loop_data = data["loop_data"]

            loop_content = ""
            for single_piece_of_content in loop_data:
                loop_content += TCPHandler.replace_placeholders(loop_template, single_piece_of_content)

            final_content = template[:start_index] + loop_content + template[end_index + len(loop_end_tag):]

            return final_content

    # generate response 
    def generate_response(body: bytes, content_type: str = "text/plain; charset=utf-8", response_code: str = '200 OK'):
        response = b'HTTP/1.1 ' + response_code.encode()
        response += b'\r\nContent-Length: ' + str(len(body)).encode()
        response += b'\r\nContent-Type: ' + content_type.encode()
        response += b'\r\n\r\n'
        response += body
        return response


def getWebsocketKey(content):
    websocket = "Sec-WebSocket-Key: "
    index = content.find(websocket)
    beginning = index + len(websocket)
    end = beginning
    while content[end] != '\r':
        end += 1
    return content[beginning:end].encode()

def escape_html(input):
        return input.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")




if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()
