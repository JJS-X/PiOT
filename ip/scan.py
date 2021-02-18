import shodan
import subprocess
import os
from mac import APImysql
import mysql.connector
from pexpect import pxssh

def shodan(api_key):
	try:
		curl_ip = "curl ifconfig.io"
		ipPublique = os.system(ipPublic)

		api = shodan.Shodan(api_key)
		results = api.search(ipPublic)

		if results['total'] == 0:
			result = "No result"
		else:
			result = str(results['total'])

		return result
	except shodan.exception.APIError:
		print("TimeOut try again")


def shodan_ip(api_key, ip_search):
	try:

		api = shodan.Shodan(api_key)
		results = api.search(ip_search)

		if results['total'] == 0:
			result = "No result"
		else:
			result = str(results['total'])

		return result
	except shodan.exception.APIError:
		print("TimeOut try again")

# Scan ip publique
# J'sais ap si on a le droit de faire ca ahah
def public_ip():
	nmap = 'nmap -sS "$(curl ifconfig.io 2>/dev/null)" | awk \'/^[0-9]/\''
	openPort = os.popen(nmap).read()
	return openPort
	pass

def port_open(ipToScan):
	#ipToScan = APImysql.select_ip_by_id(id)
	nmap = "nmap -sS " + ipToScan + " | awk '/^[0-9]/' | awk '{split($0,a,\"/\"); print a[1]}'"
	openPort = os.popen(nmap).read()
	return openPort

def attempt_con(ipToScan, macToSearch):
	#macToSearch = APImysql.select_mac_by_id(id)
	#ipToScan = APImysql.select_ip_by_id(id)
	# Connector mysql
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="corpus",
	  password="toor",
	  database="corpus"
	)
	mycursor = mydb.cursor(buffered=True)
	macRequest = "curl https://api.macvendors.com/" + macToSearch + " 2>/dev/null"
	nomModel = os.popen(macRequest).read()
	# print("The model is : " + nomModel)
	device = nomModel.partition(' ')[0]

	mycursor.execute("SELECT user FROM defaultPass WHERE device LIKE '%" + device + "%'")
	rec = mycursor.fetchall()
	user = str(rec).strip("[](),'")
	# print("The default user is : " + user)

	mycursor.execute("SELECT pass FROM defaultPass WHERE device LIKE '%" + device + "%'")
	records = mycursor.fetchall()
	passwd = str(records).strip("[](),'")
	# print("The default password is : " + passwd)

	try:
	    s = pxssh.pxssh()
	    hostname = ipToScan
	    username = user
	    password = passwd
	    s.login(hostname, username, password)
	    return True
	    pass
	except pxssh.ExceptionPxssh as e:
	    return False
	pass
