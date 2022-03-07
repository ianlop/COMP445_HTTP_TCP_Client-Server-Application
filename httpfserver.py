import socket
import threading
import argparse

def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from', addr)
    try:
        while True:
            data = conn.recv(1024)
            data = data.decode("utf-8")
            print(type(data))
            if not data:
                break
            if data == 'help':
                data = 'I dont care'
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
    #header option examples: (THEY MUST BE SURROUNDED BY QUOTES)
        "Accept-Language: en us,en;q=0.5"
        "Accept-Encoding: gzip,deflate"
        "Content-Type:application/json"
    
    httpclient.py --get "http://httpbin.org/headers" -v -H "Accept-Language: en us,en;q=0.5" -H "Content-Type: application/json; charset=utf-8"
    httpclient.py --post "http://httpbin.org/post" -v -d "Assignment: 1" -H "Content-Type: application/json"
    httpclient.py --post "http://httpbin.org/post" -v -f sample.txt -H "Content-Type: application/json"
    httpclient.py --post "http://httpbin.org/post" -v
    httpclient.py --HELP get
    //////////////////////////////////////////////
    '''

    args = parser.parse_args()
    run_server(args.host,args.port)


if(__name__=="__main__"):
    main()