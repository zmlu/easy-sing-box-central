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
screen -S esb-c
cd /opt/easy-sing-box-central || exit
echo "安装 easy-sing-box-central 依赖..."
source /opt/venv/easy-sing-box-central/bin/activate
pip3 install -r requirements.txt
echo "啟動服務..."
python3 main.py