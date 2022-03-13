Work by Ian Lopez & George Mavroeidis 
----------------------------------------------------------
# Requirements
Assignment 1. Python 3+
# Run httpclient.py
open command prompt and test http and tcp communication
with httpbin.org with GET or POST
do httpclient.py -h for more info on usage on your command prompt
here are a few samples on how to see communication with this client
and a server.

httpclient.py --get "http://httpbin.org/headers" -v -H "Accept-Language: en us,en;q=0.5" -H "Content-Type: application/json; charset=utf-8"
    httpclient.py --post "http://httpbin.org/post" -v -d "Assignment: 1" -H "Content-Type: application/json"
    httpclient.py --post "http://httpbin.org/post" -v -f sample.txt -H "Content-Type: application/json"
    httpclient.py --post "http://httpbin.org/post" -v
    httpclient.py --HELP get

----------------------------------------------------------

Assignment 2. Python 3+

# Run httpfserver.py
open command prompt and test http and tcp communication
with httpbin.org with GET or POST
do httpfserver.py -h for more info on usage on your command prompt
here are a few samples on how to see communication with this client
and a server.

# Run httpclient.py
open command prompt and test http and tcp communication
with httpbin.org with GET or POST
do httpclient.py -h for more info on usage on your command prompt
here are a few samples on how to see communication with this client
and a server.

httpclient.py --port 1234 --get "http://localhost/"
httpclient.py --port 1234 --get "http://localhost/bar.txt"
httpclient.py --port 1234 --post "http://localhost/bar.txt" -d "Test text"
httpclient.py --port 1234 --post "http://localhost/Directory3/bar.html" -d "<h>Hello World!</h>"
if we want to use 'key: value' pairing:
        httpclient.py --port 1234 --post "http://localhost/bar.txt" -d "Assignment: 1"
