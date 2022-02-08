'''
Ian L.
George M.

Task 1.)
this python file will contain the library for our HTTP client.
This library will support these features:
a.) GET operation - Retreives data from the server
b.) POST operation - Submits data to the server
c.) Query parameters
d.) Request headers
e.) Body of the request

Task 2.)
(Perhaps on another py file?)
Implementation of a cURL command line that does basic functionalities that
are related to the HTTP protocol

CLI notes:
An argument is a single part of a command line, delimited by blanks.

An option is a particular type of argument (or a part of an argument) that can modify the behavior of the command line.

A parameter is a particular type of argument that provides additional information to a single option or command.

'''
import socket
import argparse
import sys
from xmlrpc.client import Boolean

#verbose code we might use
'''
https://realpython.com/command-line-interfaces-python-argparse/
ctrl-f VerboseStore in the link above to learn more
this below is only a sample
'''
class VerboseStore(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(VerboseStore, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Here I am, setting the ' \
              'values %r for the %r option...' % (values, option_string))
        setattr(namespace, self.dest, values)


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
        line = 'The commands are:\n\t get executes a HTTP GET request and prints the response.\n    post executes a HTTP POST request and prints the response.\n    help prints this screen.\n\nUse "httpc help [command]" for more information about a command'
    response = line.encode("utf-8")
    return response   


def print_help_for_post_or_get(argument):
    if(argument == 'get' or argument == 'GET'):
        print('httpc help get'\
                '\nusage: httpc get [-v] [-h key:value] URL\n' \
                'Get executes a HTTP GET request for a given URL.\n' \
                '-v\t\tPrints the detail of the response such as protocol, status, and headers.\n'\
                "-h key:value\tAssociates headers to HTTP Request with the format 'key:value'.")
    elif(argument =='post' or argument=='POST'):
        print('httpc help post'\
                '\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n' \
                'Post executes a HTTP POST request for a given URL with inline data or from file.\n' \
                '-v\t\tPrints the detail of the response such as protocol, status, and headers.\n'\
                '-h key:value\t\tAssociates headers to HTTP Request with the format\n'\
                '-d string\t\tAssociates headers to HTTP Request with the format\n'\
                '-f file\t\tAssociates the content of a file to the body HTTP POST request.\n'\
                "Either [-d] or [-f] can be used but not both.")

#Usage: python echoclient.py --host host --port port
#parser is container to hold our arguments
parser = argparse.ArgumentParser(prog='httpc',
                                description='httpc is a curl-like application but supports HTTP protocol only.',
                                usage="\n\thttpclient.py command [arguments]", allow_abbrev=False,
                                epilog='Use "httpclient.py help [command]" for more information about a command.')
#going to have to use -H f
#positional arguments
parser.add_argument("--host", help="Input the server host ip", default="localhost", action="store")
parser.add_argument("--port", help="Input the server port number", type=int, default=8007, action="store")
parser.add_argument("--get", help="executes a HTTP GET request and prints the response.", type=str)

#parser.add_argument("post", help="executes a HTTP POST request and prints the response.", default=False)
#store_true sends a true value when sent once!
parser.add_argument("--HELP",help="executes a HTTP GET request and prints the response."
                         , type=str, choices=['GET', 'get', 'POST', 'post'], required=False)
#optional arguments
#this one below is -h for the headers key:value requirement
'''
3. To pass the headers value to your HTTP operation, you could use -h option. The latter means 
setting the header of the request in the format "key: value." Notice that; you can have 
multiple headers by having the -h option before each header parameter.
WE WILL USE -H TO NOT CONFLICT WITH -h the default help feature argparse uses!!!!
'''
parser.add_argument('-H', required=False)
parser.add_argument("-v", "--verbose", help="Turns on verbose mode for more details", 
                    action=VerboseStore,required=False)
#required argument in the params above "required=" can be used to force a user 
#to add an argument, could be useful for positional argument

#arguments that are not necessary are called optional args and use a singular -
#as u see above on everything i have. Positionals are everything that dont have a singular -

'''
After you execute .parse_args(), what you get is a Namespace object that contains a simple 
property for each input argument received from the command line.
'''
args = parser.parse_args()
#print_help_for_post_or_get(args.HELP)
run_client(args.host, args.port)

#If you wish to call a function with an option then you must create a subclass of argparse.Action
#You must supply a__call__method.

#Todo 1-change verbose mutually exlusive and obser [v|d] thing from youtube video and pdf
# 2 - pass in arguments directly to parameters 