class BhavData(object):

    def __init__(self):
        self.content = None
        self.api = "01-01-2018-TO-31-12-2018%sALLN.csv"

        # chosen by iterating through data in full file and choosing first 10 stocks that have non-empty data for the year 2018
        self.universe = ['20MICRONS', '21STCENMGM', '3IINFOTECH', '3MINDIA',
                         '3PLAND', '5PAISA', '63MOONS', '8KMILES', 'A2ZINFRA', 'AARON']

    def extract(self):
        try:
            data = {}
            for stock in self.universe:
                fname = self.api % stock
                with open("stocks/%s" % fname) as f:
                    content = f.read()
                    data[stock] = content
        except Exception as e:
            print(e)
        else:
            self.content = data
            with open("universe.json", "w") as f:
                import json
                f.write(json.dumps(self.content))
            print(data)


if __name__ == '__main__':
    bhavdata = BhavData()
    bhavdata.extract()
    # bhavdata.parse()
