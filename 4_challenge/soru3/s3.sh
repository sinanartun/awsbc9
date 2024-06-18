#!/bin/bash
yum update -y
yum install -y python3

cat <<EOF > /home/ec2-user/create_files.py

import time
import os
from datetime import datetime

directory = "/home/ec2-user/generated_text_files"

if not os.path.exists(directory):
    os.makedirs(directory)

try:
    for _ in iter(int, 1):  

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.txt"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w') as file:
            file.write(f"This file was created on {timestamp}")
        
        print(f"Created file: {filename}")

        time.sleep(1)


except KeyboardInterrupt:
    print("Script stopped.")

EOF

python3 /home/ec2-user/create_files.py 
# kanit vural