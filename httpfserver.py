'''
Ian L.
George M.

Task 1.)
Develop an HTTP Server Library
We are required to implement only a subset of the HTTP specifications. In essence, the
library should include the features that can handle the requests from the httpc app of
Assignment #1.

Task 2.)
Build a File Server Application Using Your HTTP Library.
'''
from asyncio.windows_events import NULL
from fileinput import filename
from genericpath import exists
import socket
import threading
import argparse
import os
from typing import final

global base_directory
global port_number

def get_directory():
    path = base_directory
    max_character_name = 12
    dir_content = os.listdir(path)
    content = ''
    for item in dir_content:
        if os.path.isdir(os.path.join(path, item)):
            content += 'DIR: %s\r\n'%(item)
        elif os.path.isfile(os.path.join(path, item)):
            split_text = item.split('.')
            print(split_text)
            split_text[0] = split_text[0].ljust(max_character_name)
            print(split_text[0])
            content += 'FILE: %s TYPE: %s\r\n'%(split_text[0], split_text[1])

    if not content:
        content = "HTTP ERROR 404: No files or directories found."

    return content

def get_file_content(fileName: str, dirs = None):
    fileContent = ''
    if dirs == None:
        dirs = '\\'
    print(str(base_directory + dirs))
    if exists(base_directory + dirs):
        os.chdir(base_directory + dirs)
        try:
            with open(fileName, 'r') as f:
                fileContent = f.read()
                f.close()
            if not fileContent:
                fileContent= 'WARNING: File has no content.'
        except OSError:
            fileContent = 'HTTP ERROR 400: Could not open/read file. Try another one.'
    else:
        fileContent = "HTTP ERROR 404: File could not be found."

    return fileContent

def create_overwrite(fileName, data, dirs =None):
    if(dirs != None and exists(base_directory + dirs)):
        os.chdir(base_directory + dirs)
        if(exists(fileName)):
            with open(fileName, "w") as f:
                f.write(data)
                f.close()
            return "File %s, has been overwritten!"%fileName
        else:
            file = open(fileName, "w")
            file.write(data)
            file.close()
            return "File %s has been created and the user has sucessfully written on it!"%fileName
    else:
        return "HTTP ERROR 404: Path could not be found."

def run_server(host, port, dir=None, debugger = False):
    global base_directory
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(dir == None):
        #use current directory as default
        base_directory = os.getcwd() +"\Working"
        os.chdir(base_directory)
    else:
        #use specified directory
        base_directory = dir
        os.chdir(base_directory)
    try:
        listener.bind((host, port))
        #5 is the number of connections that socket.listen() will put in queue at most
        #before rejecting the rest of the incoming connections
        listener.listen(5)
        if(debugger):
            print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            #run thread with every client with start()
            threading.Thread(target=handle_client, args=(conn, addr, debugger)).start()
    finally:
        listener.close()


