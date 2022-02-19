Work by Ian Lopez & George Mavroeidis 
----------------------------------------------------------
# Requirements
1. Python 3+
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
