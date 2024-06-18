#!/bin/bash
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install -y ./mount-s3.rpm

mkdir /home/ec2-user/data
chown -R ec2-user:ec2-user /home/ec2-user/data
mount-s3 mounted-bucket /home/ec2-user/data