def handle_client(conn, addr, debugger):
    if(debugger):
        print('New client from', addr)
    try:
        while True:
            data_from_client = conn.recv(8192)
            data_from_client = data_from_client.decode("utf-8")
            if not data_from_client:
                break
            else:
                if(debugger):
                    print("the server has received this message from the client: \n"+data_from_client+"\n")
                client_request = data_from_client.split(" ")
                #The code above will split the client's message like so (in to an array):
                #['GET', 'http://localhost/foo', 'HTTP/1.0\r\nHost:localhost\r\n\r\n']
                request_type = client_request[0]
                request = client_request[1]
                
                if(request_type == "GET"):
                    if(debugger):
                        print("I have received a GET Request\n")
                    split_request = request.split("localhost")
                    #the above will look like this: '[http://, /]'
                    requested_file = split_request[1]
                    if(len(requested_file) == 1 and requested_file.endswith("/")):
                        if(debugger):
                            print("returning the directory files found\n")
                        data = get_directory()
                        data = data.encode("utf-8")
                        conn.sendall(data)
                    else:
                        #when we are here this means that we are looking for a file
                        if(debugger):
                            print("looking for: ",requested_file)
                        forbidden_chars = ".."
                        if(len(requested_file) == 0):
                            data = "404: Bad request Page not found!\n"
                            data = data.encode("utf-8")
                            conn.sendall(data)
                        elif(len(requested_file) > 2 ):
                            split_request = requested_file.split("/")
                            counter = 1
                            directories = ''
                            while(counter < len(split_request)-1):
                                directories += "\\" + split_request[counter]
                                counter += 1

                            file = split_request[len(split_request) - 1]
                            if('.' not in file):
                                    data = "HTTP ERROR 404: Please include a file extenstion to your request. Like '.txt' for example."
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                            else:   
                                if(forbidden_chars in directories or forbidden_chars in file):
                                    data = "403: Forbidden\n"
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                                else:
                                    #GEORGE
                                    #The comment below should replace the old stuff we had (line 171)
                                    #data = get_file_content(directories, file) 
                                    data = get_file_content(file, directories)
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                elif(request_type=="POST"):
                    if(debugger):
                        print("I have received a POST request\n")
                    split_request = request.split("localhost")
                    requested_file = split_request[1]
                    if(len(requested_file) == 1 and requested_file.endswith("/")):
                        data = "No file provided, please provide one at the end of the URL like so: /bar.txt"
                        data = data.encode("utf-8")
                        conn.sendall(data)
                    else:
                        #when we are here this means that we are looking for a file
                        if(debugger):
                            print("looking for: ",requested_file, " to overwrite or create\n")
                        forbidden_chars = ".."
                        if(len(requested_file) == 0):
                            data = "404: Bad request Page not found!\n"
                            data = data.encode("utf-8")
                            conn.sendall(data)
                        elif(len(requested_file) > 2 ):
                            split_request = requested_file.split("/")
                            #split_request needs to look exactly like this [/, fileName]
                            #max indices is 2
                            if(forbidden_chars in requested_file):
                                data = "403: Forbidden\n"
                                data = data.encode("utf-8")
                                conn.sendall(data)
                            else:
                                counter = 1
                                directories = ''
                                while(counter < len(split_request)-1):
                                    directories += "\\" + split_request[counter]
                                    counter += 1

                                file = split_request[len(split_request) - 1]
                                if('.' not in file):
                                    data = "please include a file extenstion to your request. Like '.txt' for example."
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                                else:
                                    split_request = data_from_client.split("\r\n\r\n")
                                    data_to_write = split_request[len(split_request) - 1]
                                    split_request = data_to_write.split("\r\n")
                                    #data from user that they want to write the file with
                                    data_to_write = split_request[0]
                                    
                                    data = create_overwrite(file, data_to_write, directories)
                                    data = data.encode("utf-8")
                                    conn.sendall(data) 
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(prog='httpfs',
                                    description='httpfs is a simple HTTP server application and used with off- the-shelf HTTP clients' 
                                                    +'(including httpc client, the result of Lab Assignment #1). Precisely, it is'
                                                    + 'aimed to build a simple remote file manager on top of the HTTP protocol in the server side.',
                                    usage="\n\thttpserver.py command [arguments]", allow_abbrev=False)
    '''
    Syntactically, the difference between positional and optional arguments is 
    that optional arguments start with - or --, while positional arguments do not.
    We will be using optional for the most part
    '''
    #optional arguments
    parser.add_argument("--host", help="Input the server host ip", default="localhost", action="store")
    parser.add_argument("--port", help="Input the server port number", type=int, default=1234, action="store")    
    parser.add_argument('-v', required=False, help="Prints debugging messages.",action="store_true")
    parser.add_argument('-d', required=False, help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")
    #required argument in the params above "required=" can be used to force a user 
    #to add an argument, could be useful
    args = parser.parse_args()
    run_server(args.host,args.port, args.d, args.v)
    # httpfserver.py -d "E:\unity"

if(__name__=="__main__"):
    main()