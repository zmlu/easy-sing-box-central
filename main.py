from flask import Flask, request
from gevent.pywsgi import WSGIServer
import requests
import os

from generate_config import write_config, get_random_www_id, server_port

app = Flask(__name__)

config_file = os.path.expanduser('~/esb-c.config')

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
    print("Fetching config from {}".format(url))
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
    www_dir_random_id = get_random_www_id()
    nginx_www_dir = "/static/" + www_dir_random_id
    if not os.path.exists(nginx_www_dir):
        os.makedirs(nginx_www_dir)

    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port=server_port)
    # Production
    http_server = WSGIServer(('', server_port), app)
    http_server.serve_forever()