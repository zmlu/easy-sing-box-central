from flask import Flask, request
from gevent.pywsgi import WSGIServer
import requests
import os

from generate_config import write_config, init_base_config, process_client_config

app = Flask(__name__, static_folder='/static')

config_file = os.path.expanduser('~/esb-c.config')

def get_ip():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    else:
        return request.environ['REMOTE_ADDR']

@app.route('/api/hello', methods=['POST'])
def hello():
    ip = get_ip()
    if ip.startswith('::ffff:'):
        ip = ip[len('::ffff:'):]
    try:
        if request.is_json:
            data = request.get_json()
            if data:
                write_config(ip, data)
                return data
            else:
                print("未找到 json")
        else:
            print(f"無法獲取數據")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 400
    return "OK"

if __name__ == '__main__':
    server_ip, server_port, www_dir_random_id, nginx_www_dir = init_base_config()

    process_client_config()
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port=server_port)
    # Production
    http_server = WSGIServer(('', server_port), app)
    http_server.serve_forever()