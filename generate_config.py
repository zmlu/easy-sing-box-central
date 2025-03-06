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
server_port = 6713

env = Environment(
    loader=PackageLoader("generate_config"),
    autoescape=select_autoescape()
)


def generate_singbox():
    server_ip, server_port, www_dir_random_id, nginx_www_dir = init_base_config()
    random_suffix = ''.join(random.sample(uuid.uuid4().hex, 6))
    ad_dns_rule = env.get_template("/sing-box/ad_dns_rule.json").render(random_suffix=random_suffix) + ","
    ad_route_rule = env.get_template("/sing-box/ad_route_rule.json").render(random_suffix=random_suffix) + ","
    ad_rule_set = env.get_template("/sing-box/ad_rule_set.json").render(random_suffix=random_suffix) + ","
    exclude_package = env.get_template("/sing-box/exclude_package.tpl").render() + ","
    exclude_package = re.sub(r'#.*', '', exclude_package)
    all_countrys = get_all_country()
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

    with open(nginx_www_dir + "/sb.json", 'w') as file:
        file.write(json.dumps(json.loads(sb_json_content), indent=2, ensure_ascii=False))

    with open(nginx_www_dir + "/sb-noad.json", 'w') as file:
        file.write(json.dumps(json.loads(sb_noad_json_content), indent=2, ensure_ascii=False))

    os.system("cp ./templates/sing-box/my/sb_echemi.json " + nginx_www_dir)
    os.system("cp ./templates/sing-box/my/sb_mydirect.json " + nginx_www_dir)
    os.system("cp ./templates/sing-box/my/sb_myproxy.json " + nginx_www_dir)
    os.system("cp ./templates/sing-box/my/sb_wechat.json " + nginx_www_dir)

def init_base_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            esb_c_config = json.load(file)
    else:
        esb_c_config = {}

    www_dir_random_id = esb_c_config.get('www_dir_random_id', ''.join(random.sample(uuid.uuid4().hex, 6)) + "_esbc")
    esb_c_config['www_dir_random_id'] = www_dir_random_id

    curl_out = subprocess.check_output(['curl', '-s', '-4', 'ip.network/more'])
    data_str = curl_out.decode('utf-8')
    ip_infp = json.loads(data_str)
    server_ip = ip_infp.get('ip')
    esb_c_config['server_ip'] = server_ip
    esb_c_config['server_port'] = server_port

    with open(config_file, 'w') as write_f:
        write_f.write(json.dumps(esb_c_config, indent=2, ensure_ascii=False))

    nginx_www_dir = "/var/www/html/" + www_dir_random_id
    if not os.path.exists(nginx_www_dir):
        os.makedirs(nginx_www_dir)

    return server_ip, server_port, www_dir_random_id, nginx_www_dir


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
        if key == 'www_dir_random_id' or key == 'server_ip' or key == 'server_port':
            continue
        country_list.add(value['country'])
    country_list = sorted(list(country_list))
    country_map = {}
    for country in country_list:
        vps_list = []
        for key, value in esb_c_config.items():
            if key == 'www_dir_random_id' or key == 'server_ip' or key == 'server_port':
                continue
            if country == value['country']:
                vps_list.append(value)
        country_map[replace_country_with_emoji(country)] = vps_list
    return country_map


