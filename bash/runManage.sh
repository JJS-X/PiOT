#!/bin/bash
#	Last edit : 26 01 2021

export PATHUSER="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Formatting
echo "===============================" > $PATHUSER/../logs/report
date >> $PATHUSER/../logs/report
echo "===============================" >> $PATHUSER/../logs/report
echo "Manage" >> $PATHUSER/../logs/report
echo "-------------------------------" >> $PATHUSER/../logs/report

# DS_Store
bash $PATHUSER/removeDS.sh

# SUID
bash $PATHUSER/findSUID.sh

# IP
bash $PATHUSER/findIP.sh

echo -e "===============================
Base MAC
-------------------------------" >> $PATHUSER/../logs/report
if [[ -e /opt/projetmaster-master/ressource/fichierMAC ]]; then
	cat /opt/projetmaster-master/ressource/fichierMAC >> $PATHUSER/../logs/report
fi

# MOTD
bash $PATHUSER/updateMotd.sh >> $PATHUSER/../logs/report
