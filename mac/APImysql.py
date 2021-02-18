import mysql.connector
import os
from os import path
from pexpect import pxssh
import getpass
import hashlib
from contextlib import closing

if path.exists('/var/log/dhcpd.log') == True:
	# Get new @Mac
	macBash = "tail /var/log/dhcpd.log 2>/dev/null | grep \"DHCPREQUEST\" | awk '{split($0,a,\"from\"); print a[2]}' | awk '{print $1}' | tail -1 | tr -d \"\n\" "
	newMac = os.popen(macBash).read()
	pass

# Connector mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="corpus",
  password="toor",
  database="corpus"
)
mycursor = mydb.cursor(buffered=True)

def delete_table_mac():
	try:
		mycursor.execute("DROP TABLE macAdd;")
		mydb.commit()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

def delete_table_default_pass():
	try:
		mycursor.execute("DROP TABLE defaultPass;")
		mydb.commit()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

def create_table_pass():
	try:
		mycursor.execute("CREATE TABLE passwd ( id int NOT NULL AUTO_INCREMENT, user varchar(32), pass varchar(100), PRIMARY KEY (id));")
		mydb.commit()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

def display_base():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)
		mycursor = mydb.cursor(buffered=True)
		
		with closing( mydb.cursor() ) as mycursor:
			mycursor.execute("SELECT * FROM macAdd;")
			records = mycursor.fetchall()
			record = str(records).strip("[]")
		mydb.close()
		a = record.replace(")", "\n")
		b = a.replace("(", "")
		c = b.replace(", ", "")
		d = c.replace("'", " ")
		writeMac = d.replace("''", " ")

		hosts = open("/opt/projetmaster-master/ressource/fichierMAC", "w")
		hosts.write(writeMac + "\n")
		hosts.close()

		return record
	except mysql.connector.errors.ProgrammingError:
		errorC = "No @MAC found in the base"
		return errorC
	except mysql.connector.errors.OperationalError:
		# Connector mysql
		# mydb = mysql.connector.connect(
		#   host="localhost",
		#   user="corpus",
		#   password="toor",
		#   database="corpus"
		# )
		# mycursor = mydb.cursor(buffered=True)
		return "OperationalError"
		# display_base()
	pass

def create_table_default_pass():
	try:
		mycursor.execute("CREATE TABLE defaultPass ( id int NOT NULL AUTO_INCREMENT, device varchar(32), user varchar(32), pass varchar(32), PRIMARY KEY (id));")
		mydb.commit()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

def insert_default_pass():
	with open("ressource/defaultPass","r") as read_obj:
		for line in read_obj:
			unsplit = str(line).split(',')
			mycursor.execute("INSERT INTO defaultPass (device,user,pass) VALUES ('" + unsplit[0] + "','" + unsplit[1] + "','" + unsplit[2].strip('\n') + "') ")
			mydb.commit()
	pass

def create_table_mac():
	try:
		mycursor.execute("CREATE TABLE macAdd ( id int NOT NULL AUTO_INCREMENT, device varchar(32), ipA varchar(32), macA varchar(32), PRIMARY KEY (id));")
		mydb.commit()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

def test_existence_table(table):
	mycursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '" + table + "';")
	records = mycursor.fetchall()
	#record = str(records).strip("[]")
	print(record)
	pass

def select_mac_from_ip(ipAddr):
	try:
		mycursor.execute("SELECT macA FROM macAdd WHERE ipA LIKE '%" + ipAddr + "%';")
		records = mycursor.fetchall()
		if records == 0 :
			print("no data found ")
			pass
		record = str(records).strip("[](),'")
		print(mycursor.rowcount, "record found")
		if mycursor.rowcount == 0:
			return False
			pass
		pass
	except Exception as e:
		raise e
	return True

def select_ip_from_mac(macAddr):
	try:
		mycursor.execute("SELECT ipA FROM macAdd WHERE macA LIKE '%" + macAddr + "%';")
		records = mycursor.fetchall()
		return records
		pass
	except Exception as e:
		raise e
	pass
	return False

def select_ip_by_id(searchID):
	try:
		mycursor.execute("SELECT ipA FROM macAdd WHERE id=" + searchID + ";")
		records = mycursor.fetchall()
		record = str(records).strip("[](),'")
		return record
		pass
	except Exception as e:
		raise e
	pass
	return False

def select_mac_by_id(searchID):
	try:
		mycursor.execute("SELECT macA FROM macAdd WHERE id=" + str(searchID) + ";")
		records = mycursor.fetchall()
		record = str(records).strip("[](),'")
		return record
		pass
	except Exception as e:
		raise e
	pass
	return False

def authorize_ip(ipExt):
	hosts = open("/etc/hosts.allow", "a")
	hosts.write("ALL: " + ipExt + "\n")
	hosts.close()
	return 0

