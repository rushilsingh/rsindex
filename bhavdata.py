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
        self.universe = ["20MICRONS"]
    def extract(self):
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
        self.content = data
    
    #TODO: Modify and use below code if db required
    """
    def insert(self):
        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        #red = redis.Redis()
        red.flushdb()
        pipe = red.pipeline()
        n = 0
        for record in self.content:
            symbol = record["SYMBOL"]
            symbol = "\"" + symbol + "\"" if " " in symbol else symbol
            import json
            red.hset("SYMBOLS", symbol, json.dumps(record))
            n += 1
            if (n % 64) == 0:
                pipe.execute()
                pipe = red.pipeline()
        pipe.execute()
        self.loaded = True
    """

if __name__ == '__main__':
    bhavdata = BhavData()
    bhavdata.parse()
