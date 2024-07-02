import time
from datetime import datetime

def print_timestamp():
    while True:
        print(datetime.now().isoformat())
        time.sleep(1)

if __name__ == "__main__":
    print_timestamp()