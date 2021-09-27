import http.server
import os
import socketserver
import sys

PORT = 8000
HOST = "0.0.0.0"

if len(sys.argv) < 2:
    print("Usage: mini_server.py <html dir>")
    sys.exit(-1)

os.chdir(sys.argv[1])

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print("serving at", HOST, PORT)
    httpd.serve_forever()
