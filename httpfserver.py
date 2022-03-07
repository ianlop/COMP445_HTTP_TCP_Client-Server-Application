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
import socket
import threading
import argparse
import os

global directory

def run_server(host, port, dir=None):
    global directory
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(dir == None):
        #use current directory as default
        directory = os.getcwd()
        #print(directory)
    else:
        #use specified directory
        directory = dir

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
            data = conn.recv(8192)
            data = data.decode("utf-8")
            print(type(data))
            print(data+"\n")
            if not data:
                break
            data = 'message from httpfserver.py! testing 1..2..3'
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
    parser.add_argument('-v', required=False, help="Prints debugging messages.")
    parser.add_argument('-d', required=False, help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")
    #required argument in the params above "required=" can be used to force a user 
    #to add an argument, could be useful
    '''
    After you execute .parse_args(), what you get is a Namespace object that contains a simple 
    property for each input argument received from the command line.
    //////////////////////////////////////////////
    Example usages in cmd prompt:

    httpfserver.py --port 1234
    //////////////////////////////////////////////
    '''
    args = parser.parse_args()
    run_server(args.host,args.port, args.d)

if(__name__=="__main__"):
    main()