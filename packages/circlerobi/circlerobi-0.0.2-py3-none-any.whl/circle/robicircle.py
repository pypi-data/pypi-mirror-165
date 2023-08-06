# -*- coding: UTF-8 -*-
import requests, json, time,sys,os
global headers
from requests.structures import CaseInsensitiveDict
headers = CaseInsensitiveDict()
headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
headers["x-api-key"] = "0036c02dd0148e732398c199aed7e4cb"
headers["User-Agent"] = "gzip"
headers["Content-Type"] = "application/x-www-from-urlencoded"
headers2 = CaseInsensitiveDict()
headers2["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
headers2["User-Agent"] = "gzip"
headers2["Content-Type"] = "application/x-www-from-urlencoded"
# color value
blue = '\33[94m'
lightblue = '\033[94m'
red = '\033[91m'
white = '\33[97m'
yellow = '\33[93m'
green = '\033[1;32m'
cyan = "\033[96m"
bold = '\033[1m'
end = '\033[0m'
mark = ''' 



Sent From ARU"s System.
https://bit.ly/3PVwOXQ
'''
message = '''
Hey! I'm get my API Key From Mr. ARU's System.



Facebook: https://bit.ly/3PVwOXQ
GitHub:https://bit.ly/3Hz6Ff5
'''
cleanFolMsg = '''
Hey! I'm cleaned my follower from From Mr. ARU's System.



Facebook: https://bit.ly/3PVwOXQ
GitHub:https://bit.ly/3Hz6Ff5
'''
cleanFlgMsg = '''
Hey! I'm cleaned my follower from From Mr. ARU's System.



Facebook: https://bit.ly/3PVwOXQ
GitHub:https://bit.ly/3Hz6Ff5
'''
profileInfoMsg = '''
Hey! I'm updated my profile info from From Mr. ARU's System.



Facebook: https://bit.ly/3PVwOXQ
GitHub:https://bit.ly/3Hz6Ff5
'''


# global var
global url
url = "https://circle.robi.com.bd/mylife/appapi/appcall.php?"
# print by char
def printchar(z):
    for word in z + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(0.05)

def printcharSpeed(z):
    for word in z + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(0.00005)
# get api
# requ for otp
def requforapi(number):
    sentPinUrl = url+"op=getOTC&pin=21799&app_version=78&msisdn=88"+number
    try:
        sentOtp = requests.get(sentPinUrl, headers=headers2)
    except:
         print(bold,red+"     Error 404")
    try:
        if sentOtp.json()["rdesc"] == "OK":
            print(bold,green)
            printchar("    OTP SENT.")
            print(end)
        elif sentOtp.json()["rdesc"] == "You have send too much request":
            print(bold,red)
            printchar("    You have send too much request")
            print(end)
        else:
            print(bold,red)
            printchar("    OTP NOT SENT.")
            print(end)  
    except:
         print(bold,red + " Runtime Error")
# get api key
def getapi(otp,number):
    getApiURL = url+"op=validateOTC&pin=12345&otc="+otp+"&app_version=79&msisdn=88"+number
    try:
        getAPI = requests.get(getApiURL, headers = headers2)
    except:
        print(bold,red+"     Error 404")
    try:
        if getAPI.json()["rdesc"] == "OK":
            print(bold,cyan+"    Nickname: "+yellow, end="")
            printchar(getAPI.json()["data"]["nickname"])
            print(bold,cyan+"    API Key: "+yellow, end="" )
            printchar(getAPI.json()["data"]["mkey"])
            print(bold,cyan+"    SMS PIN: "+yellow, end="" )
            printchar(getAPI.json()["data"]["sms_pin"])
            print(end)
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+message+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
        else:
            print(bold,red+"     INVALID PIN")
    except:
        print(bold,red + " Runtime Error")
#id to number
def idtonumber(Circle_ID):
    op=url+"op=getUserInfobyNickname&nickname="+Circle_ID
    try:
        resp = requests.get(op, headers=headers)
        response=resp.json()
    except:
        print(bold,red+"     Error 404")
    try:
        if resp.json()["rdesc"] != "Not found":
            try:
                print(bold+cyan+"    Nickname: "+end+yellow+response['data']['nickname']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Number: "+end+yellow+"+"+response['data']['msisdn']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Name: "+end+yellow+response['data']['name']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Shout: "+end+yellow+response['data']['updates']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Comments: "+end+yellow+response['data']['comments']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Points: "+end+yellow+response['data']['points']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Friends: "+end+yellow+response['data']['friends']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Followings: "+end+yellow+response['data']['following']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Followers: "+end+yellow+response['data']['followers']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Gender: "+end+yellow+response['data']['gender']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Agent: "+end+yellow+response['data']['agent']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Language: "+end+yellow+response['data']['language']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Last Shout: "+end+yellow+response['data']['mlstatus']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Last Shout Time: "+end+yellow+response['data']['timestamp']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Birthday: "+end+yellow+response['data']['birthday']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Start Date : "+end+yellow+response['data']['start_date']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Start Date : "+end+yellow+response['data']['end_date']+end)
            except:
                pass
            try:
                if response['data']['type'] == "0":
                    print(bold+cyan+"    App Access : "+end+yellow+"ON"+end)
                elif response['data']['type'] == "1":
                    print(bold+cyan+"    App Access : "+end+yellow+"OFF"+end)
                else:
                    pass
            except:
                pass
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
        else:
            print(bold,red+"     Not fount")
    except:
        print(bold,red + " Runtime Error")
# Number to ID
def numbertoid(number):
    op=url+"op=getUserInfo&msisdn=88"+number
    try:
        resp = requests.get(op, headers=headers)
        response=resp.json()
    except:
        print(bold,red+"     Error 404")
    try:
        if resp.json()["rdesc"] != "Not found":
            try:
                print(bold+cyan+"    Nickname: "+end+yellow+response['data']['nickname']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Number: "+end+yellow+"+"+response['data']['msisdn']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Name: "+end+yellow+response['data']['name']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Shout: "+end+yellow+response['data']['updates']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Comments: "+end+yellow+response['data']['comments']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Points: "+end+yellow+response['data']['points']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Friends: "+end+yellow+response['data']['friends']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Followings: "+end+yellow+response['data']['following']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Followers: "+end+yellow+response['data']['followers']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Gender: "+end+yellow+response['data']['gender']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Agent: "+end+yellow+response['data']['agent']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Language: "+end+yellow+response['data']['language']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Last Shout: "+end+yellow+response['data']['mlstatus']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Last Shout Time: "+end+yellow+response['data']['timestamp']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Birthday: "+end+yellow+response['data']['birthday']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Start Date : "+end+yellow+response['data']['start_date']+end)
            except:
                pass
            try:
                print(bold+cyan+"    Start Date : "+end+yellow+response['data']['end_date']+end)
            except:
                pass
            try:
                if response['data']['type'] == "0":
                    print(bold+cyan+"    App Access : "+end+yellow+"ON"+end)
                elif response['data']['type'] == "1":
                    print(bold+cyan+"    App Access : "+end+yellow+"OFF"+end)
                else:
                    pass
            except:
                pass
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
        else:
            print(bold,red+"     Not fount")
    except:
        print(bold,red + " Runtime Error")
# api to id
def apitoid(api):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = api
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Nickname: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
        else:
            print(bold,red+"     NOT FOUND")
    except:
        print(bold,red + " Runtime Error")
# clean following
def flgclean(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getFlgListURL = url + "op=getFollowingInfoList&nickname="+user+"&limit=500"
    try:
        getFlgList = requests.get(getFlgListURL,headers=headers)
    except:
        print(bold,red + " Runtime Error")
    try:
        if getFlgList.json()["rdesc"] == "OK":
            lengthList = len(getFlgList.json()["data"]["following"])
            print(bold,cyan+"    Total Following: "+yellow, end="")
            printchar(str(lengthList))
            listFlg = []
            for i in range(lengthList):
                nickname = getFlgList.json()["data"]["following"][i]["nickname"]
                listFlg.append(nickname)
                print(bold,cyan+"    Nickname: "+end+green+getFlgList.json()["data"]["following"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getFlgList.json()["data"]["following"][i]["msisdn"])
                time.sleep(0.05)
            print(yellow)
            input("   Hit The Enter Key Clean This List ")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+cleanFlgMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
            os.system("clear")
            for clean in listFlg:
                try:
                    urlXjoin = url+"op=stopFren&nickname="+clean
                    removeUser = requests.get(urlXjoin, headers=headers)
                    time.sleep(2)
                    if removeUser.json()['rdesc'] == 'Request accepted':
                        printchar("\033[1;32m   You have left \033[96m" + clean +"'s\033[1;32m circle & will not be receiving his/her status update CSJOUT anymore.")
                    else:
                        print(bold,red + " Sorry we can't remove "+cyan+clean+red+"'s from your list")
                        time.sleep(5)
                except:
                    print(bold,red + " Runtime Error")
    except:
        print(bold,red + " Runtime Error")
# FOL Clean
def folclean(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getFolListURL = url + "op=getFollowerInfoList&nickname="+user+"&limit=100"
    try:
        getFolList = requests.get(getFolListURL,headers=headers)
    except:
        print(bold,red +" Runtime Error")
    try:
        if getFolList.json()["rdesc"] == "OK":
            lengthList = len(getFolList.json()["data"]["follower"])
            print(bold,cyan+"    Total Followers: "+yellow, end="")
            printchar(str(lengthList))
            listFol = []
            for i in range(lengthList):
                nickname = getFolList.json()["data"]["follower"][i]["nickname"]
                listFol.append(nickname)
                print(bold,cyan+"    Nickname: "+end+green+getFolList.json()["data"]["follower"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getFolList.json()["data"]["follower"][i]["msisdn"])
                time.sleep(0.05)
            input(white+"   Hit The Enter Key Clean This List ")
            input("   Hit The Enter Key Clean This List ")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+cleanFolMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
            os.system("clear")
            for clean in listFol:
                try:
                    urlXjoin = url+"op=blockUser&nickname="+clean
                    removeUser = requests.get(urlXjoin, headers=headers)
                    time.sleep(2)
                    if removeUser.json()['rdesc'] == 'OK':
                        printchar("\033[1;32m   You have successfully blocked\033[96m "+ clean)
                    elif removeUser.json()['rdesc'] == 'Already blocked':
                        printchar("\033[96m   You have Already blocked \033[1;32m" + clean)
                    else:
                        print(bold,red + " Sorry we can't remove "+clean+"'s from your list")
                        print(removeUser.json())
                        time.sleep(5)
                except:
                    print(bold,red = " Runtime Error")
    except:
        print(bold,red + " Runtime Error")
# flg check
def flgcheck(CircleID):
    getFlgListURL = url + "op=getFollowingInfoList&nickname="+CircleID+"&limit=500"
    try:
        getFlgList = requests.get(getFlgListURL,headers=headers)
    except:
        print(bold,red + " Runtime Error")
    try:
        if getFlgList.json()["rdesc"] == "OK":
            lengthList = len(getFlgList.json()["data"]["following"])
            print(bold,cyan+"    Total Following: "+yellow, end="")
            printchar(str(lengthList))
            listFlg = []
            for i in range(lengthList):
                nickname = getFlgList.json()["data"]["following"][i]["nickname"]
                listFlg.append(nickname)
                print(bold,cyan+"    Nickname: "+end+green+getFlgList.json()["data"]["following"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getFlgList.json()["data"]["following"][i]["msisdn"])
                time.sleep(0.05)
    except:
        print(bold,red + " Runtime Error")
# fol check
def folcheck(CircleID):
    getFolListURL = url + "op=getFollowerInfoList&nickname="+CircleID+"&limit=100"
    try:
        getFolList = requests.get(getFolListURL,headers=headers)
    except:
        print(bold,red = " Error 404")
    try:
        if getFolList.json()["rdesc"] == "OK":
            lengthList = len(getFolList.json()["data"]["follower"])
            print(bold,cyan+"    Total Followers: "+yellow, end="")
            printchar(str(lengthList))
            for i in range(lengthList):
                nickname = getFolList.json()["data"]["follower"][i]["nickname"]
                print(bold,cyan+"    Nickname: "+end+green+getFolList.json()["data"]["follower"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getFolList.json()["data"]["follower"][i]["msisdn"])
                time.sleep(0.05)
    except:
        print(bold,red + " Runtime Error")
# block check
def blockcheck(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getBlockListUrl = url + "op=getBlockedUserInfoList"
    try:
        getBlockList = requests.get(getBlockListUrl,headers=headers)
    except:
        print(bold,red + " Error 404")
    try:
        if getBlockList.json()["rdesc"] == "OK":
            lengthList = len(getBlockList.json()["data"]["list"])
            print(bold,cyan+"    Total Blocked: "+yellow, end="")
            printchar(str(lengthList))
            for i in range(lengthList):
                print(bold,cyan+"    Nickname: "+end+green+getBlockList.json()["data"]["list"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getBlockList.json()["data"]["list"][i]["msisdn"])
                time.sleep(0.05)
    except:
        print(bold,red +" Runtime Error")
# clean block
def blockclean(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getBlockListUrl = url + "op=getBlockedUserInfoList"
    try:
        getBlockList = requests.get(getBlockListUrl,headers=headers)
    except:
        print(bold,red + " Error 404")
    listBlock = []
    try:
        if getBlockList.json()["rdesc"] == "OK":
            try:
                lengthList = len(getBlockList.json()["data"]["list"])
                if lengthList != "0":
                    pass
                else:
                    print(bold,red = " Blocked Users Not Found")
                    sys.exit()
                print(bold,cyan+"    Total Blocked: "+yellow, end="")
                printchar(str(lengthList))
                for i in range(lengthList):
                    nickname = getBlockList.json()["data"]["list"][i]["nickname"]
                    listBlock.append(nickname)
                    print(bold,cyan+"    Nickname: "+end+green+getBlockList.json()["data"]["list"][i]["nickname"]+bold,cyan+"   Number: "+end+green+"+"+getBlockList.json()["data"]["list"][i]["msisdn"])
                    time.sleep(0.05)
            except:
                print(bold,red = " Blocked Users Not Found")
                sys.exit()
            print(yellow)
            input("   Hit The Enter Key Clean This List ")
            os.system("clear")
            for clean in listBlock:
                try:
                    urlXBlock = url+"op=unblockUser&nickname="+clean
                    removeUser = requests.get(urlXBlock, headers=headers)
                    time.sleep(2)
                    if removeUser.json()['rdesc'] == 'OK':
                        print(bold,green, end="")
                        printchar("\033[1;32m   You have successfully unblocked \33[93m" + clean)
                    else:
                        print(bold,red + " Sorry we can't remove "+clean+"'s from your list")
                        time.sleep(5)
                except:
                    print(bold,red +" Runtime Error")
    except:
        print(bold,red + " Runtime Error")
# clean not in your circle users
def notin(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getFlgListURL = url + "op=getFollowingInfoList&nickname="+user+"&limit=500"
    getFolListURL = url + "op=getFollowerInfoList&nickname="+user+"&limit=100"
    
    try:
        getFlgList = requests.get(getFlgListURL,headers=headers)
        time.sleep(1)
        getFolList = requests.get(getFolListURL,headers=headers)
        if getFlgList.json()["rdesc"] == "OK" and getFolList.json()["rdesc"] == "OK" :
            listFollowings = []
            notInList=[]
            lengthFollowing = len(getFlgList.json()["data"]["following"])
            for i in range(lengthFollowing):
                nick = getFlgList.json()["data"]["following"][i]["nickname"]
                listFollowings.append(nick)
            lengthFollower = len(getFolList.json()["data"]["follower"])
            for i in range(lengthFollower):
                nickname = getFolList.json()["data"]["follower"][i]["nickname"]
                if nickname not in listFollowings:
                    print("\033[1m   \33[93m Your are not in \033[96m"+nickname+"'s\33[93m CIRCLE.")
                    notInList.append(nickname)
                    time.sleep(0.05)
            print(yellow)
            input("   Hit The Enter Key Clean This List ")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+cleanFlgMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
            os.system("clear")
            try:
                for nickname in notInList:
                    joinURL = url + 'op=sendFren&nickname='+nickname
                    join = requests.get(joinURL, headers=headers)
                    if join.json()["rdesc"] == "Request accepted" :
                        printchar("\033[1m   \033[1;32m You and \033[96m"+ nickname +"\033[1;32m are now joined each other circle.")
                    else:
                        print(bold,red + " Runtime Error")
            except:
                print(bold,red +" Runtime Error")
    except:
        print(bold,red +" Runtime Error")
# clean not in your circle users
def notinyour(ApiKey):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = ApiKey
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            user = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    getFlgListURL = url + "op=getFollowingInfoList&nickname="+user+"&limit=500"
    getFolListURL = url + "op=getFollowerInfoList&nickname="+user+"&limit=500"
    try:
        getFlgList = requests.get(getFlgListURL,headers=headers)
        time.sleep(1)
        getFolList = requests.get(getFolListURL,headers=headers)
        if getFlgList.json()["rdesc"] == "OK" and getFolList.json()["rdesc"] == "OK" :
            listFollowers = []
            notInList=[]
            lengthFollower = len(getFolList.json()["data"]["follower"])
            for i in range(lengthFollower):
                nick = getFolList.json()["data"]["follower"][i]["nickname"]
                listFollowers.append(nick)
            lengthFollowing = len(getFlgList.json()["data"]["following"])
            for i in range(lengthFollowing):
                nickname = getFlgList.json()["data"]["following"][i]["nickname"]
                if nickname not in listFollowers:
                    print("\033[1m   \033[96m"+nickname+"\33[93m is not in your circle. ")
                    notInList.append(nickname)
                    time.sleep(0.05)
            print(white)
            input("   Hit The Enter Key Xjoin all users "+end)
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+cleanFlgMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
            os.system("clear")
            try:
                for nickname in notInList:
                    joinURL = url + 'op=stopFren&nickname='+nickname
                    join = requests.get(joinURL, headers=headers)
                    if join.json()["rdesc"] == "Request accepted" :
                        printchar("\033[1;32m   You have left \033[96m" + nickname +"'s\033[1;32m circle & will not be receiving his/her status update CSJOUT anymore.")
                    else:
                        print(bold,red + " Runtime Error")
            except:
                print(bold,red + " Runtime Error")
    except:
        print(bold,red + " Runtime Error")
# OwnPin
def ownPIN(apiKEY):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = apiKEY
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            nickname =getInfo.json()["data"]["nickname"]
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(nickname)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")

    join = url + "op=stopFren&nickname="+nickname
    try:
        while True:
            requ = requests.get(join,headers=headers)
            time.sleep(0.00005)
            print(requ.json())
    except:
        print(bold,red + " Runtime Error")
#  auto cp
def autoCp(yourAPI,circleID,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Sent To: "+yellow, end="")
            printchar(circleID)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    cpURL = url + "op=performAction&app_version=78&nickname="+circleID+"&action=poke&msgId=974&imei=355176100126264&imsi=470022500179917&msisd&message="+message+mark+"&retry=false&operator=Robi"
    try:
        requ = requests.get(cpURL , headers = headers)
        if requ.json()['rdesc'] == 'Request accepted':
            printchar("\n\033[1m \033[1;32m   Cpoke sent successfully \033[0m")
        else:
            print (bold,red)
            printchar("    copoke not sent")
            print("    Reason: "+requ.json()['rdesc'])
    except:
        print(bold,red + " Error 404")
#  auto cp nonstop
def NonStopAutoCp(yourAPI,circleID,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Sent To: "+yellow, end="")
            printchar(circleID)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
            sys.exit()
    except:
        print(bold,red + " Runtime Error")
    cpURL = url + "op=performAction&app_version=78&nickname="+circleID+"&action=poke&msgId=974&imei=355176100126264&imsi=470022500179917&msisd&message="+message+mark+"&retry=false&operator=Robi"
    try:
        while True:
            requ = requests.get(cpURL , headers = headers)
            time.sleep(1)
            if requ.json()['rdesc'] == 'Request accepted':
                printchar("\n\033[1m \033[1;32m   Cpoke sent successfully \033[0m")
            else:
                print (bold,red)
                printchar("    copoke not sent")
                print("    Reason: "+requ.json()['rdesc'])
                continue
    except:
        print(bold,red + " Error 404")
#  auto cm
def autoCom(yourAPI,circleID,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Sent To: "+yellow, end="")
            printchar(circleID)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")

    cmURL = url + "op=performAction&app_version=78&nickname="+circleID+"&action=kom&msgId=974&imei=355176100126264&imsi=470022500179917&msisd&message="+message+mark+"&retry=false&operator=Robi"
    try:
        requ = requests.get(cmURL , headers = headers)
        if requ.json()['rdesc'] == 'Request accepted':
            printchar("\n\033[1m \033[1;32m    Ccom sent successfully \033[0m")
        else:
            print (bold,red)
            printchar("    ccom not sent")
            print("    Reason: "+requ.json()['rdesc'])
    except:
        print(bold,red + " Error 404")
#  auto com nonstop
def NonStopAutoCom(yourAPI,circleID,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Sent To: "+yellow, end="")
            printchar(circleID)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
            sys.exit()
    except:
        print(bold,red + " Runtime Error")
    comURL = url + "op=performAction&app_version=78&nickname="+circleID+"&action=kom&msgId=974&imei=355176100126264&imsi=470022500179917&msisd&message="+message+mark+"&retry=false&operator=Robi"
    try:
        while True:
            requ = requests.get(comURL , headers = headers)
            time.sleep(1)
            if requ.json()['rdesc'] == 'Request accepted':
                printchar("\n\033[1m \033[1;32m   Ccom sent successfully \033[0m")
            else:
                print (bold,red)
                printchar("     ccom not sent")
                print("    Reason: "+requ.json()['rdesc'])
                continue
    except:
        print(bold,red +" Error 404")
#  auto shout
def autoShout(yourAPI,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        getPtURL = url + "op=getUserInfobyNickname&nickname="+getInfo.json()["data"]["nickname"]
        getPT = requests.get(getPtURL, headers=headers)
        points = getPT.json()["data"]["points"]
        followerTotal = getPT.json()['data']['followers']
    except:
        print(bold,red+"    Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Your Points: "+yellow, end="")
            printchar(points)
            print(bold,cyan+"    Your Total Followers: "+yellow, end="")
            print(followerTotal)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+message+mark+"&retry=false"
    try:
        requ = requests.get(shoutURL , headers = headers)
        if requ.json()['rdesc'] == 'Request accepted':
            printchar("\n\033[1m \033[1;32m    CSHOUT is processing sent to your \033[96m"+followerTotal+ "\033[1;32m followers in CIRCLE. \033[0m")
        else:
            print (bold,red)
            printchar("     CSHOUT not sent.")
            print("     Reason: "+requ.json()['rdesc'])
    except:
        print(bold,red +" Error 404")
#auto shout nonstop
def NonStopAutoShout(yourAPI,message):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        getPtURL = url + "op=getUserInfobyNickname&nickname="+getInfo.json()["data"]["nickname"]
        getPT = requests.get(getPtURL, headers=headers)
        points = getPT.json()["data"]["points"]
        followerTotal = getPT.json()['data']['followers']
    except:
        print(bold,red+"    Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Your Points: "+yellow, end="")
            printchar(points)
            print(bold,cyan+"    Your Total Followers: "+yellow, end="")
            print(followerTotal)
            print(bold,cyan+"    Your Message: "+yellow, end="")
            printchar(message)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+message+mark+"&retry=false"
    try:
        while True:
            requ = requests.get(shoutURL , headers = headers)
            if requ.json()['rdesc'] == 'Request accepted':
                printchar("\n\033[1m \033[1;32m    CSHOUT is processing sent to your \033[96m"+followerTotal+ "\033[1;32m followers in CIRCLE. \033[0m")
            else:
                print (bold,red)
                printchar("     CSHOUT not sent.")
                print("     Reason: "+requ.json()['rdesc'])
    except:
        print(bold,red + " Error 404")
# gender change 
def gender(yourAPI, gender):
    gender = gender.upper()
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        getPtURL = url + "op=getUserInfobyNickname&nickname="+getInfo.json()["data"]["nickname"]
        getPT = requests.get(getPtURL, headers=headers)
        genderUSER = getPT.json()["data"]["gender"]
    except:
        print(bold,red+"    Error 404")

    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Your current Gender: "+yellow, end="")
            printchar(genderUSER)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    genChangeURL = url + "op=setUserInfo&gender="+gender
    try:
        change = requests.get(genChangeURL, headers=headers)
        resp = change.json()["rdesc"]
        if resp == "OK":
            print(bold,green+"    Your GENDER "+yellow +genderUSER + green +" to " +yellow+ gender+green+ " Changed")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+profileInfoMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
        else:
            print(bold,red + "    Runtime Error")
    except:
        print(bold,red + "    Runtime Error")
# name
def name(yourAPI, name):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        getPtURL = url + "op=getUserInfobyNickname&nickname="+getInfo.json()["data"]["nickname"]
        getPT = requests.get(getPtURL, headers=headers)
        nameUSER = getPT.json()["data"]["name"]
    except:
        print(bold,red+"    Error 404")

    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Your current Name: "+yellow, end="")
            printchar(nameUSER)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    genChangeURL = url + "op=setUserInfo&name="+name
    try:
        change = requests.get(genChangeURL, headers=headers)
        resp = change.json()["rdesc"]
        if resp == "OK":
            print(bold,green+"    Your Name "+yellow +nameUSER + green +" to " +yellow+ name +green+ " Changed")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+profileInfoMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
        else:
            print(bold,red + "    Runtime Error")
    except:
        print(bold,red + "    Runtime Error")
# birthday
def birthday(yourAPI, birthday):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        getPtURL = url + "op=getUserInfobyNickname&nickname="+getInfo.json()["data"]["nickname"]
        getPT = requests.get(getPtURL, headers=headers)
        birthdayUSER = getPT.json()["data"]["birthday"]
    except:
        print(bold,red+"    Error 404")

    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            print(bold,cyan+"    Your current Birthday: "+yellow, end="")
            printchar(birthdayUSER)
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    genChangeURL = url + "op=setUserInfo&birthday="+birthday
    try:
        change = requests.get(genChangeURL, headers=headers)
        resp = change.json()["rdesc"]
        if resp == "OK":
            print(bold,green+"    Your Birthday "+yellow +birthdayUSER + green +" to " +yellow+ birthday + " 00:00:00" +green+ " Changed")
            shoutURL = url + "op=performAction&app_version=81&action=kast&msgId=62&msisdn=8801875409158&message="+profileInfoMsg+"&retry=false"
            try:
                sentAdd = requests.get(shoutURL, headers=headers)
            except:
                pass
        else:
            print(bold,red + "    Runtime Error")
    except:
        print(bold,red + "    Runtime Error")
# cstop
def cstop(yourAPI):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    stopURL = url + "op=setUserMode&mode=stop"
    try:
        change = requests.get(stopURL, headers=headers)
        resp = change.json()["rdesc"]
        if resp == "OK":
            printchar("\033[1m \033[96m    You have exited CIRCLE. To enter again, send CREG to 28880. Your nickname, friends and Points will expire in 150 days.\033[0m")
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
        else:
            print(bold,red + "    Runtime Error")
    except:
        print(bold,red + "    Runtime Error")
# creg
def creg(yourAPI):
    urlInfoGet = url + "op=getNickname"
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["x-app-key"] = "000oc0so48owkw4s0wwo4c00g00804w80gwkw8kg"
    headers["x-api-key"] = yourAPI
    headers["User-Agent"] = "gzip"
    headers["Content-Type"] = "application/x-www-from-urlencoded"
    try:
        getInfo = requests.get(urlInfoGet, headers = headers)
    except:
        print(bold,red+"     Error 404")
    try:
        if getInfo.json()["rdesc"] == "OK":
            print(bold,cyan+"    Your CIRCLE ID: "+yellow, end="")
            printchar(getInfo.json()["data"]["nickname"])
            nickname = getInfo.json()["data"]["nickname"]
        else:
            print(bold,red+"     API INVALID.")
    except:
        print(bold,red + " Runtime Error")
    stopURL = url + "op=setUserMode&mode=online"
    try:
        change = requests.get(stopURL, headers=headers)
        resp = change.json()["rdesc"]
        if resp == "OK":
            printchar("\033[1m \033[96m    Welcome back! Your profile \33[93m"+ nickname + "\033[96m still exists in CIRCLE and has been reactivated.\033[0m")
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
        else:
            print(bold,red + "    Runtime Error")
    except:
        print(bold,red + "    Runtime Error")
# showLatest Update in app
def updateInapp():
    urlUpdate = url + "op=getLatestBommList"
    try:
        getData = requests.get(urlUpdate, headers=headers)
        if getData.json()["rdesc"] == "OK":
            lengthData = len(getData.json()["data"]["mlstatus_item"])
            for i in range(lengthData):
                print(green+"    Nickname: "+cyan+getData.json()["data"]["mlstatus_item"][i]["nickname"]+green + "  Number: "+cyan+ "+"+ getData.json()["data"]["mlstatus_item"][i]['msisdn'])
                printcharSpeed("\033[1;32m    Status: \33[93m"+getData.json()["data"]["mlstatus_item"][i]['mlstatus'])
                print("\n")
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
    except:
        print(bold,red+"     Error 404")
# showLatest Update in app
def updateUser(circleID):
    urlUpdate = url + "op=getMLStatusList&nickname="+circleID
    try:
        getData = requests.get(urlUpdate, headers=headers)
        print(getData.json())
        if getData.json()["rdesc"] == "OK":
            lengthData = len(getData.json()["data"])
            print(getData.text)
            for i in range(lengthData):
                printcharSpeed("\033[1;32m    Status: \33[93m"+getData.json()["data"][i]['st'])
                print("\n")
            try:
                print("\n\n")
                printchar("\033[1m \033[96m   Made With ❤️   by \33[97m ARU   \033[0m   ")
                print("\n\n")
            except:
                pass
    except:
        print(bold,red+"     Error 404")