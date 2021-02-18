#!/bin/sh

nameEnp2s0f1=$(ip a | sed -n 7p | grep '^[0-9]' | cut -d ':' -f2 | cut -d ' ' -f2)
ipEnp2s0f1=$(ip a | sed -n 9p | cut -d ':' -f2 | cut -d ' ' -f6)
nameWg0=$(ip a | sed -n 11p | grep '^[0-9]' | cut -d ':' -f2 | cut -d ' ' -f2)
ipWg0=$(ip a | sed -n 13p | cut -d ':' -f2 | cut -d ' ' -f6)

echo "==============================="
echo Network
echo "-------------------------------"
echo "- LAN = "$nameEnp2s0f1 $ipEnp2s0f1
echo "- Wireguard = " $nameWg0 $ipWg0
echo "- WAN = "$(curl ifconfig.io 2>/dev/null)
echo "-------------------------------"
echo System
echo "-------------------------------"
echo "- Version OS =" $(head -1 /etc/os-release | awk '{split($0,a,"="); print a[2]}')
echo "- Uptime = "$(uptime | awk '{print $3,$4}' | cut -d ',' -f1)
echo "- Kernel = "$(uname -r)
echo "- Utilisateurs =" $(uptime | awk '{print $4,$5}' | tr -d ',')
echo "-------------------------------"
echo Memory
echo "-------------------------------"
echo "- Total memory = " $(free -m | grep Mem: | awk '{print $2}') "Mb"
echo "- Used memory =" $(free -m | grep Mem: | awk '{print $3}') "Mb"
echo "- Available memory = " $(free -m | grep Mem: | awk '{print $7}') "Mb"
echo "- Free memory = " $(free -m | grep Mem: | awk '{print $4}') "Mb"
echo "-------------------------------"
echo Disks
echo "-------------------------------"
echo "- Utilisation de SR1 =" $(df -hT | grep md127 | awk '{print $6}')
echo "- Utilisation de Ext =" $(df -hT | grep sde2 | awk '{print $6}')
echo "-------------------------------"
echo Updates
echo "-------------------------------"
apt list --upgradable 2>/dev/null | awk '{split($0,a,"/"); print a[1]}'
echo "==============================="