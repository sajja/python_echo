#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from multiprocessing import Pool
from multiprocessing import cpu_count
import json   

import signal
stop_loop = 0

def exit_chld(x, y):
    global stop_loop
    stop_loop = 1

def f(x):
    global stop_loop
    while not stop_loop:
        x*x


class S(BaseHTTPRequestHandler):
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
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        data = post_data.decode('utf-8')

        if data == "load":
            logging.info("Starting CPU loading...")
            processes = cpu_count()
            print('-' * 20)
            print('Running load on CPU(s)')
            print('Utilizing %d cores' % processes)
            print('-' * 20)
            pool = Pool(processes)
            pool.map(f, range(processes))   


        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
