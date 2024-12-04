"""
// Copyright 2024 mas0yama & the_empr3ss & mih@ilovna
"""
import subprocess
import requests
import time
import base64


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


if __name__ == "__main__":
    client = Client("")
    client.Run()