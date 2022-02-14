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
are related to the HTTP 

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



def get_request(url, port, verbose=False, headers = None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlparser = urlparse(url)
    #host is 'httpbin.org', a "part" of the url variable/ full url that was passed in
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
        "Host:%s\r\n" % host
        #header option examples: (THEY MUST BE SURROUNDED BY QUOTES)
        #Accept-Language: en us,en;q=0.5
        #Accept-Encoding: gzip,deflate
        #Content-Type:application/json
        #check if we have passed in a list of headers from our -H arg
        if headers != None:
            #each key:value must end with \r\n (It's essentially the delimeter for lines
            # in a request, look at slides for chapter 2), but that is what is going on below
            for header in headers:
                request += header + "\r\n"

        #every request that is sent to the server must end with one last additional \r\n, 
        #that is what is happening below
        request+= "\r\n"
        #print(request,"\n")
        request = request.encode("utf-8")
        
        client.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = client.recv(1024)
        full_response = response.decode("utf-8")
        #split() returns a string list that is seperated by what you sent as an arg.
        response_details, response_data = full_response.split("\r\n\r\n")

        #show details with verbose if activated
        if(verbose):
            print(response_details, "\n")
        print(response_data)

    finally:
        client.close()

def post_request(url, port, verbose=False, headers = None, inline_data= None, file = None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    urlparser = urlparse(url)
    #host is 'httpbin.org', a "part" of the url variable/ full url that was passed in
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

        request = "POST " + url + " HTTP/1.0\r\n" \
        "Host:%s\r\n" % host
        #header option examples: (THEY MUST BE SURROUNDED BY QUOTES)
        #Accept-Language: en us,en;q=0.5
        #Accept-Encoding: gzip,deflate
        #Content-Type:application/json

        #check if we have passed in a list of headers from our -H arg
        if headers != None:
            #each key:value must end with \r\n (It's essentially the delimeter for lines
            # in a request, look at slides for chapter 2), but that is what is going on below
            for header in headers:
                request += header + "\r\n"
        #every request that is sent to the server must end with one last additional \r\n, 
        #that is what is happening below
        print(inline_data)
        #print(request,"\n")
        data = '''
        {
            "data": "{\\"Assignment\\": 1}",
        }
        '''
        print(data)
        request+="data:"+ data
        request+= "\r\n"
        request = request.encode("utf-8")
        
        client.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = client.recv(1024)
        full_response = response.decode("utf-8")
        #split() returns a string list that is seperated by what you sent as an arg.
        response_details, response_data = full_response.split("\r\n\r\n")

        #show details with verbose if activated
        if(verbose):
            print(response_details, "\n")
        print(response_data)

    finally:
        client.close()

#method for help text
def print_help_for_post_or_get(argument):
    if(argument == 'get' or argument == 'GET'):
        print('httpc --HELP get'\
                '\nusage: httpc --get "URL" [-v] [-h key:value]\n' \
                'Get executes a HTTP GET request for a given URL.\n' \
                '-v\t\tPrints the detail of the response such as protocol, status, and headers.\n'\
                "-h key:value\tAssociates headers to HTTP Request with the format 'key:value'.")
    elif(argument =='post' or argument=='POST'):
        print('httpc --HELP post'\
                '\nusage: httpc --post "URL" [-v] [-h key:value] [-d inline-data] [-f file]\n' \
                'Post executes a HTTP POST request for a given URL with inline data or from file.\n' \
                '-v\t\tPrints the detail of the response such as protocol, status, and headers.\n'\
                '-h key:value\t\tAssociates headers to HTTP Request with the format\n'\
                '-d string\t\tAssociates headers to HTTP Request with the format\n'\
                '-f file\t\tAssociates the content of a file to the body HTTP POST request.\n'\
                "Either [-d] or [-f] can be used but not both.")


def main():
    #parser is container to hold our arguments
    #for better understanding of the argparser 
    #visit: https://realpython.com/command-line-interfaces-python-argparse/
    parser = argparse.ArgumentParser(prog='httpc',
                                    description='httpc is a curl-like application but supports HTTP protocol only.',
                                    usage="\n\thttpclient.py command [arguments]", allow_abbrev=False,
                                    epilog='Use "httpclient.py help [command]" for more information about a command.')
    '''
    Syntactically, the difference between positional and optional arguments is 
    that optional arguments start with - or --, while positional arguments do not.
    We will be using optional for the most part
    '''
    #optional arguments
    parser.add_argument("--host", help="Input the server host ip", default="localhost", action="store")
    parser.add_argument("--port", help="Input the server port number", type=int, default=80, action="store")
    parser.add_argument("--get", help="executes a HTTP GET request and prints the response. For URLs, you must surround it around double quotes.")
    parser.add_argument("--post", help="executes a HTTP POST request and prints the response.")
    
    #store_true sends a true value when sent once!
    parser.add_argument("--HELP",help="Display the help text for the --get and --post request as well as other options for these requests."
                         , type=str, choices=['GET', 'get', 'POST', 'post'], required=False)
    #more optional arguments that can go with the above, -H, _v for example
    #this one below is -H for the headers "key:value" requirement
    '''
    3. To pass the headers value to your HTTP operation, you could use -H option. The latter means 
    setting the header of the request in the format "key: value." Notice that; you can have 
    multiple headers by having the -H option before each header parameter.
    WE WILL USE -H TO NOT CONFLICT WITH -h the default help feature argparse uses!!!!
    -h is the default argparse help option that cannot be changed.
    '''
    parser.add_argument('-H', required=False, help='Associates headers to HTTP Request with the format "key:value". You must pass the headers one by one starting with -H followed up by a space then the key:value which should be surrounded by double quotes.' ,action="append")
    parser.add_argument("-v", "--verbose", help="Turns on verbose mode for more details", 
                      action="store_true",required=False)
    parser.add_argument('-d', required=False, help="Associates an inline data to the body HTTP POST request.")
    #required argument in the params above "required=" can be used to force a user 
    #to add an argument, could be useful
    '''
    After you execute .parse_args(), what you get is a Namespace object that contains a simple 
    property for each input argument received from the command line.
    //////////////////////////////////////////////
    Example usages in cmd prompt:
    
    httpclient.py --get "http://httpbin.org/headers" -v -H "Accept-Language: en us,en;q=0.5" -H "Content-Type: application/json; charset=utf-8"
    
    httpclient.py --HELP get
    //////////////////////////////////////////////
    '''
    args = parser.parse_args()
    if(args.get != None):
        get_request(args.get, args.port, args.verbose, args.H)
    elif(args.post != None):
        post_request(args.post, args.port, args.verbose, args.H, args.d)
    elif(args.HELP!=None):
        print_help_for_post_or_get(args.HELP)


if(__name__=="__main__"):
    main()