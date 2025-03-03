import json
import os
import random
import re
import subprocess
import sys
import uuid
import requests
from jinja2 import Environment, PackageLoader, select_autoescape

config_file = os.path.expanduser('~/esb-c.config')
# config_file = "/Users/zmlu/Downloads/esb-c.config"
server_port = 6713

env = Environment(
    loader=PackageLoader("generate_config"),
    autoescape=select_autoescape()
)

def get_ip_info():
    curl_out = subprocess.check_output(['curl', '-s', '-4', 'ip.network/more'])
    data_str = curl_out.decode('utf-8')
    ip_infp = json.loads(data_str)
    server_ip = ip_infp.get('ip')
    return server_ip

def generate_singbox():
    www_dir_random_id = get_random_www_id()
    random_suffix = ''.join(random.sample(uuid.uuid4().hex, 6))
    ad_dns_rule = env.get_template("/sing-box/ad_dns_rule.json").render(random_suffix=random_suffix) + ","
    ad_route_rule = env.get_template("/sing-box/ad_route_rule.json").render(random_suffix=random_suffix) + ","
    ad_rule_set = env.get_template("/sing-box/ad_rule_set.json").render(random_suffix=random_suffix) + ","
    exclude_package = env.get_template("/sing-box/exclude_package.tpl").render() + ","
    exclude_package = re.sub(r'#.*', '', exclude_package)
    all_countrys = get_all_country()
    server_ip = get_ip_info()
    sb_json_tpl = env.get_template("/sing-box/sb.json.tpl")
    sb_json_content = sb_json_tpl.render(
        server_ip=server_ip,
        server_port=server_port,
        all_countrys=all_countrys,
        exclude_package=exclude_package,
        www_dir_random_id=www_dir_random_id,
        random_suffix=random_suffix
    )
    sb_noad_json_content = sb_json_tpl.render(
        server_ip=server_ip,
        server_port=server_port,
        all_countrys=all_countrys,
        ad_dns_rule=ad_dns_rule,
        ad_route_rule=ad_route_rule,
        ad_rule_set=ad_rule_set,
        exclude_package=exclude_package,
        www_dir_random_id=www_dir_random_id,
        random_suffix=random_suffix
    )

    static_path = get_static_path()
    static_www_dir = static_path + "/" + www_dir_random_id
    if not os.path.exists(static_www_dir):
        os.makedirs(static_www_dir)

    print(sb_noad_json_content)
    with open(static_www_dir + "/sb.json", 'w') as file:
        file.write(json.dumps(json.loads(sb_noad_json_content), indent=2, ensure_ascii=False))

    with open(static_www_dir + "/sb-ad.json", 'w') as file:
        file.write(json.dumps(json.loads(sb_json_content), indent=2, ensure_ascii=False))

    os.system("cp ./templates/sing-box/my/sb_echemi.json " + static_www_dir)
    os.system("cp ./templates/sing-box/my/sb_mydirect.json " + static_www_dir)
    os.system("cp ./templates/sing-box/my/sb_myproxy.json " + static_www_dir)
    os.system("cp ./templates/sing-box/my/sb_wechat.json " + static_www_dir)


def get_random_www_id():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            esb_c_config = json.load(file)
    www_dir_random_id = esb_c_config.get('www_dir_random_id', ''.join(random.sample(uuid.uuid4().hex, 6)))
    esb_c_config['www_dir_random_id'] = www_dir_random_id
    with open(config_file, 'w') as write_f:
        write_f.write(json.dumps(esb_c_config, indent=2, ensure_ascii=False))
    return www_dir_random_id

def write_config(remote_ip, remote_config):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            esb_c_config = json.load(file)
    else:
        esb_c_config = {}
    esb_c_config[remote_ip] = remote_config

    with open(config_file, 'w') as write_f:
        write_f.write(json.dumps(esb_c_config, indent=2, ensure_ascii=False))
    process_client_config()


def get_all_country():
    country_list = set()
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            esb_c_config = json.load(file)
    for key, value in esb_c_config.items():
        if key == 'www_dir_random_id':
            continue
        country_list.add(value['country'])
    country_list = sorted(list(country_list))
    country_map = {}
    for country in country_list:
        vps_list = []
        for key, value in esb_c_config.items():
            if key == 'www_dir_random_id':
                continue
            if country == value['country']:
                vps_list.append(value)
        country_map[replace_country_with_emoji(country)] = vps_list
    return country_map

def replace_country_with_emoji(country):
    if country == "DE":
        country = "🇩🇪德國"
    if country == "JP":
        country = "🇯🇵日本"
    if country == "US":
        country = "🇺🇸美國"
    if country == "HK":
        country = "🇭🇰香港"
    if country == "TW":
        country = "🇹🇼台灣"
    return country

def get_static_path():
    project_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_base_dir, 'easy-sing-box-central', 'static')

def process_client_config():
    generate_singbox()