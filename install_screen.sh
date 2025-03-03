cd /opt/easy-sing-box-central || exit
echo "安装 easy-sing-box-central 依赖..."
source /opt/venv/easy-sing-box-central/bin/activate
pip3 install -r requirements.txt
echo "啟動服務..."
python3 main.py