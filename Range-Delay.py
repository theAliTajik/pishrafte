import time

def delayed_range(start, stop, step=1, delay=1.0):
    current = start
    while current < stop:
        yield current
        time.sleep(delay)
        current += step

for number in delayed_range(0, 5, delay=2.5):
    print(number)