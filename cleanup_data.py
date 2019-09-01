import json

with open("universe.json") as f:
    data = json.loads(f.read())

header = data[list(data.keys())[0]].split("\n")[0].split(",")
for index, item in enumerate(header):
    if "Average Price" in item:
        price_index = index
    if "Date" in item:
        date_index = index

clean_data = {}
for stock in data:
    content = data[stock]
    lines = content.split("\n")
    lines = lines[1:] # throw away header
    cleaned = {}
    clean_data[stock] = cleaned
    for line in lines:
        line = line.split(",")
        if len(line) == len(header):
            date = line[date_index]
            price = line[price_index]
            date = date.strip('"')
            price = price.strip('"').strip()
            cleaned[date] = price
        clean_data[stock] = cleaned

with open("clean_data.json", "w") as f:
    f.write(json.dumps(clean_data))

