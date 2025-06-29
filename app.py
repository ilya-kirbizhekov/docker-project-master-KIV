from http.server import BaseHTTPRequestHandler, HTTPServer
import os

UPLOAD_DIR = "./images"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
       self.send_response(200)
       self.send_header("Content-type", "text/html")
       self.end_headers()
       self.wfile.write(b"<html><body>"
                        b"<h1> File uploader...</h1>"
                        b"<form enctype=\"multipart/form-data\" method=\"POST\">"
                        b"<input name = \"file\" type = \"file\">"
                        b"<input type=\"submit\" value = \"Upload\">"
                        b"</body>"
                        b"</html>")


    def do_POST(self):
        content_type = self.headers.get('Content-Type','')
        if not content_type.startswith("multipart/form-data"):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Only multipart/form-data supported")
            return
        boundary = content_type.split("boundary")[-1].encode('utf-8')
        content_length = int(self.headers.get('Content-Length'))

        body = self.rfile.read(content_length)  # read full post body

        # split the body into parts
        parts = body.split(b"---" + boundary)
        for part in parts:
            if b'Content-Disposition' in part and b'name="file' in part:
                header, file_data = part.split(b'\r\n\r\n',1)
                header_lines =header.decode().split('\r\n')
                #extract the file name
                for line in header_lines:
                    if "filename=" in line:
                        filename = line.split("filename=")[-1].strip('""')
                        filepath = os.path.join(UPLOAD_DIR, os.path.basename(filename))
                        with open(filepath,'wb') as f:
                            f.write(file_data.rstrip(b'\r\n--'))
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"File uploaded: " + filename.encode())
                        return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"File upload failed")


def run(server_class = HTTPServer, handler_class = SimpleHandler, port = 8080):
       server_address = ('0.0.0.0',port)
       httpd = server_class(server_address, handler_class)
       print ("starting MF server")
       httpd.serve_forever()

if __name__ == '__main__':
       run()


