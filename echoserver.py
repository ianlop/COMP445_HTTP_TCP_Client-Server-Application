from email import message
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
            line = bytes(data).decode("utf-8")
            print('RECEIVED FROM CLIENT:',line)
            message = line
            if ('help' in line):
                message = 'The commands are:\n   get executes a HTTP GET request and prints the response.\n    post executes a HTTP POST request and prints the response.\n    help prints this screen.\n\nUse "httpc help [command]" for more information about a command'        
                data = message.encode("utf-8")
            elif not data:
                print('SOMETHING WRONG')
                break
            conn.sendall(data)
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
