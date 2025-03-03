screen -d
apt-get install -y git
apt-get install -y screen
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

config_file="$HOME/esb-c.config"
www_dir_random_id=$(jq -r '.www_dir_random_id' "$config_file")
server_ip=$(jq -r '.server_ip' "$config_file")
server_port=$(jq -r '.server_port' "$config_file")
echo "\\e[1;33msing-box\\033[0m"
echo "\\e[1;32mhttp://"server_ip":"+server_port+"/"+www_dir_random_id+"/sb.json\\033[0m"
echo ""