#!/bin/bash

# 检查是否为root下运行
[[ $EUID -ne 0 ]] && echo -e '\033[1;35m请在root用户下运行脚本\033[0m' && exit 1

screen -d
apt install -y git
apt install -y screen
apt install -y nginx
apt install -y jq
apt install -y python3
apt install -y python3-pip
apt install -y python3-pip
apt install -y python3-venv
screen -S esb-c -X quit
screen -wipe
echo "重置 venv..."
mkdir /opt/venv
rm -rf /opt/venv/easy-sing-box-central
cd /opt/venv && python3 -m venv easy-sing-box-central
echo "重置 easy-sing-box-central..."
rm -rf /opt/easy-sing-box-central/
cd /opt && git clone -q https://github.com/zmlu/easy-sing-box-central.git
screen -dmS esb-c
screen -x -S esb-c -p 0 -X stuff "cd /opt/easy-sing-box-central && source /opt/venv/easy-sing-box-central/bin/activate && pip3 install -r requirements.txt && echo '啟動服務...' && python3 main.py
"
echo "重启 nginx..."
systemctl start nginx
systemctl restart nginx
systemctl enable nginx