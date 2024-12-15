"""
// Copyright 2024 mas0yama & the_empr3ss & mih@ilovna
"""
import subprocess
import requests
import time
import base64

DOMAIN = ""


def timestamp():
    return base64.b64encode(bytes(str(time.time()), "utf-8")).decode("utf-8").replace("==", "").replace("=", "")


class Client:
    def __init__(self, server_address):
        self.TIMER = 20
        self.session = requests.Session()
        self.saddr = server_address
        self.auth_token = "QWERTY=="
        self.headers = {f"Host": f"{server_address}",
                        'Authorization': f'Basic {self.auth_token}'}

    def HandleResponse(self, response):

        if response['data'] == "":
            return

    def Run(self):
        print("Running %")
        while True:
            try:
                print("Trying")
                response = self.session.get(
                    f"https://{self.saddr}/public_storage/commands.json", headers=self.headers).json()
                self.HandleResponse(response)
            except Exception as e:
                print(e)
            time.sleep(self.TIMER)


def post_add_to_queue(tag, path_to_photo):
    r = requests.post(DOMAIN + f"/addToQueue?tag={tag}", files={'file': open(path_to_photo, "rb")})
    print(r)
    return r

def get_remove_from_queue(tag):
    r = requests.get(DOMAIN + f"/removeFromQueue?tag={tag}")


if __name__ == "__main__":
    # client = Client("")
    # client.Run()
    with open("vaterland.png", "rb") as f:
        dat = f.read()
    requests.post("http://127.0.0.1:8000/addToQueue?tag=5", files={'file': open("img.png", "rb")})
