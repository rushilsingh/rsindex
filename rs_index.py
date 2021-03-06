import pickle
from collections import OrderedDict

FIRST_CYCLE = 14  # Conventional value for periods in relative strength stategy before moving to smoothing


class RSI(object):

    def __init__(self, obj_file="ordered.obj"):
        self.obj_file = obj_file
        self.obj = None
        self.rs_values = {}
        self.data = {}

    def load(self):
        with open(self.obj_file, "rb") as f:
            obj = pickle.load(f)
        self.obj = obj

    def compute(self):

        for stock, data in self.obj.items():

            cumulative_profit = 0
            cumulative_loss = 0

            base_date = None
            previous_price = None

            timedelta = 0
            periods = 0  # We want periods not just days as denoted by timedelta

            goal_periods = FIRST_CYCLE

            for date, price in data.items():
                periods += 1
                if base_date is None:
                    base_date = date
                    previous_price = price
                else:
                    timedelta = date - base_date
                    timedelta = timedelta.days

                    base_date = date
                    pricedelta = float(price - previous_price) / \
                        previous_price * float(100.0)  # as percentage

                    # we divide by timedelta below because shorter timedelta for same gain or loss indicates higher intensity of change
                    pricedelta = pricedelta/float(timedelta)

                    if pricedelta >= 0.0:  # profit
                        current_profit = pricedelta
                        cumulative_profit += current_profit
                    else:  # loss
                        current_loss = abs(pricedelta)
                        cumulative_loss += current_loss

                    if (periods-1) >= goal_periods:  # We hit smoothing trigger last cycle
                        quotient_numerator = (
                            average_gain*(goal_periods-1)) + current_profit
                        quotient_denominator = (
                            average_loss*(goal_periods-1)) + current_loss

                        # Need to update cumulatives and averages to reflect current date data
                        cumulative_profit += current_profit
                        cumulative_loss += current_loss

                        average_gain = cumulative_profit/float(periods)
                        average_loss = cumulative_loss/float(periods)

                        if quotient_numerator <= 0.0000000000:  # Limit for minima
                            rs = 0.0
                        elif quotient_denominator <= 0.0000000000:  # Limit for maxima
                            rs = 100.0
                        else:
                            quotient = quotient_numerator/quotient_denominator
                            main_denominator = 1+quotient
                            rs = 100 - (100/main_denominator)

                        self.rs_values[stock][date] = rs

                    elif periods >= goal_periods:  # Do some computations and move to smoothing from next iteration of for loop

                        average_gain = cumulative_profit/float(goal_periods)
                        average_loss = cumulative_loss/float(goal_periods)

                        if average_gain <= 0.0000000000:
                            rs = 0.0
                        elif average_loss <= 0.000000000000:
                            rs = 100.0
                        else:
                            quotient = average_gain/average_loss
                            denominator = 1 + quotient
                            rs = float(100)/denominator
                        values = OrderedDict()
                        values[date] = rs
                        self.rs_values[stock] = values

            if periods < goal_periods:
                raise Exception("Insufficient data for meaningful analysis")



if __name__ == '__main__':
    rsi = RSI()
    rsi.load()
    rsi.compute()
    data = rsi.rs_values
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
