#!/bin/bash
saveConf() {

	if [ ! -d "/lib/ipSave/" ];then
		mkdir /lib/ipSave/
	fi
	touch /lib/ipSave/rulesIPtables
	#touch /lib/systemd/system/ipSave.service
	chmod -R 700 /lib/ipSave/
	chown -R cherrypy:root /opt/projetmaster-master
	iptables-save -f /lib/ipSave/rulesIPtables

	echo -e "[Unit]\nDescription=Restore rules\nRequires=network.target\nDefaultDependencies=no\n[Service]\nType=oneshot\nExecStart=iptables-restore /lib/ipSave/rulesIPtables\n\n[Install]\nWantedBy=multi-user.target\n" > /lib/systemd/system/ipSave.service

	echo -e "[Unit]\nDescription=CherryPy\nAfter=network.target\n\n[Service]\nType=simple\nUser=root\nGroup=root\nWorkingDirectory=/opt/projetmaster-master/graph/\nExecStart=/usr/bin/python3 tut01.py\n\n[Install]\nWantedBy=multi-user.target\n" > /lib/systemd/system/cherrypy.service
	
	systemctl enable ipSave.service
	systemctl enable cherrypy.service
	systemctl daemon-reload
	crontab -l > /lib/ipSave/mycron
	echo -e "10 * * * * /sbin/iptables-save -f /lib/ipSave/rulesIPtables" >> /lib/ipSave/mycron
	echo -e "30 05 * * * /opt/projetmaster-master/bash/runManage.sh" >> /lib/ipSave/mycron
	echo -e "30 08 * * * /opt/projetmaster-master/bash/runManage.sh" >> /lib/ipSave/mycron
	crontab /lib/ipSave/mycron
	rm /lib/ipSave/mycron
	echo -e "Rules are saved"
}
saveConf