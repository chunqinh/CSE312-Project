from cgitb import handler
import socketserver
import sys
import json
import os
import hashlib
import base64
import secrets
import mysql.connector
from request import split_request, parse_headers
import bcrypt


class TCPHandler(socketserver.BaseRequestHandler):
    # username = ''
    voting_alive =False
    # option_data =[]

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'database',
        'database': '312project_db'
    }

    websocket_connections = []

    def handle(self):
        recievedData = self.request.recv(2048)
        head = {}
        # print(received_data)
        msg = recievedData.decode()
        split_header = msg.split('\r\n')
        # print(split_header)
        for x in split_header:
            if ": " in x:
                key, value = x.split(": ")
                head[key] = value
        if "Cookie" in head:
            cookie = head["Cookie"]
        print(recievedData)
        # print("createvote--------------------------------",recievedData) 
        # print("length------------------",len(recievedData))      
        [request_line, headers_as_bytes, body] = split_request(recievedData)
        headers = parse_headers(headers_as_bytes)
        body_length = len(body)
        if 'Content-Length' in headers.keys():
            Content_Length = int(headers['Content-Length'])
            # print("Content_Length------------------",Content_Length)
        
            while body_length < Content_Length:
                received_data_loop = self.request.recv(2048)
                # print("hhh_length------------------",len(received_data_loop))    
                body += received_data_loop
                recievedData += received_data_loop
                body_length += len(received_data_loop)
                # print("body_length------------------",body_length)        
                    
            # print("createvote--------------------------------",recievedData)   
        splitData = recievedData.split(b" ")

        # signup page
        if splitData[0] == b"GET":
            if splitData[1] == b"/signup":
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
            elif b".css" in splitData[1]:

                css_path = 'cse312-html' + splitData[1].decode()
                # file_size_css = os.path.getsize(css_path)
                file_css = open(css_path, "r")
                read_css = file_css.read()
                style = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_css.encode())) + "\r\nContent-Type: text/css;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_css
                self.request.sendall(style.encode())

            # load js
            elif b"functions.js" in splitData[1]:
                # file_size_css = os.path.getsize(css_path)
                file_js = open("functions.js", "r")
                read_js = file_js.read()
                style = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_js.encode())) + "\r\nContent-Type: text/css;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_js
                self.request.sendall(style.encode())

            #load image
            elif b"/public/playground_assets/" in splitData[1]:
                print(splitData[1])
                img_path = "cse312-html"+splitData[1].decode()
                print("---------------------",img_path)
                img_header = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg \r\nX-Content-Type-Options: nosniff \r\nContent-Length: "
                with open(img_path,'rb') as img_file:
                    img_content =  img_file.read()
                    b = bytearray(img_content)
                img_size = len(b)
                img_response = img_header + str(img_size) + "\r\n\r\n" 
                self.request.sendall(img_response.encode()+ img_content)

            # empty homepage
            elif splitData[1] == b"/homepage":

                print(TCPHandler.voting_alive)

                if TCPHandler.voting_alive:
                    self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /homepage_voting \r\n\r\n".encode())
                    
                else:
                    connection = mysql.connector.connect(**TCPHandler.config)
                    cursor = connection.cursor()
                    cursor.execute('SELECT username_color, username FROM user WHERE token = %s', (cookie,))
                    info = cursor.fetchone()
                    print(info)
                    print(info[0])
                    color = info[0]
                    username = info[1]
                    print("----------------color")
                    print(color)
                    content = TCPHandler.render_template("cse312-html/homepage-empty.html",
                                                            {"username": username, "username color": color})
                    response = TCPHandler.generate_response(content.encode(),
                                                            "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                            "200 OK")
                    self.request.sendall(response)

            
            elif splitData[1] == b"/homepage_voting":

                if TCPHandler.voting_alive:
                    connection = mysql.connector.connect(**TCPHandler.config)
                    cursor = connection.cursor()
                    cursor.execute('SELECT username_color, username FROM user WHERE token = %s', (cookie,))
                    info = cursor.fetchone()
                    color = info[0]
                    username = info[1]

                    cursor.execute('SELECT * FROM voting ORDER BY vote_ID DESC LIMIT 1')
                    voting_info = cursor.fetchone()
                    print(voting_info)
                    creator = voting_info[1]

                    participants =str(voting_info[6]+voting_info[8]+voting_info[10]+voting_info[12]+voting_info[14])
                    Voting_Name=voting_info[2]
                    Description=voting_info[3]
                    upload_file=voting_info[4]
                    # option_data=[]
                    
                    # option_data.append({'option_name':voting_info[5],"option_votes":str(voting_info[6])})
                    # option_data.append({'option_name':voting_info[7],"option_votes":str(voting_info[8])})
                    if voting_info[9] == "":
                        option3_display="Display:none"
                    else:
                        option3_display="Display:inline"

                    if voting_info[11] == "":
                        option4_display="Display:none"
                    else:
                        option4_display="Display:inline"

                    if voting_info[13] == "":
                        option5_display="Display:none"
                    else:
                        option5_display="Display:inline"

                    if creator == username:
                        end_vote_display ="Display:inline"
                    else:
                        end_vote_display = "Display:none"
                    
                    template_dict ={
                        "option_votes_1": str(voting_info[6]),"option_name_1":voting_info[5], 
                        "option_votes_2": str(voting_info[8]),"option_name_2":voting_info[7], 
                        "option_votes_3": str(voting_info[10]),"option_name_3":voting_info[9],  "option3_display":option3_display, 
                        "option_votes_4": str(voting_info[12]),"option_name_4":voting_info[11], "option4_display":option4_display,
                        "option_votes_5": str(voting_info[14]),"option_name_5":voting_info[13], "option5_display":option5_display,
                        "username": username, "Description":Description, "end_vote_display":end_vote_display, 
                        "username color": color, "upload_file":upload_file,"Voting_Name":Voting_Name,"participants":participants
                    }


                    content = TCPHandler.render_template("cse312-html/homepagewvoting-creator.html", template_dict)

                    response = TCPHandler.generate_response(content.encode(),
                                                            "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                            "200 OK")
                    self.request.sendall(response)
                else:
                    self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /homepage \r\n\r\n".encode())
                    

            # profile page
            elif splitData[1] == b"/profile":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color, bio, username FROM user WHERE token = %s', (cookie,))
                info = cursor.fetchone()
                username = info[2]
                bio = info[1]
                color = info[0]

                content = TCPHandler.render_template("cse312-html/profile.html",
                                                     {"bio": escape_html(bio), "username color": color,
                                                      "username": username})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

            elif splitData[1] == b"/profile_edit":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color, username FROM user WHERE token = %s', (cookie,))
                info = cursor.fetchone()
                color = info[0]
                username = info[1]
                content = TCPHandler.render_template("cse312-html/profile_edit.html",
                                                     {"username": username, "username color": color})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

            elif splitData[1] == b"/createvote":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username_color, username FROM user WHERE token = %s', (cookie,))
                info = cursor.fetchone()
                color = info[0]
                username = info[1]
                # print(username)
                content = TCPHandler.render_template("cse312-html/createvote.html",
                                                     {"username": username, "username color": color})
                response = TCPHandler.generate_response(content.encode(),
                                                        "text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff",
                                                        "200 OK")
                self.request.sendall(response)

                # file_size_html = os.path.getsize('cse312-html/profile_edit.html')
                # file_html = open("cse312-html/profile_edit.html", "r")
                # read_html = file_html.read()
                # frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(file_size_html) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
                # self.request.sendall(frontend.encode())

            elif splitData[1] == b"/websocket":
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

            elif splitData[1] == b"/online_users":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username, username_color FROM user WHERE is_online = True')
                info = cursor.fetchall()
                cursor.execute('SELECT username FROM user WHERE is_online = True AND token = %s', (cookie,))
                sender = cursor.fetchone()
                print(info)
                lis = []
                for x in info:
                    dic = {}
                    dic["sender"] = sender[0]
                    dic["receiver"] = x[0]
                    dic["color"] = x[1]
                    cursor.execute('SELECT * FROM message WHERE (sender_username = %s AND receiver_username =%s) OR (receiver_username = %s AND sender_username =%s) ORDER BY message_ID ASC ', (sender[0],x[0],sender[0],x[0]))
                    messages = cursor.fetchall()
                    print(messages)
                    list_messages =[]
                    for message in messages:
                        message_dic ={}
                        message_dic['sender'] =message[1]
                        message_dic['receiver'] =message[2]
                        message_dic['message'] =message[3]
                        list_messages.append(message_dic)
                    dic["chat_history"] = json.dumps(list_messages)
                    lis.append(dic)
                print(lis)
                response = TCPHandler.generate_response(json.dumps(lis).encode(),'application/json; charset=utf-8')
                self.request.sendall(response)

            elif b"/chat=" in splitData[1]:
                file_html = open("cse312-html/chatpage.html", "r")
                read_html = file_html.read()
                frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_html.encode())) + "\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n" + read_html
                self.request.sendall(frontend.encode())

            elif splitData[1] == b"/get-message":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM user WHERE is_online = True AND token = %s', (cookie,))
                receiver = cursor.fetchone()
                cursor.execute('SELECT * FROM message WHERE receiver_username =%s AND is_new=%s ORDER BY message_ID ASC LIMIT 1', (receiver[0],True))
                oldest_new_message = cursor.fetchall()
                if oldest_new_message:
                    print(oldest_new_message)
                    sender_info = oldest_new_message[0][1]
                    print(sender_info)
                    print(type(sender_info))
                    

                    cursor.execute('UPDATE message SET is_new = False WHERE receiver_username =%s AND sender_username = %s',
                            (receiver[0],sender_info))
                    connection.commit()
                    cursor.execute('SELECT * FROM message WHERE (sender_username = %s AND receiver_username =%s) OR (receiver_username = %s AND sender_username =%s) ORDER BY message_ID ASC ', (receiver[0],sender_info,receiver[0],sender_info))
                    messages = cursor.fetchall()

                    # lis=[]
                    dic = {}
                    dic["sender"] =sender_info
                    dic["receiver"] = receiver[0]
                    # dic["color"] = x[1]
                    # cursor.execute('SELECT * FROM message WHERE (sender_username = %s AND receiver_username =%s) OR (receiver_username = %s AND sender_username =%s) ORDER BY message_ID ASC LIMIT 1', (TCPHandler.username,x[0],TCPHandler.username,x[0]))
                    # messages = cursor.fetchall()
                    # print(messages)
                    list_messages =[]
                    for message in messages:
                        message_dic ={}
                        message_dic['sender'] =message[1]
                        message_dic['receiver'] =message[2]
                        message_dic['message'] =message[3]
                        list_messages.append(message_dic)
                    dic["chat_history"] = json.dumps(list_messages)
                    print("__________________________new message")

                    response = TCPHandler.generate_response(json.dumps(dic).encode(),'application/json; charset=utf-8')
                    self.request.sendall(response)
                else:
                    print("no new message --------------------")
                    response = TCPHandler.generate_response(json.dumps({'sender':'','receiver':'','chat_history':''}).encode(),'application/json; charset=utf-8')
                    self.request.sendall(response)
            
            # logout
            elif splitData[1] == b"/logout":
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('UPDATE user SET is_online = FALSE WHERE token = %s',(cookie,))
                connection.commit()
                cursor.close()
                self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nSet-Cookie: id=none; Max-Age=-1\r\nLocation: / \r\n\r\n".encode())

            # login page
            elif splitData[1] == b"/":

                print(recievedData)

                # file_size_html = os.path.getsize('cse312-html/login.html')
                file_html = open("cse312-html/login.html", "r")
                read_html = file_html.read()
                frontend = "HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(read_html.encode())) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + read_html
                self.request.sendall(frontend.encode())


                

        # signup
        elif splitData[0] == b"POST":
            if splitData[1] == b"/signup":
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
                        insert_username = escape_html(insert_username)

                    elif start_password in x:
                        start_index_password = x.find(start_password)
                        need_password = x[start_index_password + len(start_password):]
                        size_password = len(need_password)
                        insert_password = need_password[:size_password - len(b'\r\n')].decode()
                        insert_password = escape_html(insert_password)

                    elif start_password2 in x:
                        start_index_password2 = x.find(start_password2)
                        need_password2 = x[start_index_password2 + len(start_password2):]
                        size_password2 = len(need_password2)
                        last_boundary = b'\r\n' + boundary + b'--\r\n'  # \r\n-- + boundary + --
                        password2 = need_password2[:size_password2 - len(last_boundary)].decode()
                        password2 = escape_html(password2)


                print(insert_username)
                print(insert_password)
                print(password2)
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                salt = bcrypt.gensalt()
                hash_password = bcrypt.hashpw(insert_password.encode(), salt)
                cursor.execute('SELECT * FROM user WHERE username = %s',
                               (insert_username,))
                account = cursor.fetchone()
                if insert_password != password2:
                    print("你好")
                    self.request.sendall(
                        "HTTP/1.1 403 Forbidden\r\nContent Length: 22\r\nContent-Type: text/html\r\nX-Content-Type-Options: nosniff\r\n\r\nPasswords do not match".encode())
                # elif '&' or '/' in insert_username:
                #     self.request.sendall(
                #         "HTTP/1.1 403 Forbidden\r\nContent Length: 45\r\nContent-Type: text/html\r\nX-Content-Type-Options: nosniff\r\n\r\nYour username cannot contain html characters.".encode())
            
                elif account:
                    taken = "Username already exists"
                    self.request.sendall(("HTTP/1.1 403 Forbidden\r\nContent-Length: " + str(
                        len(taken)) + "\r\nContent-Type: text/html;\r\n X-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + taken).encode())
                else:
                    cursor.execute("INSERT INTO user(username, password) VALUES(%s,%s)",
                                   (insert_username, hash_password))
                    connection.commit()
                    cursor.close()
                    self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: / \r\n\r\n".encode())

            # login
            elif splitData[1] == b"/login":
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
                        insert_username = escape_html(insert_username)

                    elif start_password in x:
                        start_index_password = x.find(start_password)
                        need_password = x[start_index_password + len(start_password):]
                        size_password = len(need_password)
                        last_boundary = b'\r\n' + boundary + b'--\r\n'  # \r\n-- + boundary + --
                        insert_password = need_password[:size_password - len(last_boundary)].decode()
                        insert_password= escape_html(insert_password)

                print(insert_username)
                print(insert_password)
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute('SELECT password FROM user WHERE username = %s',
                               (insert_username,))
                account = cursor.fetchone()
                if account:
                    print(account[0])
                    if bcrypt.checkpw(insert_password.encode(), account[0].encode()):
                        print("mtach")
                        auth_token = secrets.token_urlsafe()
                        salt = bcrypt.gensalt()
                        hash_token = b'id=' + bcrypt.hashpw(auth_token.encode(), salt)
                        print(hash_token)
                        cursor.execute('UPDATE user SET token = %s, is_online = True WHERE username = %s',
                        (hash_token.decode(), insert_username,))
                        connection.commit()
                        self.request.sendall(("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nSet-Cookie: "+ hash_token.decode() +"; Max-Age=3600; HttpOnly\r\nLocation: /homepage \r\n\r\n").encode())
                    else:
                        print("not match")
                        invaild = "Wrong Password or Account doesn't exist"
                        self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + str(
                            len(invaild)) + "\r\nContent-Type: text/html;\r\nX-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
                else:
                    invaild = "Wrong Password or Account doesn't exist"
                    self.request.sendall(("HTTP/1.1 404 Not Found\r\nContent-Length: " + str(
                        len(invaild)) + "\r\nContent-Type: text/html;\r\nX-Content-Type-Options: nosniff\r\n charset=utf-8\r\n\r\n" + invaild).encode())
                

            # profile edit post 
            elif splitData[1] == b"/profile_edit":
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
                        new_bio = escape_html(new_bio)

                    elif start_color in x:
                        start_index_color = x.find(start_color)
                        need_color = x[start_index_color + len(start_color):]
                        size_color = len(need_color)
                        last_boundary = b'\r\n' + boundary + b'--'  # \r\n-- + boundary + --
                        new_color = need_color[:size_color - len(last_boundary)].decode()
                        

                print(new_bio)
                print(new_color)
                print(cookie)
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                cursor.execute("UPDATE user SET bio = %s,username_color = %s WHERE token = %s",
                               (new_bio, new_color, cookie,))
                connection.commit()
                cursor.close()
                self.request.sendall(
                    "HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /profile \r\n\r\n".encode())

            elif splitData[1] == b"/direct-message":
                # ("print ___________DM")
                [request_line, headers_as_bytes, body] = split_request(recievedData)
                json_string = json.loads(body)
                print(json_string)
                # if json_string['receiver'] == TCPHandler.username:
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()
                # cursor.execute('SELECT sender_username FROM message WHERE receiver_username = %s',
                #            (TCPHandler.username,))
                # message = cursor.fetchone()
                # if message:
                #     cursor.execute("UPDATE message SET sender_username = %s, content =%s WHERE receiver_username = %s",
                #                 (json_string['sender'], json_string['message'], TCPHandler.username))
                #     connection.commit()
                #     cursor.close()
                # else:
                cursor.execute("INSERT INTO message(sender_username, content, receiver_username,is_new) VALUES(%s, %s, %s,True)",
                            (json_string['sender'],json_string['message'], json_string['receiver']))
                connection.commit()

                cursor.execute('SELECT * FROM message WHERE sender_username = %s',
                           (json_string['sender'],))
                message = cursor.fetchall()
                print(message)
                cursor.close()
                response = TCPHandler.generate_response(json.dumps({'result':True}).encode(),'application/json; charset=utf-8')
                self.request.sendall(response)
                

                # else:
                #     response = TCPHandler.generate_response(json.dumps({'result':False}).encode(),'application/json; charset=utf-8')
                #     self.request.sendall(response)
                
                

            elif splitData[1] == b"/createvote":      
              
                boundary = find_boundary(recievedData)
                form_data = recievedData.split(boundary)
                image = find_image(form_data[1])
                if image != b"":
                    file_name = store_image(image)
                else:
                    file_name = 'vote-200h.png'
                print(file_name)

                vote_name = getData(form_data[2].decode())
                vote_name = escape_html(vote_name)
                description = getData(form_data[3].decode())
                description = escape_html(description)
                option_1 = getData(form_data[4].decode())
                option_1= escape_html(option_1)
                option_2 = getData(form_data[5].decode())
                option_2= escape_html(option_2)
                option_3 = getData(form_data[6].decode())
                option_3= escape_html(option_3)
                option_4 = getData(form_data[7].decode())
                option_4= escape_html(option_4)
                print("option_4----------------------------------------",option_4)
                option_5 = getData(form_data[8].decode())
                option_5= escape_html(option_5)
                print("option_5----------------------------------------",option_5)
                connection = mysql.connector.connect(**TCPHandler.config)
                cursor = connection.cursor()

                cursor.execute('SELECT username FROM user WHERE token = %s', (cookie,))
                creator = cursor.fetchone()
                # print(creator[0])
                # print("hello")
                cursor.execute("INSERT INTO voting(creator_username, vote_name, vote_description, photo, option_one_name, option_two_name, option_three_name, option_four_name, option_five_name) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (creator[0],vote_name, description, file_name ,option_1, option_2, option_3, option_4, option_5 ))
                connection.commit()


                cursor.execute("SELECT * FROM voting")
                voting = cursor.fetchall()
                print(voting)

                connection.commit()
                cursor.close()

                TCPHandler.voting_alive=True
                self.request.sendall("HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: /homepage_voting \r\n\r\n".encode())



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
        if "loop_data" in data:
            print("----------loop")
            template = TCPHandler.render_loop(template, data)

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


def getBoundary(content):
    boundary = "boundary="
    index = content.find(boundary)
    beginning = index + len(boundary)
    end = beginning
    while content[end] != '\r':
        end += 1
    return content[beginning:end].encode()

def find_boundary(request):
    [request_line, headers_as_bytes, body] = split_request(request)
    header = parse_headers(headers_as_bytes)
    
    print(header['Content-Type'])
    Content_Type = header['Content-Type']
    boundary_len = len('boundary=')
    boundary = Content_Type[Content_Type.find('boundary=')+boundary_len:]
    boundary = "--"+ boundary
    return boundary.encode()


def getData(content):
    doublecrlf = "\r\n\r\n"
    index = content.find(doublecrlf)
    beginning = index + len(doublecrlf)
    end = beginning
    while content[end] != '\r':
        end += 1
    return content[beginning:end]

def parse_body(body, boundary):
    request_split = body.split(boundary)
    request_split = request_split[1:len(request_split)]
    return(request_split)

new_line = b'\r\n'
blank_line_boundary = b'\r\n\r\n' 

def find_image(parsed_body):
    image = parsed_body[parsed_body.find(blank_line_boundary)+len(blank_line_boundary):len(parsed_body)-len(new_line)]
    return image

def store_image(image):
    list = os.listdir('cse312-html/public/playground_assets') # dir is your directory path
    number_files = len(list)+1
    print(number_files)
    file_name = "image" + str(number_files)+".jpg"
    save_path = 'cse312-html/public/playground_assets'
    completeName = os.path.join(save_path, file_name)
    with open(completeName , "wb") as output_file:
        output_file.write(image)
    return file_name

def escape_html(input):
    return input.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace("'","&#39;").replace('"',"&quot;").replace("/","&#47;")



if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    server.serve_forever()