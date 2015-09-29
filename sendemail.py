import smtplib
import sys
import getopt
import argparse
import os

username = ""
password = ""

#opens file and reads in sensitive data
info_file = open("C:\\Python34\\Scripts\\info-file.txt","r")
for lines in info_file.readlines():
    if lines.find("username") >= 0:
        tmpStr = lines.replace("username=","")
        tmpStr = tmpStr.strip()
        username = tmpStr
    elif lines.find("password") >= 0:
        tmpStr = lines.replace("password=","")
        tmpStr = tmpStr.strip()
        password = tmpStr
info_file.close()

#input parameters
sendFrom = sys.argv[1]
sendTo   = sys.argv[2]
msg      = sys.argv[3]

#add a subject line
if msg.find("down") >= 0:
    subtxt = "Subject: Cams Server Alert \n"
elif msg.find("running") >= 0:
    subtxt = "Subject: Cams Server Notification \n"
else:
    subtxt = ""
print(msg)
print(sendTo)
print(sendFrom)

try:
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username, sendTo.split(","), subtxt + msg)
    server.close()
except smtplib.SMTPException():
    print("Something went wrong!")



