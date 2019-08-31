import os
import requests
import io
import zipfile


class BhavData(object):

    def __init__(self):
        self.content = None
        self.api = "01-01-2018-TO-31-12-2018%sALLN.csv"
        self.load_universe()

        # chosen by iterating through data in full file and choosing first 10 stocks that have non-empty data for the year 2018
        self.universe = ['20MICRONS', '21STCENMGM', '3IINFOTECH', '3MINDIA',
                         '3PLAND', '5PAISA', '63MOONS', '8KMILES', 'A2ZINFRA', 'AARON']

    def load_universe(self):
        with open("universe") as f:
            text = f.read()
            list = text.split(",")


    def extract(self):

        self.load_universe()
        data = {}
        for stock in self.universe:
            fname = self.api % stock
            try:
                with open("stocks/%s" % fname) as f:
                    lines = f.readlines()
                    new_lines = []
                    for line in lines:
                        value = line.split(",")[0]
                        value = value.strip('"')
                        print(value)
                        print(stock)
                        if value == "Symbol" or value == stock:
                            new_lines.append(line)
                            print(new_lines)
                
                    if new_lines != lines:
                        with open("stocks/%s" % fname, "w") as f:
                            f.writelines(new_lines)
                    
                data[stock] = content
            except Exception as e:
                pass

if __name__ == '__main__':
    bhavdata = BhavData()
    bhavdata.extract()
    # bhavdata.parse()
