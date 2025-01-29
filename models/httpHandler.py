from http.server import HTTPServer, BaseHTTPRequestHandler

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

       if self.path == '/':
           self.path = 'assets/web/index.html'
       try:
           file_to_open = open(self.path[1:]).read()
           self.send_response(200)
       except:
           file_to_open = "File not found"
           self.send_response(404)
       self.end_headers()
       self.wfile.write(bytes(file_to_open, 'utf-8'))

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

import http.server
import socketserver
import threading


def start_http_server(directory, port):
    # Change to the desired directory
    import os
    os.chdir(directory)

    # Define the handler and server
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("", port), handler)

    # Start the server
    print(f"Serving HTTP on localhost:{port} (Press CTRL+C to stop)")
    server.serve_forever()


# Define directory and port

# Main program continues here
print("HTTP server is running in the background. You can continue with the rest of your program.")
