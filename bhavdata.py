import os
import requests
import io
import zipfile
import redis

API = "https://www.nseindia.com/products/content/sec_bhavdata_full.csv"

class BhavData(object):

    def __init__(self):
        self.content = None
        self.api = "01-01-2018-TO-31-12-2018%sALLN.csv"
        self.full_file_api = API
        self.load_universe()
        self.universe = ["20MICRONS"] #arbitrarily chosen

    def load_universe(self):
        response = requests.get(self.full_file_api)
        if response.code == 200:
            text = response.text
            lines = text.split("/n")
            lines = lines[1:]
            symbols = []
            for line in lines:
                symbol = line.split(",")
                if symbol not in line and len(symbols)<10:
                    symbols.append(symbol)
                if len(symbols) >= 10:
                    break
            self.universe = symbols
        else:
            self.load_universe()

    
    def extract(self):

        self.load_universe()
        data = {}
        for stock in self.universe:
            fname = self.api % stock
            with open("stocks/%s" % fname) as f:
                content = f.read()
            data[stock] = content
        self.content = data

    #TODO: Modify below methods to implement Relative Strength Strategy 

    def parse(self):
        self.extract()
        if self.content is None:
            return
        data = {}
        for stock in self.content:
            content = self.content[stock]
            content = content.split("\n")
            header = content[0].split(",")
            header = [i.strip('"').strip("'") for i in header]
            date_index = header.index("Date")
            content = content[1:]
            parsed = []
            for line in content:
                    values = line.split(",")
                    if len(values) == len(header):
                        values = [i.strip('"').strip("'") for i in values]
                        date = values[date_index]
                        record = dict(zip(header, values))
                        record = {date: record}
                        parsed.append(record)
            
            data[stock.strip("'").strip('"')] = parsed

if __name__ == '__main__':
    import requests
    text = requests.get(API).text
    with open(API.split("/")[-1], "w") as f:
        f.write(text)
    bhavdata = BhavData()
    bhavdata.parse()
