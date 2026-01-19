from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os
import json
import mimetypes

# Sets a var for path of file root to current dir, __file__ points to where the script is
root_dir = os.path.dirname(os.path.abspath(__file__))

# Handler class to handle HTTP requests
class Handler(BaseHTTPRequestHandler):

    #GET method for getting data from client
    def do_GET(self):

        if self.path == "/":
            filename = os.path.join(root_dir, "index.html")
        else:
            filename = self.path.lstrip("/")

        # Will automatically check file type
        content_type = mimetypes.guess_type(filename)
        # Default case if no type was 
        if not content_type:
            content_type = "application/octet-stream"

        print(filename)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                print("Writing File") 
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()

            self.wfile.write(bytes(html_content, "utf-8"))

        except FileNotFoundError:
            self.send_error(404, f"File Not Found: {self.path}")

    #POST method for parsing data from user input and returning with new HTML
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            parsed_data = parse_qs(post_data.decode("utf-8"))

            response = f"<h1> Hello {parsed_data.get('name', [''])[0]}</h1>"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())
        except KeyboardInterrupt:
            pass


#Sets server address and port
server_address = ("localhost", 8000)
#Creates server, using the IP address and sets handler
httpd = HTTPServer(server_address, Handler)
#Debug
print("Running on localhost:8000")
#Runs server indefinitely
httpd.serve_forever()
