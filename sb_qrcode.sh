apt-get install -y qrencode jq

config_file="$HOME/esb-c.config"
www_dir_random_id=$(jq -r '.www_dir_random_id' "$config_file")
server_ip=$(jq -r '.server_ip' "$config_file")
server_port=$(jq -r '.server_port' "$config_file")
echo "\\e[1;33msing-box\\033[0m"
echo "\\e[1;32mhttp://${server_ip}:${server_port}/${www_dir_random_id}/sb.json\\033[0m"
echo ""

echo "sing-box://import-remote-profile?url=http%3A%2F%2F"+server_port+":"+server_port+"%2F8e59d9%2Fsb.json#esb" | qrencode -o - -t ANSI