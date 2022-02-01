'''
Ian L.
George M.

Task 1.)
this python file will contain the library for our HTTP client.
This library will support these features:
a.) GET operation
b.) POST operation
c.) Query parameters
d.) Request headers
e.) Body of the request

Task 2.)
(Perhaps on another py file?)
Implementation of a cURL command line that does basic functionalities that
are related to the HTTP protocol
'''
import socket
import argparse
import sys


def run_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type 'help' to get assistance. Press ENTER and then CTRL+C to quit.")
        while True:
            line = input()
            request = line.encode("utf-8")
            conn.sendall(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(1024)
            message = response.decode("utf-8")
            print(message)
    finally:
        conn.close()


def handle_request(response: bytes) -> bytes:
    line = 'default'
    decoded = response.decode("utf-8")
    if ('help' in decoded):
        line = 'The commands are:\n   get executes a HTTP GET request and prints the response.\n    post executes a HTTP POST request and prints the response.\n    help prints this screen.\n\nUse "httpc help [command]" for more information about a command'
    response = line.encode("utf-8")
    return response   

# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8007)
#parser.add_argument("--get", help="executes a HTTP GET request and prints the response.", type=str, default="default")
args = parser.parse_args()
run_client(args.host, args.port)
