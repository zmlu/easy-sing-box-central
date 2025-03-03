screen -d
apt-get install -y git
apt-get install -y screen
screen -S esb-c -X quit
screen -wipe
echo "重置 venv..."
mkdir /opt/venv
rm -rf /opt/venv/easy-sing-box-central
cd /opt/venv && python3 -m venv easy-sing-box-central
echo "重置 easy-sing-box..."
rm -rf /opt/easy-sing-box-central/
cd /opt && git clone -q https://github.com/zmlu/easy-sing-box-central.git
screen -dmS esb-c
screen -x -S esb-c -p 0 -X stuff "cd /opt/easy-sing-box-central || exit"
screen -x -S esb-c -p 0 -X stuff "source /opt/venv/easy-sing-box-central/bin/activate"
screen -x -S esb-c -p 0 -X stuff "pip3 install -r requirements.txt"
screen -x -S esb-c -p 0 -X stuff "python3 main.py"