import time
from datetime import datetime
import os

def print_timestamp():
    name = os.getenv('NAME', 'DefaultName')
    while True:
        print(f"{name}: {datetime.now().isoformat()}")
        time.sleep(1)

if __name__ == "__main__":
    print_timestamp()
