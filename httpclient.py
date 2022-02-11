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
Implementation of a cURL command line that does basic functionalities that
are related to the HTTP protocol
'''
import socket
import argparse
from typing import Text
from xmlrpc.client import Boolean
from urllib.parse import urlparse

class PayloadRequest:
    def __init__(self, p_args, p_headers, p_url, p_data, p_files, p_form, p_json):
        args = p_args
        headers = p_headers
        url = p_url
        data = p_data
        files = p_files
        form = p_form
        json = p_json

    #def getRequest(self, url_link : Text | bytes):
     #   url = url_link



def get_request(url, port, verbose=False):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlparser = urlparse(url)
    #host is 'httpbin.org', a "part" of the url variable/ full url
    host = urlparser.hostname
    #print(host)
    # this below does the same as above
    #print(urlparser.path)
    #prints request type i think
    #print(urlparser.query)
    #ip address of the host
    #print(socket.gethostbyname(host))
    try:
        #host: 'www.httpbin.org'
        #url: http://httpbin.org/get?course=networking&assignment=1 
        client.connect((host, port))

        request = "GET " + url + " HTTP/1.0\r\n" \
        "Host:%s\r\n\r\n" % host
        request = request.encode("utf-8")
        
        client.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = client.recv(1024)
        full_response = response.decode("utf-8")
        response_details, response_data = full_response.split("\r\n\r\n")
        #show details with verbose
        if(verbose):
            print(response_details, "\n")
        print(response_data)

    finally:
        client.close()

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


def main():
    #Usage: python echoclient.py --host host --port port
    #parser is container to hold our arguments
    parser = argparse.ArgumentParser(prog='httpc',
                                    description='httpc is a curl-like application but supports HTTP protocol only.',
                                    usage="\n\thttpclient.py command [arguments]", allow_abbrev=False,
                                    epilog='Use "httpclient.py help [command]" for more information about a command.')
    '''
    Syntactically, the difference between positional and optional arguments is 
    that optional arguments start with - or --, while positional arguments don’t.
    '''

    #positional arguments
    parser.add_argument("--host", help="Input the server host ip", default="localhost", action="store")
    parser.add_argument("--port", help="Input the server port number", type=int, default=80, action="store")
    parser.add_argument("--get", help="executes a HTTP GET request and prints the response. For URLs, you must surround it around double quotes.")

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
                      action="store_true",required=False)
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
    #print(args.get)
    if(args.get != None):
        get_request(args.get, args.port, args.verbose)


if(__name__=="__main__"):
    main()









#notes for cli
#If you wish to call a function with an option then you must create a subclass of argparse.Action
#You must supply a__call__method.