def replace_country_with_emoji(country):
    # 完整國家和地區列表，按照 ISO 3166-1 alpha-2 標準
    if country == "AD":
        country = "🇦🇩安道爾"
    if country == "AE":
        country = "🇦🇪阿聯酋"
    if country == "AF":
        country = "🇦🇫阿富汗"
    if country == "AG":
        country = "🇦🇬安提瓜和巴布達"
    if country == "AI":
        country = "🇦🇮安圭拉"
    if country == "AL":
        country = "🇦🇱阿爾巴尼亞"
    if country == "AM":
        country = "🇦🇲亞美尼亞"
    if country == "AO":
        country = "🇦🇴安哥拉"
    if country == "AQ":
        country = "🇦🇶南極"
    if country == "AR":
        country = "🇦🇷阿根廷"
    if country == "AS":
        country = "🇦🇸美屬薩摩亞"
    if country == "AT":
        country = "🇦🇹奧地利"
    if country == "AU":
        country = "🇦🇺澳洲"
    if country == "AW":
        country = "🇦🇼阿魯巴"
    if country == "AX":
        country = "🇦🇽奧蘭群島"
    if country == "AZ":
        country = "🇦🇿亞塞拜疆"
    if country == "BA":
        country = "🇧🇦波斯尼亞和黑塞哥維那"
    if country == "BB":
        country = "🇧🇧巴貝多"
    if country == "BD":
        country = "🇧🇩孟加拉"
    if country == "BE":
        country = "🇧🇪比利時"
    if country == "BF":
        country = "🇧🇫布吉納法索"
    if country == "BG":
        country = "🇧🇬保加利亞"
    if country == "BH":
        country = "🇧🇭巴林"
    if country == "BI":
        country = "🇧🇮布隆迪"
    if country == "BJ":
        country = "🇧🇯貝南"
    if country == "BL":
        country = "🇧🇱聖巴泰勒米"
    if country == "BM":
        country = "🇧🇲百慕達"
    if country == "BN":
        country = "🇧🇳汶萊"
    if country == "BO":
        country = "🇧🇴玻利維亞"
    if country == "BQ":
        country = "🇧🇶荷屬加勒比"
    if country == "BR":
        country = "🇧🇷巴西"
    if country == "BS":
        country = "🇧🇸巴哈馬"
    if country == "BT":
        country = "🇧🇹不丹"
    if country == "BV":
        country = "🇧🇻布韋島"
    if country == "BW":
        country = "🇧🇼波札那"
    if country == "BY":
        country = "🇧🇾白俄羅斯"
    if country == "BZ":
        country = "🇧🇿貝里斯"
    if country == "CA":
        country = "🇨🇦加拿大"
    if country == "CC":
        country = "🇨🇨科科斯群島"
    if country == "CD":
        country = "🇨🇩剛果民主共和國"
    if country == "CF":
        country = "🇨🇫中非共和國"
    if country == "CG":
        country = "🇨🇬剛果共和國"
    if country == "CH":
        country = "🇨🇭瑞士"
    if country == "CI":
        country = "🇨🇮象牙海岸"
    if country == "CK":
        country = "🇨🇰庫克群島"
    if country == "CL":
        country = "🇨🇱智利"
    if country == "CM":
        country = "🇨🇲喀麥隆"
    if country == "CN":
        country = "🇨🇳中國"
    if country == "CO":
        country = "🇨🇴哥倫比亞"
    if country == "CR":
        country = "🇨🇷哥斯大黎加"
    if country == "CU":
        country = "🇨🇺古巴"
    if country == "CV":
        country = "🇨🇻維德角"
    if country == "CW":
        country = "🇨🇼庫拉索"
    if country == "CX":
        country = "🇨🇽聖誕島"
    if country == "CY":
        country = "🇨🇾塞浦路斯"
    if country == "CZ":
        country = "🇨🇿捷克"
    if country == "DE":
        country = "🇩🇪德國"
    if country == "DJ":
        country = "🇩🇯吉布提"
    if country == "DK":
        country = "🇩🇰丹麥"
    if country == "DM":
        country = "🇩🇲多米尼克"
    if country == "DO":
        country = "🇩🇴多米尼加共和國"
    if country == "DZ":
        country = "🇩🇿阿爾及利亞"
    if country == "EC":
        country = "🇪🇨厄瓜多"
    if country == "EE":
        country = "🇪🇪愛沙尼亞"
    if country == "EG":
        country = "🇪🇬埃及"
    if country == "EH":
        country = "🇪🇭西撒哈拉"
    if country == "ER":
        country = "🇪🇷厄立特里亞"
    if country == "ES":
        country = "🇪🇸西班牙"
    if country == "ET":
        country = "🇪🇹衣索比亞"
    if country == "FI":
        country = "🇫🇮芬蘭"
    if country == "FJ":
        country = "🇫🇯斐濟"
    if country == "FK":
        country = "🇫🇰福克蘭群島"
    if country == "FM":
        country = "🇫🇲密克羅尼西亞"
    if country == "FO":
        country = "🇫🇴法羅群島"
    if country == "FR":
        country = "🇫🇷法國"
    if country == "GA":
        country = "🇬🇦加彭"
    if country == "GB":
        country = "🇬🇧英國"
    if country == "GD":
        country = "🇬🇩格瑞那達"
    if country == "GE":
        country = "🇬🇪喬治亞"
    if country == "GF":
        country = "🇬🇫法屬圭亞那"
    if country == "GG":
        country = "🇬🇬根西"
    if country == "GH":
        country = "🇬🇭迦納"
    if country == "GI":
        country = "🇬🇮直布羅陀"
    if country == "GL":
        country = "🇬🇱格陵蘭"
    if country == "GM":
        country = "🇬🇲甘比亞"
    if country == "GN":
        country = "🇬🇳幾內亞"
    if country == "GP":
        country = "🇬🇵瓜地洛普"
    if country == "GQ":
        country = "🇬🇶赤道幾內亞"
    if country == "GR":
        country = "🇬🇷希臘"
    if country == "GS":
        country = "🇬🇸南喬治亞和南桑威奇群島"
    if country == "GT":
        country = "🇬🇹瓜地馬拉"
    if country == "GU":
        country = "🇬🇺關島"
    if country == "GW":
        country = "🇬🇼幾內亞比索"
    if country == "GY":
        country = "🇬🇾蓋亞那"
    if country == "HK":
        country = "🇭🇰香港"
    if country == "HM":
        country = "🇭🇲赫德島和麥克唐納群島"
    if country == "HN":
        country = "🇭🇳宏都拉斯"
    if country == "HR":
        country = "🇭🇷克羅埃西亞"
    if country == "HT":
        country = "🇭🇹海地"
    if country == "HU":
        country = "🇭🇺匈牙利"
    if country == "ID":
        country = "🇮🇩印尼"
    if country == "IE":
        country = "🇮🇪愛爾蘭"
    if country == "IL":
        country = "🇮🇱以色列"
    if country == "IM":
        country = "🇮🇲曼島"
    if country == "IN":
        country = "🇮🇳印度"
    if country == "IO":
        country = "🇮🇴英屬印度洋領地"
    if country == "IQ":
        country = "🇮🇶伊拉克"
    if country == "IR":
        country = "🇮🇷伊朗"
    if country == "IS":
        country = "🇮🇸冰島"
    if country == "IT":
        country = "🇮🇹意大利"
    if country == "JE":
        country = "🇯🇪澤西"
    if country == "JM":
        country = "🇯🇲牙買加"
    if country == "JO":
        country = "🇯🇴約旦"
    if country == "JP":
        country = "🇯🇵日本"
    if country == "KE":
        country = "🇰🇪肯亞"
    if country == "KG":
        country = "🇰🇬吉爾吉斯"
    if country == "KH":
        country = "🇰🇭柬埔寨"
    if country == "KI":
        country = "🇰🇮基里巴斯"
    if country == "KM":
        country = "🇰🇲葛摩"
    if country == "KN":
        country = "🇰🇳聖克里斯多福及尼維斯"
    if country == "KP":
        country = "🇰🇵北韓"
    if country == "KR":
        country = "🇰🇷韓國"
    if country == "KW":
        country = "🇰🇼科威特"
    if country == "KY":
        country = "🇰🇾開曼群島"
    if country == "KZ":
        country = "🇰🇿哈薩克"
    if country == "LA":
        country = "🇱🇦寮國"
    if country == "LB":
        country = "🇱🇧黎巴嫩"
    if country == "LC":
        country = "🇱🇨聖盧西亞"
    if country == "LI":
        country = "🇱🇮列支敦士登"
    if country == "LK":
        country = "🇱🇰斯里蘭卡"
    if country == "LR":
        country = "🇱🇷賴比瑞亞"
    if country == "LS":
        country = "🇱🇸賴索托"
    if country == "LT":
        country = "🇱🇹立陶宛"
    if country == "LU":
        country = "🇱🇺盧森堡"
    if country == "LV":
        country = "🇱🇻拉脫維亞"
    if country == "LY":
        country = "🇱🇾利比里亞"
    if country == "MA":
        country = "🇲🇦摩洛哥"
    if country == "MC":
        country = "🇲🇨摩納哥"
    if country == "MD":
        country = "🇲🇩摩爾多瓦"
    if country == "ME":
        country = "🇲🇪蒙特內哥羅"
    if country == "MF":
        country = "🇲🇫聖馬丁"
    if country == "MG":
        country = "🇲🇬馬達加斯加"
    if country == "MH":
        country = "🇲🇭馬紹爾群島"
    if country == "MK":
        country = "🇲🇰北馬其頓"
    if country == "ML":
        country = "🇲🇱馬利"
    if country == "MM":
        country = "🇲🇲緬甸"
    if country == "MN":
        country = "🇲🇳蒙古"
    if country == "MO":
        country = "🇲🇴澳門"
    if country == "MP":
        country = "🇲🇵北馬里亞納群島"
    if country == "MQ":
        country = "🇲🇶馬提尼克"
    if country == "MR":
        country = "🇲🇷茅利塔尼亞"
    if country == "MS":
        country = "🇲🇸蒙特塞拉特"
    if country == "MT":
        country = "🇲🇹馬爾他"
    if country == "MU":
        country = "🇲🇺模里西斯"
    if country == "MV":
        country = "🇲🇻馬爾地夫"
    if country == "MW":
        country = "🇲🇼馬拉威"
    if country == "MX":
        country = "🇲🇽墨西哥"
    if country == "MY":
        country = "🇲🇾馬來西亞"
    if country == "MZ":
        country = "🇲🇿莫三比克"
    if country == "NA":
        country = "🇳🇦納米比亞"
    if country == "NC":
        country = "🇳🇨新喀里多尼亞"
    if country == "NE":
        country = "🇳🇪尼日"
    if country == "NF":
        country = "🇳🇫諾福克島"
    if country == "NG":
        country = "🇳🇬奈及利亞"
    if country == "NI":
        country = "🇳🇮尼加拉瓜"
    if country == "NL":
        country = "🇳🇱荷蘭"
    if country == "NO":
        country = "🇳🇴挪威"
    if country == "NP":
        country = "🇳🇵尼泊爾"
    if country == "NR":
        country = "🇳🇷諾魯"
    if country == "NU":
        country = "🇳🇺紐埃"
    if country == "NZ":
        country = "🇳🇿紐西蘭"
    if country == "OM":
        country = "🇴🇲阿曼"
    if country == "PA":
        country = "🇵🇦巴拿馬"
    if country == "PE":
        country = "🇵🇪秘魯"
    if country == "PF":
        country = "🇵🇫法屬玻里尼西亞"
    if country == "PG":
        country = "🇵🇬巴布亞新幾內亞"
    if country == "PH":
        country = "🇵🇭菲律賓"
    if country == "PK":
        country = "🇵🇰巴基斯坦"
    if country == "PL":
        country = "🇵🇱波蘭"
    if country == "PM":
        country = "🇵🇲聖皮埃爾和密克隆"
    if country == "PN":
        country = "🇵🇳皮特凱恩群島"
    if country == "PR":
        country = "🇵🇷波多黎各"
    if country == "PS":
        country = "🇵🇸巴勒斯坦"
    if country == "PT":
        country = "🇵🇹葡萄牙"
    if country == "PW":
        country = "🇵🇼帛琉"
    if country == "PY":
        country = "🇵🇾巴拉圭"
    if country == "QA":
        country = "🇶🇦卡達"
    if country == "RE":
        country = "🇷🇪留尼旺"
    if country == "RO":
        country = "🇷🇴羅馬尼亞"
    if country == "RS":
        country = "🇷🇸塞爾維亞"
    if country == "RU":
        country = "🇷🇺俄羅斯"
    if country == "RW":
        country = "🇷🇼盧安達"
    if country == "SA":
        country = "🇸🇦沙烏地阿拉伯"
    if country == "SB":
        country = "🇸🇧索羅門群島"
    if country == "SC":
        country = "🇸🇨塞席爾"
    if country == "SD":
        country = "🇸🇩蘇丹"
    if country == "SE":
        country = "🇸🇪瑞典"
    if country == "SG":
        country = "🇸🇬新加坡"
    if country == "SH":
        country = "🇸🇭聖赫倫那"
    if country == "SI":
        country = "🇸🇮斯洛維尼亞"
    if country == "SJ":
        country = "🇸🇯斯瓦爾巴群島和揚馬延島"
    if country == "SK":
        country = "🇸🇰斯洛伐克"
    if country == "SL":
        country = "🇸🇱獅子山"
    if country == "SM":
        country = "🇸🇲聖馬利諾"
    if country == "SN":
        country = "🇸🇳塞內加爾"
    if country == "SO":
        country = "🇸🇴索馬利亞"
    if country == "SR":
        country = "🇸🇷蘇利南"
    if country == "SS":
        country = "🇸🇸南蘇丹"
    if country == "ST":
        country = "🇸🇹聖多美和普林西比"
    if country == "SV":
        country = "🇸🇻薩爾瓦多"
    if country == "SX":
        country = "🇸🇽聖馬丁"
    if country == "SY":
        country = "🇸🇾敘利亞"
    if country == "SZ":
        country = "🇸🇿史瓦帝尼"
    if country == "TC":
        country = "🇹🇨特克斯和凱科斯群島"
    if country == "TD":
        country = "🇹🇩查德"
    if country == "TF":
        country = "🇹🇫法屬南部領地"
    if country == "TG":
        country = "🇹🇬多哥"
    if country == "TH":
        country = "🇹🇭泰國"
    if country == "TJ":
        country = "🇹🇯塔吉克"
    if country == "TK":
        country = "🇹🇰托克勞"
    if country == "TL":
        country = "🇹🇱東帝汶"
    if country == "TM":
        country = "🇹🇲土庫曼"
    if country == "TN":
        country = "🇹🇳突尼西亞"
    if country == "TO":
        country = "🇹🇴東加"
    if country == "TR":
        country = "🇹🇷土耳其"
    if country == "TT":
        country = "🇹🇹千里達及托巴哥"
    if country == "TV":
        country = "🇹🇻吐瓦魯"
    if country == "TW":
        country = "🇹🇼台灣"
    if country == "TZ":
        country = "🇹🇿坦尚尼亞"
    if country == "UA":
        country = "🇺🇦烏克蘭"
    if country == "UG":
        country = "🇺🇬烏干達"
    if country == "UM":
        country = "🇺🇲美國本土外小島嶼"
    if country == "US":
        country = "🇺🇸美國"
    if country == "UY":
        country = "🇺🇾烏拉圭"
    if country == "UZ":
        country = "🇺🇿烏茲別克"
    if country == "VA":
        country = "🇻🇦梵蒂岡"
    if country == "VC":
        country = "🇻🇨聖文森及格瑞那丁"
    if country == "VE":
        country = "🇻🇪委內瑞拉"
    if country == "VG":
        country = "🇻🇬英屬維京群島"
    if country == "VI":
        country = "🇻🇮美屬維京群島"
    if country == "VN":
        country = "🇻🇳越南"
    if country == "VU":
        country = "🇻🇺萬那杜"
    if country == "WF":
        country = "🇼🇫瓦利斯和富圖納"
    if country == "WS":
        country = "🇼🇸薩摩亞"
    if country == "YE":
        country = "🇾🇪葉門"
    if country == "YT":
        country = "🇾🇹馬約特"
    if country == "ZA":
        country = "🇿🇦南非"
    if country == "ZM":
        country = "🇿🇲尚比亞"
    if country == "ZW":
        country = "🇿🇼辛巴威"
    return country

def process_client_config():
    project_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_path = os.path.join(project_base_dir, 'easy-sing-box-central')
    os.system(f"cd {project_path} && python3 generate_config.py")

if __name__ == '__main__':
    generate_singbox()

