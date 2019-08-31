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

    def extract(self):
        pass

if __name__ == '__main__':
    bhavdata = BhavData()
    bhavdata.extract()
    # bhavdata.parse()
