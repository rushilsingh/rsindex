import pickle
from collections import OrderedDict

"""
Prospective constants:
STARTING_CAPITAL = 1000
INVESTED_CAPITAL = 0
"""

PERIODS = 14  # Conventional value for periods in relative strength stategy

"""
ROUGHLY:
PURCHASE_AMOUNT = PRICE * UNITS
INVESTED_CAPITAL += PURCHASE_AMOUNT
STARTING_CAPITAL -= PURCHASE_AMOUNT
TRADE is some buy/sell operation
... and so on. something like this.
"""


class RSI(object):

    def __init__(self):
        self.obj = self.load()
        self.rs_values = {}

    def load(self):
        with open("ordered.obj", "rb") as f:
            obj = pickle.load(f)
            return obj

    def compute(self):
        rs_values = {}
        for stock, data in self.obj.items():

            profit = 0
            loss = 0
            base_date = None
            previous_price = None
            timedelta = 0
            periods = 0  # We want periods not just days as denoted by timedelta

            goal_periods = 14  # DECLARING CONSTANT

            end_reached = False  # What if fewer than goal_periods periods?
            for date, price in data.items():
                periods += 1
                if base_date is None:
                    base_date = date
                    previous_price = price
                else:
                    timedelta = date - base_date
                    timedelta = timedelta.days
                    pricedelta = float(price - previous_price) / \
                        previous_price * float(100.0)  # as percentage

                    # shorter timedelta for same gain or loss indicates higher intensity of change
                    pricedelta = pricedelta/float(timedelta)

                    profit_made = False
                    if pricedelta >= 0.0:
                        profit_made = True
                        profit += pricedelta
                    else:
                        pricedelta = abs(pricedelta)
                        loss += pricedelta
                    if end_reached:
                        profit = 0
                        loss = 0
                        if profit_made:
                            profit = pricedelta
                        else:
                            loss = pricedelta
                        quotient_numerator = (
                            average_gain*(goal_periods-1)) + profit
                        quotient_denominator = (
                            average_loss*(goal_periods-1)) + loss
                        if quotient_numerator <= 0.000000000:
                            rs = 0.0
                        elif quotient_denominator <= 0.0000000:
                            rs = 100.0
                        else:
                            quotient = quotient_numerator/quotient_denominator
                            main_denominator = 1+quotient
                            rs = 100 - (100/main_denominator)
                        self.rs_values[stock][date] = rs
                    elif periods >= goal_periods:
                        average_gain = profit/float(goal_periods)
                        average_loss = loss/float(goal_periods)
                        if average_gain <= 0.00000000:
                            rs = 0.0
                        elif average_loss <= 0.000000000:
                            rs = 100.0
                        else:
                            quotient = average_gain/average_loss
                            denominator = 1 + quotient
                            rs = float(100)/denominator
                        values = OrderedDict()
                        values[date] = rs

                        end_reached = True  # goal periods reached. move on to smoothing
                        self.rs_values[stock] = values

            if not end_reached:
                raise Exception("Insufficient data for meaningful analysis")

        return self.rs_values

    def smoothen(self, stock, date, price, average_gain, average_loss):
        pass


if __name__ == '__main__':
    rsi = RSI()
    data = rsi.compute()
    lines = ["STOCK", "DATA", "RSI"]
    for stock in data:
        mappings = data[stock]
        for date in mappings:
            rs = mappings[date]
            lines.append("%s, %s, %s" % (stock, date, rs))
    csv_data = "\n".join(lines)

    with open("rsi_data.csv", "w") as f:
        f.write(csv_data)
    with open("rsi_data.obj", "wb") as f:
        f.write(pickle.dumps(data))
