start = "01-08-2019"
end = "30-08-2019"
API = "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=AB&segmentLink=3&symbolCount=2&series=ALL&dateRange=+&fromDate=01-08-2019&toDate=30-08-2019&dataType=PRICEVOLUMEDELIVERABLE"


def download(api):
    import requests
    response = requests.get(api)
    content = response.text if response.status_code == 200 else None
    if content is not None:
        with open("data.html", "w") as f:
            f.write(content)




if __name__ == '__main__':
    download(API) 
