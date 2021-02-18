# your Gmail account
import smtplib
import os

def send_mail(mailFrom,mailTo,appPass):
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login(mailFrom, appPass)

	catManage = 'cat /opt/projetmaster-master/logs/report'
	body = os.popen(catManage).read()

	# message to be sent
	message = "\r\n".join([
	  "From: PIOT",
	  "To: " + mailTo + "",
	  "Subject: Maintenance Report",
	  "",
	 "" + body  + ""
	  ])

	# sending the mail
	s.sendmail(mailFrom, mailTo, message)

	# terminating the session
	s.quit()
	return 0