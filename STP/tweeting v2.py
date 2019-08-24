import json
import requests
import twython
import datetime
import time
import os

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    rttapi_username,
    rttapi_password,
    nre_key
)

from twython import Twython
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

from nredarwin.webservice import DarwinLdbSession
darwin_session = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx",api_key=nre_key)

path = os.getcwd()
tlc = os.path.basename(path).upper()
out = ""
message = ""

def setTimer():
    return 60 - (datetime.datetime.now().second+datetime.datetime.now().microsecond*0.000001)

board = darwin_session.get_station_board(tlc,rows=200)

print("This program will tweet departures from",board.location_name)

while True:
    try:
        #tlc = input("Input a three letter code: ").upper()
        board = darwin_session.get_station_board(tlc,rows=200)
        #print("This program will tweet departures from",board.location_name)
        while True:
            print(str(datetime.datetime.now())+": Still Alive")
            if (datetime.datetime.now().minute)%5 == 0:
                if (datetime.datetime.now().second) == 0:
                    try:
                        if board != darwin_session.get_station_board(tlc):
                            break
                    except:
                        print(str(datetime.datetime.now())+": Get Service Info Error")
            time.sleep(setTimer())#'''

        board.all_services = []

        t = 0
        b = 0
        f = 0
        tmax = len(board.train_services)
        bmax = len(board.bus_services)
        fmax = len(board.ferry_services)
        amax = tmax + bmax + fmax

        possibleETDs = ["On time","Delayed","Cancelled"]

        if amax == 0:
            print("There are no services")
            out = "There are no services"

        if tmax != 0:
            print("There are trains")

            board.all_services.append(board.train_services[t])
            board.all_services[0].serviceType = "Train"
            t = t+1

            for i in range(t,tmax):
                for x in range(len(board.all_services)):
                    if board.train_services[i].etd in possibleETDs:
                        if board.all_services[x].etd in possibleETDs:
                            if board.train_services[i].std.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.train_services[i])
                                board.all_services[x].serviceType = "Train"
                                break
                        else:
                            if board.train_services[i].std.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.train_services[i])
                                board.all_services[x].serviceType = "Train"
                                break
                    else:
                        if board.all_services[x].etd in possibleETDs:
                            if board.train_services[i].etd.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.train_services[i])
                                board.all_services[x].serviceType = "Train"
                                break
                        else:
                            if board.train_services[i].etd.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.train_services[i])
                                board.all_services[x].serviceType = "Train"
                                break
                    if x == len(board.all_services)-1:
                        board.all_services.append(board.train_services[i])
                        board.all_services[x+1].serviceType = "Train"
                    
            
        if bmax != 0:
            print("There are busses")

            if len(board.all_services) == 0:
                board.all_services.append(board.bus_services[b])
                board.all_services[0].serviceType = "Bus"
                b = b+1

            for i in range(b,bmax):
                for x in range(len(board.all_services)):
                    if board.bus_services[i].etd in possibleETDs:
                        if board.all_services[x].etd in possibleETDs:
                            if board.bus_services[i].std.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.bus_services[i])
                                board.all_services[x].serviceType = "Bus"
                                break
                        else:
                            if board.bus_services[i].std.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.bus_services[i])
                                board.all_services[x].serviceType = "Bus"
                                break
                    else:
                        if board.all_services[x].etd in possibleETDs:
                            if board.bus_services[i].etd.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.bus_services[i])
                                board.all_services[x].serviceType = "Bus"
                                break
                        else:
                            if board.bus_services[i].etd.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.bus_services[i])
                                board.all_services[x].serviceType = "Bus"
                                break
                    if x == len(board.all_services)-1:
                        board.all_services.append(board.bus_services[i])
                        board.all_services[x+1].serviceType = "Bus"
            
        if fmax != 0:
            print("There are ferries")

            if len(board.all_services) == 0:
                board.all_services.append(board.bus_services[f])
                board.all_services[0].serviceType = "Ferry"
                f = f+1

            for i in range(f,fmax):
                for x in range(len(board.all_services)):
                    if board.ferry_services[i].etd in possibleETDs:
                        if board.all_services[x].etd in possibleETDs:
                            if board.ferry_services[i].std.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.ferry_services[i])
                                board.all_services[x].serviceType = "Ferry"
                                break
                        else:
                            if board.ferry_services[i].std.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.ferry_services[i])
                                board.all_services[x].serviceType = "Ferry"
                                break
                    else:
                        if board.all_services[x].etd in possibleETDs:
                            if board.ferry_services[i].etd.replace(':', '') < board.all_services[x].std.replace(':', ''):
                                board.all_services.insert(x,board.ferry_services[i])
                                board.all_services[x].serviceType = "Ferry"
                                break
                        else:
                            if board.ferry_services[i].etd.replace(':', '') < board.all_services[x].etd.replace(':', ''):
                                board.all_services.insert(x,board.ferry_services[i])
                                board.all_services[x].serviceType = "Ferry"
                                break
                    if x == len(board.all_services)-1:
                        board.all_services.append(board.ferry_services[i])
                        board.all_services[x+1].serviceType = "Ferry"

        services = board.all_services
        preout = ""
        print("""
-------------------------------------------------------------------------------------------------------
| SCHED | PLAT |    DUE    |                    DEST                   |           OPERATOR           |
-------------------------------------------------------------------------------------------------------""")

        for i in services:
            print("| %5s | %4s | %9s | %41s | %28s |" %(i.std, i.platform or "", i.etd,i.destination_text,i.operator_name))
        print("-------------------------------------------------------------------------------------------------------")
        
            #preout = preout + services[i].std+" "+services[i].operator_name+" "+services[i].serviceType.lower()+" to "+services[i].destination_text+" expected "+services[i].etd.lower()+"\n"
        #print(preout)

#------------------------------Ordering Complete------------------------------#
        def customOperator(i):
            if services[i].operator_name == "London North Eastern Railway":
                return "LNER"
            else:
                return services[i].operator_name

        def writeTweet(i):
            global out
            
            #out = out + services[i].std.replace(':', '') + " " + customOperator(i) + " " + services[i].serviceType.lower() + " to " + services[i].destination_text
            out = out + services[i].std.replace(':', '') + " " + services[i].serviceType.lower() + " to " + services[i].destination_text

            if services[i].etd in possibleETDs:
                out = out + ": " + services[i].etd
            else:
                out = out + ": expected " + services[i].etd.replace(':', '')
            if services[i].serviceType == "Train":
                if services[i].platform != None:
                    out = out + " - plat " + services[i].platform
            out = out + "\n"

        if out != "There are no services":
            for i in range(6):
                writeTweet(i)           
            if len(out) > 280:
                out = ""
                for i in range(5):
                    writeTweet(i)
                if len(out) > 280:
                    out = ""
                    for i in range(4):
                        writeTweet(i)
                    if len(out) > 280:
                        out = ""
                        for i in range(3):
                            writeTweet(i)

        print("\n"+out)

        if out != message:
            message = out
            try:
                twitter.update_status(status=message)
                print("-------------------------\n"+str(datetime.datetime.now())+": Tweeted:\n"+message)
            except:
                print(str(datetime.datetime.now())+": Tweet Send Error")#'''

        out = ""
        
    except:
        print("Error")
