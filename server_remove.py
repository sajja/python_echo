#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json   


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("Echo Backend responding..\nRelease version: V2\nGET request for {}\n".format(self.path).encode('utf-8'))
        self.wfile.write("Headers..\n".encode("utf-8"))
        print(self.headers["Host"])
        
        logging.info(self.path)
        logging.info(self.headers)

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv
    run()
