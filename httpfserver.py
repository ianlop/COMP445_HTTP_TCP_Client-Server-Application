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

def get_file_content(fileName: str):
    path = base_directory
    print(path)
    filePath = ''
    fileContent = ''
    for (dirpath, subDirs, files) in os.walk(path):
        for file in files:
            if fileName == file:
                try:
                    filePath = os.path.join(dirpath, fileName)

                    fileResult = open(filePath, 'r')
                    fileContent = fileResult.read()
                    break
                except OSError:
                    fileContent = 'HTTP ERROR 400: Could not open/read file. Try another one.'
                    break

    if not fileContent:
        fileContent = "HTTP ERROR 404: File could not be found."

    return fileContent

def create_overwrite(fileName, data, dirs =None):
    if(dirs != None and exists(base_directory + dirs)):
        os.chdir(base_directory + dirs)
        if(exists(fileName)):
            with open(fileName, "w") as f:
                f.write(data)
                f.close()
            print("File %s, has been overwritten!"%fileName)
        else:
            file = open(fileName, "w")
            file.write(data)
            file.close()
            print("File %s has been created and the user has sucessfully written on it!"%fileName)
    else:
        print("Path DNE")
        #probably shuld let user know

def run_server(host, port, dir=None):
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
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            #run thread with every client with start()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from', addr)
    try:
        while True:
            data_from_client = conn.recv(8192)
            data_from_client = data_from_client.decode("utf-8")
            if not data_from_client:
                break
            else:
                print("the server has received: \n"+data_from_client+"\n")
                client_request = data_from_client.split(" ")
                #The code above will split the client's message like so (in to an array):
                #['GET', 'http://localhost/foo', 'HTTP/1.0\r\nHost:localhost\r\n\r\n']
                print(client_request)
                request_type = client_request[0]
                request = client_request[1]
                
                if(request_type == "GET"):
                    print("I have received a GET Request")
                    split_request = request.split("localhost")
                    #the above will look like this: '[http://, /]'
                    requested_file = split_request[1]
                    if(len(requested_file) == 1 and requested_file.endswith("/")):
                        print("return the directory files found")
                        data = get_directory()
                        data = data.encode("utf-8")
                        conn.sendall(data)
                    else:
                        #when we are here this means that we are looking for a file
                        print("looking for: ",requested_file)
                        forbidden_chars = ".."
                        if(len(requested_file) == 0):
                            data = "404: Bad request Page not found!\n"
                            data = data.encode("utf-8")
                            conn.sendall(data)
                        elif(len(requested_file) > 2 ):
                            split_request = requested_file.split("/")
                            print(split_request)
                            
                            counter = 1
                            directories = ''
                            while(counter < len(split_request)-1):
                                directories += "\\" + split_request[counter]
                                counter += 1

                            print(directories)
                            file = split_request[len(split_request) - 1]
                            if('.' not in file):
                                    data = "please include a file extenstion to your request. Like '.txt' for example."
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                            else:
                                print(file)
                                
                                if(forbidden_chars in directories or forbidden_chars in file):
                                    data = "403: Forbidden\n"
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                                else:
                                    #GEORGE
                                    #The comment below should replace the old stuff we had (line 172)
                                    #data = get_file_content(directories, file) 
                                    data = get_file_content(file)
                                    data = data.encode("utf-8")
                                    conn.sendall(data)

                elif(request_type=="POST"):
                    print("I have received a POST request")
                    split_request = request.split("localhost")
                    #the above will look like this: '[http://, /]'
                    requested_file = split_request[1]
                    if(len(requested_file) == 1 and requested_file.endswith("/")):
                        data = "No file provided, please provide one at the end of the URL like so: /bar.txt"
                        data = data.encode("utf-8")
                        conn.sendall(data)
                    else:
                        #when we are here this means that we are looking for a file
                        print("looking for: ",requested_file, " to overwrite or create")
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
                                print(split_request)
                                counter = 1
                                directories = ''
                                while(counter < len(split_request)-1):
                                    directories += "\\" + split_request[counter]
                                    counter += 1

                                print(directories)
                                file = split_request[len(split_request) - 1]
                                print(file)
                                if('.' not in file):
                                    data = "please include a file extenstion to your request. Like '.txt' for example."
                                    data = data.encode("utf-8")
                                    conn.sendall(data)
                                else:
                                    split_request = data_from_client.split("\r\n\r\n")
                                    data_to_write = split_request[len(split_request) - 1]

                                    split_request = data_to_write.split("\r\n")
                                    data_to_write = split_request[0]
                                    create_overwrite(file, data_to_write, directories)
                                    data = "The necessary actions have been taken accordingly for: %s"%file
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
    parser.add_argument("--port", help="Input the server port number", type=int, default=1274, action="store")    
    parser.add_argument('-v', required=False, help="Prints debugging messages.")
    parser.add_argument('-d', required=False, help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")
    #required argument in the params above "required=" can be used to force a user 
    #to add an argument, could be useful
    args = parser.parse_args()
    run_server(args.host,args.port, args.d)
    # httpfserver.py -d "E:\unity"

if(__name__=="__main__"):
    main()