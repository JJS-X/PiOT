#	Script corpus
#	Last edit : 26 01 2021
import os
import mac.APImysql
from init import init_lan
from uninstall import remove_lan
import sys
import ip.scan
import ip.sendMail

#Installation du FW IOT <-> LAN
def install_fw():
	if input("Install Firewall ? [Y/N] ") == "Y":
		#1
		flushRules = "./bash/flushRules.sh"
		os.system(flushRules)
		#2
		acceptPing = "./bash/acceptPing.sh"
		os.system(acceptPing)
		#3
		conReseau = "./bash/conReseau.sh"
		os.system(conReseau)
		#4
		fail2Ban = "./bash/fail2Ban.sh"
		os.system(fail2Ban)
		#5
		installKnock = "./bash/installKnock.sh"
		os.system(installKnock)
		#6
		policyDrop = "./bash/policyDrop.sh"
		os.system(policyDrop)
		# #7
		saveConf = "./bash/saveConf.sh"
		os.system(saveConf)
		pass
	else:
		print("Alright no problem ! ")
	pass

def add_addr_mac():
	pass
	if input("Add a @MAC ? [Y/N] ") == "Y":
		mac.APImysql.add_mac()
		pass
	else:
		print("Alright buddy ! ")

def delete_addr_mac():
	if input("Delete a rule ? [Y/N] ") == "Y":
		mac.APImysql.delete_mac()
		pass
	pass

def setup_lan():
	if input("Setup LAN ? [Y/N] ") == "Y":
		init_lan.write_config_file()
		init_lan.write_find_file()
		mac.APImysql.create_table_default_pass()
		mac.APImysql.insert_default_pass()
		mac.APImysql.create_table_mac()
		print("Table created")
		pass
	pass

def lan_remove():
	if input("Remove LAN ? [Y/N] ") == "Y":
		remove_lan()
		flushR = "./bash/flushRules.sh"
		os.system(flushR)		
		pass
	pass

def scan_public_ip():
	if input("Scan public IP ? [Y/N] ") == "Y":
		ip.scan.public_ip()
		pass
	pass

def run_manage():
	manage = "./bash/runManage.sh"
	os.system(manage)
	ip.sendMail.send_mail()
	pass

def menu():
	out = 0
	while out == 0 :
		print("**********************************************")
		print("	WECOME IN OUR AWESOME TOOL")
		choice = input("""
	1: Set up LAN
	2: Install Firewall
	3: Add mac address
	4: Display mac address
	5: Scan port
	6: Remove LAN
	7: Delete mac address
	8: Scan public IP
	9: Run Manage
	10: Authoriwe IP
	Q: Exit
**********************************************
	Please enter your choice: """)
		if choice == "1":
			setup_lan()
		elif choice == "2":
			install_fw()
		elif choice == "3":
			add_addr_mac()
		elif choice == "4":
			mac.APImysql.display_base()
		elif choice == "5":
			ip.scan.port_open()
		elif choice == "6":
			lan_remove()
		elif choice == "7":
			delete_addr_mac()
		elif choice == "8":
			scan_public_ip()
		elif choice == "9":
			run_manage()
		elif choice == "10":
			authorize_ip()
		elif choice == "Q":
			print("Exit")
			out = 1
		pass
	pass

if mac.APImysql.search_user() == True:
	menu()
else:
	print("Authentication")
	mac.APImysql.search_user()
	menu()