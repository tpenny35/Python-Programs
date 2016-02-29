import smtplib
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mailName = "pymail1017@gmail.com"
mailPass = "P3nny1017"

def sendmail(sendFrom,sendTo,sendSub,sendMsg,attachment):
    sendSub = sendSub + "\n"
    if sendFrom == "":
        sendFrom = mailName
    #sendFrom = "From: " + sendFrom

    attachments = attachment.split(',')

    outer = MIMEMultipart('Mixed')
    outer['Subject'] = sendSub
    outer['To'] = sendTo
    outer['From'] = sendFrom
    outer.preamble = 'Automated Email System.\n'

    outer.attach( MIMEText(sendMsg) )

    for file in attachments:
        if file != "":
            print(file)
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                #msg.add_header('Content-Disposition', 'attachment; filename=' + file)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments")
                raise


    composed = outer.as_string()
    
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(mailName, mailPass)
        server.sendmail(sendFrom, sendTo.split(","), composed)
        server.close()
    except smtplib.SMTPException():
        print("Something went wrong!")
