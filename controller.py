import socket
from plot import *
from getloc import *
import re
import subprocess

def traceroute(domain):
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


    res = subprocess.Popen(f'traceroute {domain}', shell = True, stdout=subprocess.PIPE).stdout
    output = res.read()
    lines = output.decode().split('\n')

    # with open("test.txt",'r') as file:
    #     data = file.read().split('\n')
    #     for i in data:
    #         lines.append(i)

    # print(lines)

    ipList = []
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    for line in lines:
        # print(f"Searching in line {line}")
        res = pattern.search(line)
        # print(res)
        if(res is not None):
            addr = res.group()
            if(addr not in ipList):
                ipList.append(addr)

    return ipList


def plotMap(domain):   
    hostname = domain


    myLoc = getMyLoc()


    targetIP = socket.gethostbyname(hostname)
    targetLoc = getTargetLoc(targetIP)

    ipList = traceroute(hostname)


    routeLocList = getLoc(ipList)
    # print(routeLocList)
    routeLocList.insert(0,myLoc)
    routeLocList.append(targetLoc)


    routeLocLon =[]
    routeLocLat = []
    tempLon = 0
    tempLat = 0
    for x in routeLocList:
        if x[1][0]-tempLon == 0 or x[1][1]-tempLat == 0:
            continue
        routeLocLon.append(x[1][0])
        routeLocLat.append(x[1][1])

        tempLon = x[1][0]
        tempLat = x[1][1]



    fig = go.Figure()
    mapsInit(fig)


    for i in range(len(routeLocLon)-1):
        for x in routeLocList:
            if (routeLocLon[i],routeLocLat[i]) in x:
                route_city = x[2]
                route_ip = x[0]
        print(route_ip,'---',route_city)
        addRoute(fig,f'route{i}',((routeLocLon[i:i+2],routeLocLat[i:i+2]),route_city))
    print(targetLoc[0],'---',targetLoc[2])

    mark(fig,f'My IP - {myLoc[2]}', myLoc[1])
    mark(fig,f'{hostname} - {targetLoc[2]}',targetLoc[1],name=hostname)

    fig.show()

