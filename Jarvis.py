__author__ = 'TerryP'

'''
List of things to do:
    - if python34 folder not avail then write to random spot on c:
    - verify initial user/admin setup
    - write in an edit of user password
    - fix defrag option and SFC
    - finish itunes options
    - keep music album covers from being moved into images folder... look at base folder, if can find that name in music folder don't copy
'''

import os
import webbrowser
import time as t
import re
import shutil
import urllib
# import sys
import subprocess
import stagger

# define variables
fileName = "JARVIS-master.txt"
fileBase = "C:\\Python34"
fileHome = "C:\\Python34\\Documents"
verified = ""
userName = ""
password = ""
tmpPassword = ""
tmpUserName = ""
cType = ""
cLocation = ""
userVerified = ""
cName = ""
cAvailTasks = ["Add Multimedia to Server", "Open Web Browser", "Perform System Maintenance", "Itunes Duplicate Remover",
               "Itunes New Album Checker"]


class NewFile():
    def __init__(self, cName):
        self.name = cName
        self.baselevel = False
        self.hasseason = False
        self.root = ""
        self.seasonnum = 0
        self.type = ""
        self.path = ""
        self.l1 = ""
        self.moveto = ""
        self.ext = ""
        self.tagartist = ""
        self.tagalbum = ""
        self.tagdate = ""
        self.tagtrack = ""


class NewFolder():
    def __init__(self, cName, cPath, cBase):
        self.name = cName
        self.path = cPath
        self.base = cBase


# check usernames and passwords
def readFile(cType, cUser, cPassword, tmpFile):
    tmpCheck = False
    tmpCnt = 0
    tmpReturn = ""
    sortFolder = ""
    mediaFolder = ""

    if not os.path.exists(tmpFile):
        open(tmpFile, "w").close()

    if cType == "verifyUser":
        tFile = open(tmpFile, "r")
        for lines in tFile.readlines():
            if tmpReturn == "":
                if lines.find("U:") >= 0:
                    userName = lines.replace("U:", "")
                    userName = userName.strip()
                    password = ""
                elif lines.find("P:") >= 0:
                    password = lines.replace("P:", "")
                    password = password.strip()

                if userName != "" and password != "":
                    if userName == cUser and password == cPassword:
                        tmpReturn = "Valid"

    elif cType == "createAdmin":
        tFile = open(tmpFile, "a")
        # tFile.write("\n")
        tFile.write("U:Admin" + "\n")
        tFile.write("P:" + str(input("Enter Admin Password: ")) + "\n")
        tFile.close()

    elif cType == "addUser":
        tFile = open(tmpFile, "r")
        cPassword = input("Enter admin password to add new user: ")
        tmpReturn = ""
        for lines in tFile.readlines():
            if tmpReturn == "":
                if lines.find("U:") >= 0:
                    userName = lines.replace("U:", "")
                    userName = userName.strip()
                    password = ""
                elif lines.find("P:") >= 0:
                    password = lines.replace("P:", "")
                    password = password.strip()

                if userName == "Admin" and password != "":
                    tmpReturn = "foundAdmin"
                    tmpCnt = 0
                    while tmpCnt <= 3 and tmpReturn != "Valid":
                        tmpCnt += 1
                        if password == cPassword:
                            tmpReturn = "Valid"
                        else:
                            cPassword = input("Incorrect... please enter Admin password: ")
        tFile.close()

        if tmpReturn == "Valid":
            tFile = open(tmpFile, "a")
            tFile.write("\n")
            tFile.write("U:" + cUser)
            while tmpCheck == False:
                cPassword = input("Enter password: ")
                if cPassword == input("ReType password: "):
                    tmpCheck = True
                    tFile.write("\n")
                    tFile.write("P:" + cPassword)
            tFile.close()
        else:
            print("Add of new user failed... ")

    elif cType == "Sorter":
        tFile = open(tmpFile, "r")
        tmpReturn = ""
        for lines in tFile.readlines():
            if lines.find("sortFolder:") >= 0:
                sortFolder = lines.replace("sortFolder:", "")
                sortFolder = sortFolder.strip()
            elif lines.find("mediaFolder:") >= 0:
                mediaFolder = lines.replace("mediaFolder:", "")
                mediaFolder = mediaFolder.strip()

        if sortFolder != "" and mediaFolder != "":
            # begin moving files
            fileSorter(sortFolder, mediaFolder)
        else:
            tFile.close()
            tFile = open(tmpFile, "a")
            tFile.write("\n\n")
            sortFolder = input("Please enter location of unsorted media folder: ")
            tFile.write("sortFolder:" + sortFolder)
            tFile.write("\n")
            mediaFolder = input("Please enter location of server media folder: ")
            tFile.write("mediaFolder:" + mediaFolder)
            tFile.close()
            # now begin moving files
            fileSorter(sortFolder, mediaFolder)

    if tmpReturn == "Valid":
        return "Valid"


