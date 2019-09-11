#  Simulate some trade based on some initial conditions and decisions based on relative strength based strategy

"""
Prospective constants:
STARTING_CAPITAL = 1000
INVESTED_CAPITAL = 0
ROUGHLY:
PURCHASE_AMOUNT = PRICE * UNITS
INVESTED_CAPITAL += PURCHASE_AMOUNT
STARTING_CAPITAL -= PURCHASE_AMOUNT
TRADE is some buy/sell operation
... and so on. something like this.
"""
import pickle

with open("rsi_data.obj", "rb") as f:
    obj = pickle.load(f)

for stock in obj:
    mappings = obj[stock]
    lines = ["STOCK", "DATA", "RSI"]
    for date in mappings:
        rs = mappings[date]
        lines.append("%s, %s, %s" % (stock, date, rs))
    csv_data = "\n".join(lines)

print(csv_data)
