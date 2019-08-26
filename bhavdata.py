import os
import requests
import io
import zipfile


API = "https://www.nseindia.com/products/content/sec_bhavdata_full.csv"

class BhavData(object):

    def __init__(self):
        self.url = API
        self.fname = API.split("/")[-1]
        self.response = None
        self.content = None
    def download(self):

        while(self.response is None or self.response.status_code != 200):
            self.response = requests.get(self.url, stream=True)
            content = self.response.text if self.response.status_code == 200 else None
            if content is not None:
                if self.content is None or content != self.content:
                    self.content = content
        self.parse()

    def parse(self):
        if self.content is None:
            return
        content = self.content.split("\n")
        header = content[0].split(",")
        content = content[1:]
        parsed = []
        for line in content:
            values = line.split(",")
            record = dict(zip(header, values))
            parsed.append(record)

        self.content = parsed
        


if __name__ == '__main__':
    data = BhavData()
    data.download()
    print(data.content) 
