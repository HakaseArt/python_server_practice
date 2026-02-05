from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from dataclasses import dataclass, field, asdict
import os, json, mimetypes, uuid

# Sets a var for path of file root to current dir, __file__ points to where the script is
root_dir = os.path.dirname(os.path.abspath(__file__))

@dataclass
class user:
    firstname: str
    lastname: str
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))

# Handler class to handle HTTP requests
class Handler(BaseHTTPRequestHandler):

    #GET method for getting data from client
    def do_GET(self):

        if self.path == "/":
            filename = os.path.join(root_dir, "index.html")
        else:
            filename = self.path.lstrip("/")

        # Will automatically check file type, with a default case if none are found
        mimtype, _ = mimetypes.guess_type(filename)
        content_type = mimtype or "application/octet-stream"

        print(filename)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                print("Writing File") 
                html_content = f.read()

            html_content = html_content.replace("{{name}}", "User")

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        except FileNotFoundError:
            self.send_error(404, f"File Not Found: {self.path}")

    #POST method for parsing data from user input and returning with new HTML
    def do_POST(self):
        
        try:

            # Size or length of data being sent from the HTTP header, 
            # lets python know how much to read and when to stop
            content_length = int(self.headers.get("Content-Length", 0))

            # Reads the raw data, and decodes, from binary into a readable format that python can use
            # Uses UTF-8, a translator turning all text into a displayable character 
            # regardless of what language, emoji, etc
            raw_data = self.rfile.read(content_length).decode("utf-8")

            # Translates the raw data into a usable format, ex. firstname=name&lastname=name into a list dict
            user_input = parse_qs(raw_data)

            # Gets the values and inputs them into their respected fields of the data struct
            new_user =  user(
                firstname=user_input.get("firstname", "Firstname"),
                lastname=user_input.get("lastname", "Lastname")
            )

            # Hard coded to get the firstname from the list, need to change to 
            # and add a condition if the user didn't add a first name
            display_name = user_input.get("firstname", [""][0])

            # Absolute path
            json_path = os.path.join(root_dir, "data.json")

            # Empty array for json population
            all_data = []

            # Checks if the JSON exists to load, if not it'll create it
            if os.path.exists(json_path):

                with open(json_path, "r", encoding="utf-8") as f:

                    try:
                        all_data = json.load(f)
                    except json.JSONDecodeError:
                        all_data = []

            # Appends the data from the HTML form casted as a dict
            all_data.append(asdict(new_user))

            # Rewrites/appends data back into the JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4)

            # Reads the HTML file and changes {{name}} to first name
            with open(os.path.join(root_dir, "index.html"), "r", encoding="utf-8") as f:
                html_content = f.read().replace("{{name}}", display_name[0])

            # Block of necessary HTTP coding
            # Response to browser
            self.send_response(200)
            # Sends HTML data header
            self.send_header("Content-type", "text/html")
            # Ends header data
            self.end_headers()
            # End of file where data will be sent to browser, 
            # self.wfile the write stream to the servers browser
            # write the action of data that is being transmitted,
            # endcodes the data into binary
            self.wfile.write(html_content.encode("utf-8"))

        except (json.JSONDecodeError, Exception) as e:
            self.send_error(400, f"Bad request: {e}")


#Sets server address and port
server_address = ("localhost", 8000)
#Creates server, using the IP address and sets handler
httpd = HTTPServer(server_address, Handler)
#Debug
print("Running on localhost:8000")
#Runs server indefinitely
httpd.serve_forever()
