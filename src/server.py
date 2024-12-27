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
import os


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

        match self.path[:self.path.find("?")].split("/")[1]:

            case "removeFromQueue":
                try:
                    self.__remove_from_queue()
                except Exception as e:
                    print(e)
            case "getNextFromQueue":
                try:
                    entry = self.__get_next_from_queue()
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/form-data')
                    file = b''
                    with open(f"{entry.photo}", "rb") as f:
                        file = f.read()
                    self.wfile.write(file)

                except Exception as e:
                    print(e)

    def do_POST(self):
        match self.path[:self.path.find("?")].split("/")[1]:

            case "addToQueue":
                try:
                    self.__add_to_queue()
                except Exception as e:
                    print(e)

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

        with open(f"../files/{timestamp}_{tag}.png", "wb") as f:
            f.write(data)

        for entry in self.server.queue:
            res = DeepFace.verify(entry.photo, f"../files/{timestamp}_{tag}.png")
            if res['verified']:
                print('Found same')
                os.system(f"rm ../files/{timestamp}_{tag}.png")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes('{ "result" : "such photo exists" }', "utf-8"))
                return
                # HANDLE EXISTING PHOTO

        self.server.queue.enqueue(tag=tag, path_to_photo=f"../files/{timestamp}_{tag}.png", timestamp=timestamp)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes('{ "result" : "ok" }', "utf-8"))

    def __remove_from_queue(self):
        params = dict(parse_qsl(urlparse(self.path).query))
        tag = params.get('tag')
        self.server.queue.remove_by_tag(tag)

    def  __get_next_from_queue(self):
        entry = self.server.queue.get_next_entry()
        return entry

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

    def service_actions(self):
        print("Service")
        cqueue.update_queue(self.queue)

    def getAuthKey(self):
        return self.auth_key


if __name__ == "__main__":
    print("\n\n")
    server = Server(('', 8000), Handler)
    print("Starting server %")

    # add here check for 30 minutes queuue
    server.serve_forever()
    server.server_close()
