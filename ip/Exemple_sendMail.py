# your Gmail account
import smtplib
import os

def send_mail_exemple():
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login("jjs10.mail@gmail.com", "juoihlsgiesddiet")

	catManage = 'cat /opt/projetmaster-master/logs/report'
	body = os.popen(catManage).read()

	# message to be sent
	message = "\r\n".join([
	  "From: JJS10",
	  "To: jjs10.mail@gmail.com",
	  "Subject: Maintenance Report",
	  "",
	 "" + body  + ""
	  ])

	# sending the mail
	s.sendmail("jjs10.mail@gmail.com", "jjs10.mail@gmail.com", message)

	# terminating the session
	s.quit()
	pass