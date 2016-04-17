import requests
import os
import re
from bs4 import BeautifulSoup

sList = []
mediaFolder = "Z:\\Shows"
showDict = {}


def main():
    getList()
    base = "https://eztv.ag"
    url = base + "/showlist/"
    fileSeason = ['s\d+e\d+', 'S\d+E\d+']

    #print(showDict)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")

    for show in soup.find_all("a"):
        for List in sList:
            gotList = []
            tmpList = List.split()
            isFound = True
            for L in tmpList:
                if show.text.find(L) < 0:
                    isFound = False

            if show.text == List or isFound == True:
                url = base + show.get("href")
                r = requests.get(url)
                newSoup = BeautifulSoup(r.content,"html.parser")

                for newShow in newSoup.find_all("a"):
                   
                    showTitle = str(newShow.get("title"))
                    exclude = str(newShow.get("href")) 
                                                      
                    if showTitle.find("Link") >= 0 and showTitle.find("x264") >= 0 and exclude.find("rarbg") == -1:
                        for rlist in fileSeason:
                            regex = re.compile(rlist)
                            rlist2 = regex.findall(showTitle)
                            for relist in rlist2:
                                if relist != "":
                                    iHaveThis = haveIt(List,relist)
                                    gotListStr = getStr(gotList)
                                    #if List == "Quantico":
                                        #print(iHaveThis,gotListStr.find(relist),relist)
                                    #print(iHaveThis, gotListStr.find(relist) >=0 )
                                    if iHaveThis or gotListStr.find(relist) >= 0:
                                        pass
                                    else:
                                        print("Getting",showTitle)
                                        gotList.append(relist)
                                        os.startfile(newShow.get("href"))

    print("Check Finished!")


def getStr(pList):
    tmpStr = ""
    for p in pList:
        if tmpStr == "":
            tmpStr = p
        else:
            tmpStr = tmpStr +  "," + p

    return tmpStr


def getList():
    tmpName = ""

    files = [f for f in os.listdir(mediaFolder)]
    for f in files:
        tmpList = []
        newFolder = mediaFolder + "\\" + f
        files2 = [f2 for f2 in os.listdir(newFolder)]
        for f2 in files2:
            tmpf2 = f2.upper()
            if tmpf2.find("SEASON") >= 0:
                newFolder2 = newFolder + "\\" + f2
                files3 = [f3 for f3 in os.listdir(newFolder2)]
                for f3 in files3:
                    tmpList.append(f3)
            else:
                tmpList.append(f2)

            showDict[f] = tmpList

        if f != "Reign" and f != "Pretty Little Liars" and f != "The Originals":
            sList.append(f)

    
def haveIt(show,episode):
    for show1 in showDict[show]:
        show1 = show1.upper()
        if show1.find(episode) >= 0:
            return True

    return False



if __name__ == "__main__":
    main()
