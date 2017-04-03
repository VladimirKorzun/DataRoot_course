#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
import sys


def list_directory(dir, str=""):
        files = os.listdir("./" + dir)
        response = "HTTP/1.1 200 OK\n Content-Type: text/html\n\n" \
                   "<html>" \
                   "<head>" \
                   "<meta charset='utf-8'>" \
                   "</head>" \
                   "<body>" \
                   "<h2>Directory listing for: " + dir + "</h2>" \
                   "<br>" + str +\
                   "<hr>" \
                   "<ul>"
        #print(files)
        if "index.html" in files:
            return "index.html"

        for file in files:
                if dir == '/':
                    response += "<li><a href=\"" + dir +  file +"\">" + file + "</a></li>\n<br>"
                else:
                    response += "<li><a href=\"" + dir + "/" + file + "\">" + file + "</a></li>\n<br>"

        response += "</ul>" \
                    "<hr> " \
                    "<br> " \
                    "</body>" \
                    "</html>"
        return response

def read_file(file_requested):
    file_handler = open(file_requested[1:], 'rb')
    response_content = file_handler.read()  # read file content
    file_handler.close()
    response_headers = 'HTTP/1.1 200 OK\n Content-Type: text/html\n\n'
    server_response = response_headers.encode()
    server_response += response_content
    return server_response


def start_server():
    port = sys.argv[1]
    #print(host)
    serversocket = socket.socket()
    try:
        serversocket.bind(('localhost', int(port)))
        print("Starting server on port: " + port)
    except:
        print("Invalid port number. Try again.")
        return -1

    while True:
        serversocket.listen(1)
        connection, address = serversocket.accept()
        data = connection.recv(1024)

        string = bytes.decode(data)

        file_requested = string.split(' ')

        try:
            file_requested = file_requested[1]
            #print(file_requested)
        except:
            connection.close()
            continue

        #print("FILE" + file_requested)

        if os.path.isdir("./" + file_requested):
            response = list_directory(file_requested)
            if response == "index.html":
                if file_requested == "/":
                    file_requested += "index.html"
                else:
                    file_requested += "/index.html"
                server_response = read_file(file_requested)
                connection.send(server_response)
            else:
                connection.send(response.encode('utf-8'))
        else:

            try:
                #print("FILE TO OPEN" + file)
                server_response = read_file(file_requested)
                connection.send(server_response)
            except:
                str = "File not exist. " \
                      "You've been returned to start directory."
                response = list_directory("/", str)
                connection.send(response.encode('utf-8'))

        connection.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        start_server()
    else:
        print("Invalid number of arguments")