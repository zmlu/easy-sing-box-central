from flask import Flask, request
import requests

app = Flask(__name__)

def get_ip():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    else:
        return request.environ['REMOTE_ADDR']

@app.route('/api/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if 'name' not in request.args:
            return "Error", 400
        name = request.args.get('name')
    else:
        return "Method not allowed", 405

    ip = get_ip()
    url = f"http://{ip}/{name}/esb.config"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            else:
                print("未找到 'h2_obfs_password' 鍵")
        else:
            print(f"無法獲取數據：狀態碼 {response.status_code}")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 400
    return "OK"

if __name__ == "__main__":
    app.run()