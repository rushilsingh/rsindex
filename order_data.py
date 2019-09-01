from collections import OrderedDict
import json
from dateutil import parser

with open("clean_data.json") as f:
    unordered_dict = json.loads(f.read())

parsed = {}
for stock, inner in unordered_dict.items():
    parsed[stock] = {}
    for date, price in inner.items():
        parsed[stock][parser.parse(date)] =  price


unordered_dict = parsed

ordered_dict = OrderedDict()
for key, value in sorted(unordered_dict.items(), key=lambda t: t[0]):
        inner_ordered_dict = OrderedDict()
        if type(value) is dict:
            inner_unordered_dict = value
            for inner_key, inner_value in sorted(inner_unordered_dict.items(), key = lambda x: x[0]):
                inner_ordered_dict[inner_key] = inner_value
        ordered_dict[key] = inner_ordered_dict


#check
dates_sorted = True
for stock in ordered_dict:
    data = ordered_dict[stock]
    previous = None
    for date in data:
        if previous is None:
            previous = date
        else:
            if previous>date:
                dates_sorted = False
                break
import pickle 
# using pickle so all object structures are preserved as is during serialization
if dates_sorted:
    with open("ordered.obj", "wb") as f:
        pickle.dump(ordered_dict, f)
