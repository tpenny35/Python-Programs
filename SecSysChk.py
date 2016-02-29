import subprocess
import os
import datetime
import time
import pymailer2


#ip addresses/from email/to email/email password
ipList  = []
fromAddr = ""
toAddr   = ""
password = ""

#list of bad ping responses
badResp  = "Destination host unreachable"
badResp2 = "Request timed out"

#function that pings ip address and checks response
def checkIP(Address):
    return_code = subprocess.call(["ping",Address])
    if return_code == 0:
        response = str(subprocess.check_output(["ping", Address], shell=True))
        tmpstr = ''
        for lines in response:
            tmpstr = tmpstr + lines

        numbad = tmpstr.count(badResp)
        numbad2 = tmpstr.count(badResp2)

        if numbad + numbad2 > 2:
            return "No"
        else:
            return "Yes"
        
    else:
        return "No"


#opens file and reads in sensitive data
info_file = open("C:\Python34\Scripts\info-file.txt","r")
for lines in info_file.readlines():
    if lines.find("ipaddress") >= 0:
        tmpStr = ""
        tmpStr = lines.replace("ipaddress=","")
        tmpStr = tmpStr.strip()
        ipList.append(tmpStr)
    elif lines.find("from") >= 0:
        tmpStr = lines.replace("from=","")
        tmpStr = tmpStr.strip()
        fromAddr = tmpStr
    elif lines.find("to") >= 0:
        tmpStr = lines.replace("to=","")
        tmpStr = tmpStr.strip()
        toAddr = tmpStr
info_file.close()

#checks ip address
for ipAdd in ipList:
    is_ok = checkIP(ipAdd)
    #print(is_ok)
    logfile = open("C:\Python34\Scripts\camslog.log","a")
    logfile.write("\n")
    daytime = datetime.datetime.now()
    tmpstr = daytime.isoformat() + " Online Status of " + ipAdd + ": " + is_ok
    logfile.write(tmpstr) 
    logfile.close()
    if is_ok == "No":
        pymailer2.sendmail("",toAddr,"Cams Server Alert",str("IP Address " + ipAdd + " is currently down! "),"")
        #subprocess.call(["C:\Python34\Scripts\sendemail.py",
        #                 fromAddr,
        #                 toAddr,
        #                 str("IP Address " + ipAdd + " is currently down! ")],shell= True)

#This emails every 2 hours to verify that system is up and running
tFile = "C:\Python34\Scripts\sysRunLog.log"
if not os.path.exists(tFile):
    open(tFile,"w").close()
    
timefile = open(tFile,"r+")
tf = timefile.readlines()
note = False
recTime = str(time.time())
 
for line in tf:
    timefile.close()
    os.remove(tFile)
    timefile = open(tFile,"a+")
    note = True
    timepast = (float(recTime) - float(line))
    if timepast >= 10000:
        timefile.write(recTime)
        pymailer2.sendmail("",toAddr,"Cams Server Notification",str("System is currently up and running!"),"")
        '''
        subprocess.call(["C:\Python34\Scripts\sendemail.py",
                         fromAddr,
                         toAddr,
                         str("System is currently up and running!")],shell= True)
        '''
    else:
        timefile.write(line)
    timefile.close()

if note == False:
    timefile.write(recTime)
    pymailer2.sendmail("",toAddr,"Cams Server Notification",str("System is currently up and running!"),"")
    '''
    subprocess.call(["C:\Python34\Scripts\sendemail.py",
                     fromAddr,
                     toAddr,
                     str("System is currently up and running!")],shell= True)
    '''
    timefile.close()
