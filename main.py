from flask import Flask, request
from gevent.pywsgi import WSGIServer
import requests

from utils import write_config

app = Flask(__name__)

def get_ip():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    else:
        return request.environ['REMOTE_ADDR']

@app.route('/api/hello', methods=['GET'])
def hello():
    if request.method == 'GET':
        if 'name' not in request.args:
            return "Error", 400
    name = request.args.get('name')
    ip = get_ip()
    if ip.startswith('::ffff:'):
        ip = ip[len('::ffff:'):]
    url = f"http://{ip}/{name}/esb.config"
    print("url")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                write_config(ip, data)
                return data
            else:
                print("未找到 json")
        else:
            print(f"無法獲取數據：狀態碼 {response.status_code}")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 400
    return "OK"

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()