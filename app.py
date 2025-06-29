from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
       self.send_response(200)
       self.send_header("Content-type", "text/html")
       self.end_headers()
       self.wfile.write(b"<html><body><h1> Hello MF </h1></body></html>")

     #def do_POST(self):


def run(server_class = HTTPServer, handler_class = SimpleHandler, port = 8080):
       server_address = ('0.0.0.0',port)
       httpd = server_class(server_address, handler_class)
       print ("starting MF server")
       httpd.serve_forever()

if __name__ == '__main__':
       run()