# Add mac in iptables and in the base
# addressM):
def add_mac(addressM):
	if create_table_mac() != False:
		create_table_mac()

	if select_ip_from_mac(addressM) != []:
		already="@MAC already in the base"
		return already

		# if input("Do you want to enter the addressM manually ? [Y/N] ") == "Y":
		# 	macToAdd = input("Enter Mac : ")
		# 	try:
		# 		# Add ip mac to the base
		# 		ipMac = "arp -n -i wlan0 | grep '" + macToAdd + "' | awk '{split($1,a,\" \"); print $1}' | tr -d \"\n\" "
		# 		ip_mac = os.popen(ipMac).read()

		# 		if ip_mac == "":
		# 			if input("No IP found \nDo you want to enter the IP ? [Y/N] ") == "Y":
		# 				ip_mac = input("Enter IP : ")
		# 				pass
		# 			else:
		# 				print("Alright")
		# 			pass
		# 		else:
		# 			print("Alright")

		# 		# Insert table
		# 		mycursor.execute("INSERT INTO macAdd (ipA,macA) VALUES ('" + ip_mac + "','" + macToAdd + "');")
		# 		mydb.commit()

		# 		mycursor.execute("SELECT id FROM macAdd WHERE ipA='" + ip_mac + "';")
		# 		record = mycursor.fetchone()
		# 		records = str(record).strip("[](),'")
		# 		print(records)
		# 		records = str(int(records) + 2)
		# 		addMac = "iptables -I FORWARD " + records + " -i wlan0 -m mac --mac-source " + macToAdd + " -j ACCEPT"
		# 		os.system(addMac)

		# 		print("@MAC added successfully ! ")

		# 	except Exception as e:
		# 		raise e
		# 	pass
		# else:
		# 	print("You\'re the boss")
	else:
		# Insert new @mac in mysql db
		# if input("Add this @MAC ? \n" + addressM + " [Y/N] : ") == "Y":
			# Add iptables mac rule
		try:
			# Add ip mac to the base
			# ipMac = "arp -n -i wlan0 | grep '" + addressM + "' | awk '{print $1}' | tr -d \"\n\""
			# ip_mac = os.popen(ipMac).read()

			ipMac = "grep 'DHCPACK' /var/log/dhcpd.log | grep '" + addressM + "' | awk '{print $8}' | sort -u | tr -d \"\n\" | tr -d '()'"
			ip_mac = os.popen(ipMac).read()


			deviceName = "grep 'DHCPACK' /var/log/dhcpd.log | grep '" + addressM + "' | awk '{print $11}' | sort -u | tr -d \"\n\" | tr -d '()'"
			device = os.popen(deviceName).read()

			# END OF AUTH

			# Create table
			mycursor.execute("INSERT INTO macAdd (device,ipA,macA) VALUES ('" + device + "','" + ip_mac + "','" + addressM + "');")
			mydb.commit()
			print("@MAC added successfully ! ")
			pass
		except Exception as e:
			raise e
		pass

		mycursor.execute("SELECT id FROM macAdd WHERE ipA='" + ip_mac + "';")
		record = mycursor.fetchone()
		records = str(record).strip("[](),'")

		records = str(int(records) + 2)
		addMac = "iptables -I FORWARD " + records + " -i wlan0 -m mac --mac-source " + addressM + " -j ACCEPT"
		os.system(addMac)

		# else:
		# 	print("Error")
	pass

	# DELETE MAC FROM BASE
def delete_mac(id):
	try:
		# display_base()
		# id = str(input("Select to delete : "))
		mycursor.execute("DELETE FROM macAdd WHERE id=" + id + ";")
		mydb.commit()
		# print("Deleted from the database")
		id = str(int(id) + 2)
		# print(id)
		# Injection dans id !!
		delMac = "iptables -D FORWARD " + id + ""
		# print(delMac)
		os.system(delMac)

		mycursor.execute("SELECT device,ipA,macA FROM macAdd;")
		confTable = mycursor.fetchall()
		mycursor.execute("DROP TABLE macAdd;")
		mydb.commit()
		# print('Deleted from firewall')

		# Increment auto id database
		create_table_mac()
		for item in confTable:
			device = item[0]
			ip = item[1]
			mac = item[2]
			mycursor.execute("INSERT INTO macAdd (device,ipA,macA) VALUES ('" + device + "','" + ip + "', '" + mac + "')")
			mydb.commit()
			pass
		confTable = ""
		# print("Database updated ")
		# True="Address MAC deleted"
		return True
		pass
	except mysql.connector.errors.ProgrammingError:
		# errProg="error programming"
		return False
		pass
	except Exception as e:
		raise e
		return False
	pass

def search_user():
	if create_table_pass() == True:
		print("You have to register ! ")
		user = input("Enter username : ")
		# SHA - 256
		passwd = getpass.getpass("Enter password : ")
		pass_hash = hashlib.sha256(passwd.encode())
		pass_hashed = pass_hash.hexdigest()

		mycursor.execute("INSERT INTO passwd (user,pass) VALUES ('" + user + "', '" + pass_hashed + "')")
		print("User registred\n")
		mydb.commit()
	else:
		print("Authentication\n")
		user = input("Enter username : ")
		passwd = getpass.getpass("Enter password : ")
		pass_hash = hashlib.sha256(passwd.encode())
		pass_hashed = pass_hash.hexdigest()

		mycursor.execute("SELECT user FROM passwd WHERE pass='" + pass_hashed + "'")
		rec = mycursor.fetchall()
		userBdd = str(rec).strip("[](),'")

		if userBdd == user:
			print("Identification granted")
			return True
			pass
		else:
			print("Sorry authentication refused")
	pass
	return False
