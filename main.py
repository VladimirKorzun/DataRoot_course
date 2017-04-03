#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
import sys


def list_directory(current_dir, new_dir, str=""):
        dir = current_dir + new_dir
        files = os.listdir(current_dir + new_dir)
        dir = dir.split(os.getcwd())
        response = "HTTP/1.1 200 OK\n Content-Type: text/html\n\n" \
                   "<html>" \
                   "<head>" \
                   "<meta charset='utf-8'>" \
                   "</head>" \
                   "<body>" \
                   "<h2>Directory listing for: " + dir[1] + "</h2> " \
                   "<br>" + str + \
                   "<ul>"
        #print(files)
        if "index.html" in files:
            return "index.html"

        for file in files:
                response += "<li><a href=\"" + file + "\">" + file + "</a></li>\n<br>"

        response += "</ul>" \
                    "<hr> " \
                    "<br> " \
                    "</body>" \
                    "</html>"
        #print(current_dir + dir)
        return response

def read_file(file_requested):
    file_handler = open(file_requested[2:], 'rb')
    response_content = file_handler.read()  # read file content
    file_handler.close()
    response_headers = 'HTTP/1.1 200 OK\n Content-Type: text/html\n\n'
    server_response = response_headers.encode()
    server_response += response_content
    return server_response


def start_server():
    host = sys.argv[1]
    #print(host)
    serversocket = socket.socket()
    serversocket.bind(('localhost', int(host)))

    dir = os.getcwd()

    root = ""

    while True:
        serversocket.listen(1)
        connection, address = serversocket.accept()
        data = connection.recv(1024)

        string = bytes.decode(data)

        file_requested = string.split(' ')
        #print(file_requested)
        try:
            file_requested = file_requested[1]
            file = file_requested
        except:
            connection.close()
            continue

        #print("FILE" + file_requested)



        if os.path.isdir(dir + file):
            response = list_directory(dir, file)
            if response == "index.html":
                dir += file
                root += file
                file_requested = root + "/index.html"
                server_response = read_file(file_requested)
                connection.send(server_response)
            else:
                dir += file
                root += file
                connection.send(response.encode('utf-8'))
        else:
            file_requested = root + file
            #print("FILE TO OPEN" + file_requested)
            try:
                server_response = read_file(file_requested)
                connection.send(server_response)
            except:
                str = "It's seems like you try to get failed gateway to folder or file." \
                      " You've been returned to start directory"
                dir = os.getcwd()
                root = "/"
                response = list_directory(dir, "/", str)
                connection.send(response.encode('utf-8'))
                connection.close()
                continue


        connection.close()


if __name__ == "__main__":
    start_server()