def fileSorter(fromLocation, toLocation):
    name = ""
    videoFileExt = (".mp4", ".avi", ".mkv")
    musicFileExt = (".mp3")
    imageFileExt = (".pdf", ".jpg", ".tif", ".gif", ".jpeg", ".bmp", ".png", ".svg")
    date = t.localtime(t.time())
    dateFormated = '%d_%d_%d' % (date[1], date[2], date[0] % 100)
    report = os.environ['USERPROFILE'] + "\Desktop" + "\\" + dateFormated + "_mediaSortReport.txt"
    fileSeason = ['s\d+e\d+', 'S\d+E\d+']
    list2 = []

    # create the report file
    readFile("", "", "", report)

    # search for each type folder(ex.pictures,movies,shows,music, etc)
    for root, dirs, files in os.walk(toLocation):
        for name in dirs:
            '''
            could write this to set folders and names based off of where the, for example, .mp4 files are located... so
            if those file types were found in "blah blah" then the movieFolder name would be "blah blah
            '''
            if name.upper() == "MOVIES":
                movieFolder = NewFolder(name, os.path.join(root, name), toLocation)
            elif name.upper() == "SHOWS":
                showFolder = NewFolder(name, os.path.join(root, name), toLocation)
            elif name.upper() == "MUSIC":
                musicFolder = NewFolder(name, os.path.join(root, name), toLocation)
            elif name.upper() == "PICTURES":
                picFolder = NewFolder(name, os.path.join(root, name), toLocation)

    sReport = open(report, "a")
    sReport.write("Sort Report for " + dateFormated + "\n")
    sReport.write("This report show what files were sorted and their new location.")
    for root, dirs, files in os.walk(fromLocation):
        for name in files:
            # get name and init
            sFile = NewFile(name)
            sFile.root = root
            sFile.path = os.path.join(root, name)
            if sFile.root != fromLocation:
                sFile.baselevel = False

            # set the type of file
            if sFile.name.endswith(videoFileExt):
                sFile.type = "video"
            elif sFile.name.endswith(musicFileExt):
                sFile.type = "music"
            elif sFile.name.endswith(imageFileExt):
                sFile.type = "image"
            else:
                sFile.type = "NA"

            if sFile.type == "video":
                # only care about season info if its a video
                for list in fileSeason:
                    regex = re.compile(list)
                    list2 = regex.findall(name)
                    for l in list2:
                        if l != "":
                            sFile.l1 = l
                            sFile.hasseason = True
                            if len(sFile.l1) == 6:
                                sFile.seasonnum = int(sFile.l1[1:3])
                            if len(sFile.l1) == 4:
                                sFile.seasonnum = int(sFile.l1[1:2])

            if sFile.type == "video":
                if sFile.hasseason == True:
                    # shows
                    # find Show Folder
                    tmpPath = findFolder("folder", sFile.name, showFolder.path, str(sFile.seasonnum))
                    if sFile.seasonnum != 0:
                        # find season Folder
                        tmpPath = findFolder("season", str(sFile.seasonnum), tmpPath, str(sFile.seasonnum))
                    sFile.moveto = tmpPath
                else:
                    # Movies
                    sFile.moveto = movieFolder.path
            elif sFile.type == "image":
                sFile.moveto = picFolder.path
            elif sFile.type == "music":
                tmpPath = ""
                audiofile = stagger.read_tag(sFile.path)
                tmpPath = findFolder("folder", audiofile.artist, musicFolder.path,"")
                tmpPath = findFolder("folder", audiofile.album, tmpPath,"")
                sFile.moveto = tmpPath
            if sFile.moveto != "":
                sReport.write("\n")
                sReport.write("File " + sFile.path + " was moved to " + sFile.moveto + "\\" + sFile.name)

                if not os.path.exists(sFile.moveto + "\\" + sFile.name):
                    shutil.copy(sFile.path, sFile.moveto + "\\" + sFile.name)

    sReport.close()


'''
def getExt(cFile):
    cExt    = ""
    cExtLoc = 0
'''


