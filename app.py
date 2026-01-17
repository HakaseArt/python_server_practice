from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os

base_dir = os.path.dirname("Python/week3_server/")
print(base_dir)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if os.path.exists(base_dir):
            if self.path == "/":
                print("path")
                filename = "index.html"
            else:
                filename = self.path
        else:
            self.send_error(404, f"File Not Found: {base_dir}")
        
        try:

            with open(filename, "r", encoding="utf-8") as f:
                print("Writing File") 
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(html_content, "utf-8"))

        except FileNotFoundError:
            self.send_error(404, f"File Not Found: {self.path}")

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


server_address = ("localhost", 8000)
httpd = HTTPServer(server_address, Handler)
print("Running on localhost:8000")
httpd.serve_forever()
