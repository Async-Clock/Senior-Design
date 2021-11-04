import os.path
import sys
import time
import random
import struct
import select
import socket
from prometheus_client import start_http_server, Summary,Gauge



def ping(addr, timeout=2, number=1, data=b''): # Pinging program accepts IP address, Timeout,Number and data, currently set to return 1 if a response is recieved
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as conn:
        payload = struct.pack('!HH', random.randrange(0, 65536), number) + data

        conn.connect((addr, 80))
        conn.sendall(b'\x08\0' + chk(b'\x08\0\0\0' + payload) + payload)
        start = time.time()

        while select.select([conn], [], [], max(0, start + timeout - time.time()))[0]:
            data = conn.recv(65536)
            if len(data) < 20 or len(data) < struct.unpack_from('!xxH', data)[0]:
                continue
            if data[20:] == b'\0\0' + chk(b'\0\0\0\0' + payload) + payload:
                #return time.time() - start
                return 1
        
        return 0       
        
def chk(data):
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return struct.pack('<H', ~x & 0xFFFF)
        

def readTargetFile(List,fileName): #Reads from configuration file and parses data into targets to pinged
    global Sleep
    with open(fileName,'r') as file:
        for line in file:
            if(line[0]== '*'):
                if(line[1]=='?'):
                    line=line.replace('\n','')
                    line.split('?')
                    Sleep=int(line[2:])
                    print(Sleep)
                continue
            line=line.replace('\n','')
            line=line.split(' ')
            List.append(line)
            
def createGauges(List): #Takes in an nx3 list and then creates Gauges from the list data returns a list that is nx4 as it adds the new Gauge object to each list entry
    gList=[]
    
    for x in range(0,len(List)):
        if(List[x][0] not in gList):
            gList.append(List[x][0])
            List[x].append(Gauge(List[x][0],'isUP',['method']))
            
            
        else:
            for z in range(0,len(List)):
                if(List[x][0]==List[z][0]):
                    List[x].append(List[z][3])
                    break
    
    for x in range(0,len(List)):
        List[x][3].labels(method=List[x][1]).set(0)
    
            

            
            
    


#Instatiates Target List and fileName parameter
tList=[]
pathname = os.path.dirname(sys.argv[0])
fileName=pathname+"\\TargetList.txt"
Sleep=100
Timeout=0.05
#Reads file creates Gauges then starts the HTTP server
readTargetFile(tList,fileName)
createGauges(tList)
start_http_server(8000)


while 1: # Simple Code that loops and pings addresses inside of list
    
    
    for obj in tList:
        pingTemp=ping(obj[2],Timeout)
        print(pingTemp)
        if(pingTemp):
            obj[3].labels(method=obj[1]).set(pingTemp)
        else:
            print("Starting Refresh pings",pingTemp)
            i=0
            while(i<3 | pingTemp != 1):
                print("Ping Failed Trying Again")
                pingTemp=ping(obj[2],Timeout)
                i=i+1
            obj[3].labels(method=obj[1]).set(pingTemp)
    print(Sleep)        
    time.sleep(Sleep)