def findFolder(cType, tmpchar1, tmpchar2, tmpchar3):
    tmpFolder = ""
    tmpFolderName = tmpchar1.upper()
    tmpFolderPos = 0

    if cType == "folder":
        tmpFolderName = tmpFolderName.replace(".", " ")
        if tmpFolderName.find("S0" + tmpchar3) >= 0:
            tmpFolderPos = tmpFolderName.find("S0" + tmpchar3)
            tmpFolderName = tmpFolderName[0:tmpFolderPos]
        elif tmpFolderName.find("S" + tmpchar3) >= 0:
            tmpFolderPos = tmpFolderName.find("S" + tmpchar3)
            tmpFolderName = tmpFolderName[0:tmpFolderPos]
        if tmpFolderName.find(".") >= 0:
            tmpFolderPos = tmpFolderName.find("." + tmpchar3)
            tmpFolderName = tmpFolderName[0:tmpFolderPos]
        tmpFolderName = tmpFolderName.strip()

    elif cType == "season":
        tmpFolderName = "Season " + tmpchar3

    if cType == "folder" or cType == "season":
        dirs2 = os.listdir(tmpchar2)  # showFolder.path
        for name2 in dirs2:
            if tmpFolder == "":
                tmpName = name2.upper()
                tmpName = tmpName.replace(" ", "")
                # used 6 characters b/c didn't want the season and episode info in there
                tmpName2 = tmpchar1.upper()[0:6]
                if tmpName.find(tmpName2) >= 0:
                    tmpFolder = str(tmpchar2 + "\\" + name2)

        if tmpFolder == "":
            createFolder(tmpchar2 + "\\" + tmpFolderName)
            tmpFolder = tmpchar2 + "\\" + tmpFolderName
        return tmpFolder


def createFolder(cPath):
    if not os.path.exists(cPath):
        try:
            os.makedirs(cPath)
        except OSError:
            print("There was an error creating folder")
            pass


# User enters username and password then we varify with readFile
def verifyUser():
    varified = ""
    while not varified == "Valid" and not varified == "Bailout":
        varified = ""
        tmpUserName = input("Enter Username/Exit: ")
        if tmpUserName.upper() == "EXIT":
            varified = "Bailout"
        elif tmpUserName != "":
            tmpPassword = input("Enter Password: ")
            varified = readFile("verifyUser", tmpUserName, tmpPassword, recordFile)
            if not varified == "Valid":
                tmpStr = input(
                    "Username " + tmpUserName + " does not exist. Whould you like to create this user?... Yes/No? ")
                if tmpStr.upper() == "YES":
                    varified = readFile("addUser", tmpUserName, tmpPassword, recordFile)
        if varified == "Valid":
            print("Welcome " + tmpUserName + "!")

    return varified


def defrag():
    dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]

    #only on mounted drives... not network mapped drives
    for d in drives:
        return_code = subprocess.call("fsutil fsinfo drivetype " + d)
        if return_code == 0:
            response = str(subprocess.check_output("fsutil fsinfo drivetype " + d))
            if response.find("Fixed") >= 0:
                cmd = "defrag " + d + " /U"
                try:
                    subprocess.run(cmd)
                except OSError:
                    print("defrag of " + d + " failed")


def runTask(tmpTask):
    if tmpTask == "Add Multimedia to Server":
        tmpVar = readFile("Sorter", "", "", recordFile)
    elif tmpTask == "Open Web Browser":
        webbrowser.open("www.google.com")
        '''
        with urllib.request.urlopen("http://www.espn.com") as response:
            html = response.read()
            print(html)
        '''
    elif tmpTask == "Perform System Maintenance":
        userResponse = input("Run system cleanup?... yes/no: ")
        if userResponse.upper() == "YES":
            subprocess.run("cleanmgr")
        userResponse = input("Run defrag of local drives?... yes/no: ")
        if userResponse.upper() == "YES":
            defrag()
        userResponse = input("Check system files?... yes/no: ")
        if userResponse.upper() == "YES":
            subprocess.run("sfc /scannow")

    else:
        print("Could not complete that task... Contact Admin!")


'''
*******MAIN*******
'''

# make sure homefolder exists
if not os.path.exists(fileBase):
    os.mkdir(fileBase)
if not os.path.exists(fileHome):
    os.mkdir(fileHome)

recordFile = fileHome + "\\" + fileName
#if file/folder existed then verify user else assume initial setup
if os.path.exists(recordFile):
    userVerified = verifyUser()
else:
    print("No users found...creating one now!")
    #user = createUser()
    userVerified = readFile("createAdmin","","",recordFile)

'''
#need to uncomment this when live so can validate user also comment userverified = "valid" below
'''

userVerified = "Valid"
if userVerified == "Valid":
    bailout = False
    tmpCnt = 0
    while bailout == False:
        # display avail tasks
        if tmpCnt > 0:
            print("\n")
        for lines in cAvailTasks:
            print(str(cAvailTasks.index(lines)) + ". " + lines)

        tmpCnt += 1
        print("\n")
        selectTask = input("Enter number of ask you want to run: ")
        if selectTask.upper() == "EXIT":
            bailout = True
        else:
            selectTask = cAvailTasks[int(selectTask)]
            runTask(selectTask)


else:
    exit()

'''
*****END MAIN*****
'''
