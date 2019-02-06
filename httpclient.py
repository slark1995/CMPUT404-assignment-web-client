#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        ParseResult = urllib.parse.urlparse(url)
        host = ParseResult.hostname
        port = ParseResult.port

        if port == None:
            port = 80

        return host, port
    

    def get_path(self,url):
        ParseResult = urllib.parse.urlparse(url)
        if ParseResult.path == '':
            return "/"
       	else:
            return ParseResult.path



    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):

        data_split = re.split(r' ',data)
        code = data_split[1]

        #m = re.search('(?<=Error code: )\d\d\d', data)
        #code = m.group(0)
        return int(code)

    def get_headers(self,data):
        data_split = re.split(r'\r\n\r\n',data)
        headers = data_split[0]
        return body        


    def get_body(self, data):
        data_split = re.split(r'\r\n\r\n',data)
        body = data_split[1]
        return body

    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')



    def GET(self, url, args=None):
        print("function get: ", url)
        host,port = self.get_host_port(url)
        self.connect(host,port)
        path = self.get_path(url)
        http_request = "GET " + path + " HTTP/1.1\r\nHost: " + str(host) + "\r\nConnection: close\r\n\r\n"
        #print("!!!!!!!!http_request:",http_request)
        self.sendall(http_request)
        http_response = self.recvall(self.socket)
        print("=========================http_response===============:\r\n" + http_response + "=============http_response_ends=====================")
        code = self.get_code(http_response)
        body = self.get_body(http_response)
        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        host,port = self.get_host_port(url)
        self.connect(host,port)
        path = self.get_path(url)
        if args != None:
        	content_body = urllib.parse.urlencode(args)
        	content_length = len(content_body)
        	http_request = "POST " + path + " HTTP/1.1\r\nHost: " + str(host) + "\r\nContent-Type: application/x-www-form-urlencoded\r\n" + "Content-Length: "+ str(content_length)+ "\r\n" +"Connection: close\r\n\r\n" + content_body
        else:
        	content_body = None
        	content_length = 0
        	http_request = "POST " + path + " HTTP/1.1\r\nHost: " + str(host) + "\r\nContent-Type: application/x-www-form-urlencoded\r\n" + "Content-Length: "+ str(content_length)+ "\r\n" +"Connection: close\r\n\r\n"

        self.sendall(http_request)
        http_response = self.recvall(self.socket)
        print("=========================http_response===============:\r\n" + http_response + "=============http_response_ends=====================")
        code = self.get_code(http_response)
        body = self.get_body(http_response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
