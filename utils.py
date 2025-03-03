import json
import os
import random
import re
import subprocess
import sys
import uuid

config_file = os.path.expanduser('~/esb-c.config')

def write_config(remote_ip, remote_config):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[remote_ip] = remote_config

    with open(config_file, 'w') as write_f:
        write_f.write(json.dumps(data, indent=2, ensure_ascii=False))