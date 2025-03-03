{
  "log": {
    "level": "fatal",
    "timestamp": true
  },
  "experimental": {
    "clash_api": {
      "external_controller": "127.0.0.1:9090",
      "access_control_allow_origin": [
        "http://127.0.0.1",
        "https://yacd.metacubex.one",
        "http://yacd.haishan.me",
        "https://metacubex.github.io"
      ],
      "access_control_allow_private_network": true
    },
    "cache_file": {
      "enabled": true,
      "store_fakeip": true
    }
  },
  "dns": {
    "servers": [
      {
        "type": "https",
        "server": "cloudflare-dns.com",
        "domain_resolver": "dns-google",
        "detour": "🚀Proxy",
        "tag": "dns-remote"
      },
      {
        "type": "udp",
        "server": "119.29.29.29",
        "tag": "dns-tencent"
      },
      {
        "type": "udp",
        "server": "8.8.8.8",
        "detour": "🚀Proxy",
        "tag": "dns-google"
      },
      {
        "type": "fakeip",
        "inet4_range": "240.0.0.0/4",
        "inet6_range": "fc00::/18",
        "tag": "dns-fakeip"
      }
    ],
    "rules": [
      {
        "clash_mode": "Direct",
        "server": "dns-tencent"
      },
      {
        "clash_mode": "Global",
        "server": "dns-google"
      },
      {
        "query_type": [
          "A",
          "AAAA"
        ],
        "rule_set": [
          "netflix",
          "netflixip"
        ],
        "action": "route",
        "server": "dns-fakeip"
      },
      {
        "rule_set": [
          "echemi{{ random_suffix }}",
          "mywechat{{ random_suffix }}",
          "cn",
          "mydirect{{ random_suffix }}"
        ],
        "server": "dns-google",
        "client_subnet": "47.104.0.0"
      },
      {
        "query_type": [
          "A",
          "AAAA"
        ],
        "server": "dns-fakeip"
      }
    ],
    "final": "dns-remote",
    "strategy": "ipv4_only",
    "independent_cache": true
  },
  "inbounds": [
    {
      "type": "tun",
      "tag": "tun-in",
      "address": [
        "172.18.0.1/30",
        "fdfe:dcba:9876::1/126"
      ],
      "auto_route": true,
      "strict_route": true,
      "route_exclude_address": [
        "10.0.0.0/8",
        "17.0.0.0/8",
        "192.168.0.0/16",
        "fc00::/7",
        "fe80::/10"
      ],
      "exclude_package": [
        {{ exclude_package }}
      ],
      "stack": "mixed",
      "platform": {
        "http_proxy": {
          "enabled": true,
          "server": "127.0.0.1",
          "server_port": 7890,
          "bypass_domain": [
            "localhost",
            "*.local",
            "push.apple.com",
            "talk.google.com",
            "mtalk.google.com",
            "alt1-mtalk.google.com",
            "alt2-mtalk.google.com",
            "alt3-mtalk.google.com",
            "alt4-mtalk.google.com",
            "alt5-mtalk.google.com",
            "alt6-mtalk.google.com",
            "alt7-mtalk.google.com",
            "alt8-mtalk.google.com"
          ]
        }
      }
    },
    {
      "type": "mixed",
      "tag": "mixed-in",
      "listen": "127.0.0.1",
      "listen_port": 7890
    }
  ],
  "outbounds": [
    {
      "tag": "🚀Proxy",
      "type": "selector",
      "outbounds": [
        {% for key, value in all_countrys.items() %}
        "{{ key }}",
        {% endfor %}
        "🤖Auto"
      ],
      "interrupt_exist_connections": true
    },
    {
      "tag": "🎬Netflix",
      "type": "selector",
      "outbounds": [
        "🚀Proxy",
        {% for key, value in all_countrys.items() %}
        "{{ key }}",
        {% endfor %}
        "🤖Auto"
      ],
      "interrupt_exist_connections": true
    },
    {
      "tag": "🤖AI",
      "type": "selector",
      "outbounds": [
        "🚀Proxy",
        {% for key, value in all_countrys.items() %}
        "{{ key }}",
        {% endfor %}
        "🤖Auto"
      ],
      "interrupt_exist_connections": true
    },
    {
      "tag": "🔐Crypto",
      "type": "selector",
      "outbounds": [
        "🚀Proxy",
        {% for key, value in all_countrys.items() %}
        "{{ key }}",
        {% endfor %}
        "🤖Auto"
      ],
      "interrupt_exist_connections": true
    },
    {
      "tag": "🏃‍Test",
      "type": "selector",
      "outbounds": [
        "🚀Proxy",
        {% for key, value in all_countrys.items() %}
        "{{ key }}",
        {% endfor %}
        "🤖Auto"
      ],
      "interrupt_exist_connections": true
    },
    {% for key, value in all_countrys.items() %}
    {
      "tag": "{{ key }}",
      "type": "selector",
      "outbounds": [
        {% for vps in value %}
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-anytls",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-h2",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-tuic",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-reality"{% if not loop.last %},{% endif %}
        {% endfor %}
      ],
      "interrupt_exist_connections": true
    },
    {% endfor %}
    {
      "tag": "🤖Auto",
      "type": "urltest",
      "outbounds": [
        {% for key, value in all_countrys.items() %}
        {% for vps in value %}
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-anytls",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-h2",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-tuic",
        "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-reality"
        {% endfor %}
        {% if not loop.last %},{% endif %}
        {% endfor %}
      ],
      "tolerance": 500,
      "interrupt_exist_connections": true
    },
    {% for key, value in all_countrys.items() %}
    {% for vps in value %}
    {
      "type": "anytls",
      "tag": "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-anytls",
      "server": "{{ vps.server_ip }}",
      "server_port": {{ vps.anytls_port }},
      "password": "{{ vps.password }}",
      "tls": {
        "enabled": true,
        "utls": {
          "enabled": true,
          "fingerprint": "firefox"
        },
        "reality": {
          "enabled": true,
          "public_key": "{{ vps.public_key }}",
          "short_id": "{{ vps.reality_sid }}"
        },
        "server_name": "yahoo.com",
        "insecure": true
      },
      "tcp_fast_open": true,
      "udp_fragment": true,
      "tcp_multi_path": false
    },
    {
      "type": "hysteria2",
      "tag": "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-h2",
      "server": "{{ vps.server_ip }}",
      "server_port": {{ vps.h2_port }},
      "up_mbps": 1000,
      "down_mbps": 1000,
      "obfs": {
        "type": "salamander",
        "password": "{{ vps.h2_obfs_password }}"
      },
      "password": "{{ vps.password }}",
      "tls": {
        "enabled": true,
        "server_name": "www.bing.com",
        "insecure": true,
        "alpn": [
          "h3"
        ]
      },
      "tcp_fast_open": true,
      "udp_fragment": true,
      "tcp_multi_path": false
    },
    {
      "type": "tuic",
      "tag": "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-tuic",
      "server": "{{ vps.server_ip }}",
      "server_port": {{ vps.tuic_port }},
      "uuid": "{{ vps.password }}",
      "password": "{{ vps.password }}",
      "tls": {
        "enabled": true,
        "server_name": "www.bing.com",
        "insecure": true,
        "alpn": [
          "h3"
        ]
      },
      "tcp_fast_open": true,
      "udp_fragment": true,
      "tcp_multi_path": false
    },
    {
      "type": "vless",
      "tag": "[{{ vps.country }}-{{ loop.index }}]{{ vps.vps_org }}-reality",
      "server": "{{ vps.server_ip }}",
      "server_port": {{ vps.reality_port }},
      "uuid": "{{ vps.password }}",
      "flow": "xtls-rprx-vision",
      "tls": {
        "enabled": true,
        "utls": {
          "enabled": true,
          "fingerprint": "firefox"
        },
        "reality": {
          "enabled": true,
          "public_key": "{{ vps.public_key }}",
          "short_id": "{{ vps.reality_sid }}"
        },
        "server_name": "yahoo.com",
        "insecure": true
      },
      "packet_encoding": "xudp",
      "tcp_fast_open": true,
      "udp_fragment": true,
      "tcp_multi_path": false
    },
    {% endfor %}
    {% endfor %}
    {
      "type": "direct",
      "tag": "direct",
      "domain_resolver": "dns-tencent"
    }
  ],
  "route": {
    "rules": [
      {
         "action": "sniff"
      },
      {
        "protocol": "dns",
        "port": [
          53,
          853
        ],
        "action": "hijack-dns"
      },
      {
        "clash_mode": "Direct",
        "outbound": "direct"
      },
      {
        "clash_mode": "Global",
        "outbound": "🚀Proxy"
      },
      {
        "domain_suffix": [
          {% if country == "DE" %}
          "mcc262.pub.3gppnetwork.org",
          {% endif %}
          {% if country == "US" %}
          "crl.t-mobile.com",
          "ps.t-mobile.com",
          "t-mobile.com",
          "mcc310.pub.3gppnetwork.org",
          {% endif %}
          "gspe1-ssl.ls.apple.com"
        ],
        "outbound": "🚀Proxy"
      },
      {
        "ip_cidr": [
          "1.1.1.1/32",
          "8.8.8.8/32"
        ],
        "outbound": "🎬Netflix"
      },
      {{ ad_route_rule }}
      {
        "protocol": "quic",
        "rule_set": [
          "cn",
          "cnip",
          "mydirect{{ random_suffix }}"
        ],
        "outbound": "direct"
      },
      {
        "protocol": "quic",
        "outbound": "🚀Proxy"
      },
      {
        "rule_set": [
          "netflix",
          "netflixip"
        ],
        "outbound": "🎬Netflix"
      },
      {
        "rule_set": [
          "ai"
        ],
        "outbound": "🤖AI"
      },
      {
        "rule_set": [
          "networktest"
        ],
        "outbound": "🏃‍Test"
      },
      {
        "rule_set": [
          "myproxy{{ random_suffix }}"
        ],
        "outbound": "🚀Proxy"
      },
      {
        "rule_set": [
          "private",
          "privateip",
          "echemi{{ random_suffix }}",
          "mywechat{{ random_suffix }}",
          "cn",
          "cnip",
          "mydirect{{ random_suffix }}"
        ],
        "outbound": "direct"
      }
    ],
    "rule_set": [
      {
        "type": "remote",
        "tag": "echemi{{ random_suffix }}",
        "format": "source",
        "url": "http://{{ server_ip }}/{{ www_dir_random_id }}/sb_echemi.json",
        "download_detour": "direct",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "mydirect{{ random_suffix }}",
        "format": "source",
        "url": "http://{{ server_ip }}/{{ www_dir_random_id }}/sb_mydirect.json",
        "download_detour": "direct",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "myproxy{{ random_suffix }}",
        "format": "source",
        "url": "http://{{ server_ip }}/{{ www_dir_random_id }}/sb_myproxy.json",
        "download_detour": "direct",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "mywechat{{ random_suffix }}",
        "format": "source",
        "url": "http://{{ server_ip }}/{{ www_dir_random_id }}/sb_wechat.json",
        "download_detour": "direct",
        "update_interval": "24h0m0s"
      },
      {{ ad_rule_set }}
      {
        "type": "remote",
        "tag": "cn",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/cn.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "cnip",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/cnip.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "netflix",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/netflix.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "netflixip",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/netflixip.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "ai",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/ai.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "networktest",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/networktest.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "private",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/private.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      },
      {
        "type": "remote",
        "tag": "privateip",
        "format": "binary",
        "url": "https://github.com/DustinWin/ruleset_geodata/releases/download/sing-box-ruleset/privateip.srs",
        "download_detour": "🚀Proxy",
        "update_interval": "24h0m0s"
      }
    ],
    "final": "🚀Proxy",
    "auto_detect_interface": true,
    "override_android_vpn": true,
    "default_domain_resolver": "dns-google"
  }
}
