apt-get install -y qrencode jq

clear

config_file="$HOME/esb-c.config"
www_dir_random_id=$(jq -r '.www_dir_random_id' "$config_file")
server_ip=$(jq -r '.server_ip' "$config_file")
echo -e "\e[1;33msing-box\\033[0m"
echo -e "\e[1;32mhttp://${server_ip}/${www_dir_random_id}/sb.json\\033[0m"
echo -e ""

echo "sing-box://import-remote-profile?url=http%3A%2F%2F${server_ip}%2F${www_dir_random_id}%2Fsb.json#esb" | qrencode -o - -t ANSI