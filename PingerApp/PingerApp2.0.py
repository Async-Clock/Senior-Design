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
    with open(fileName,'r') as file:
        for line in file:
            if(line[0]== '*'):
                continue
            line=line.replace('\n','')
            line=line.split(' ')
            List.append(line)
            
def createGauges(List): #Takes in an nx3 list and then creates Gauges from the list data returns a list that is nx4 as it adds the new Gauge object to each list entry
    gList=[]
    for x in range(0,len(List)):#Creates G List to keep track of buildings, used as categories to store scrapes into
        if(List[x][0] not in gList):
            gList.append(List[x][0])
            List[x].append(Gauge(List[x][0],'isUP',['method']))#Appends gauge object 
            
            
        else: # If the category is already instatiated this is run
            for z in range(0,len(List)):# Searches through list to find the guage object and appends it spot [x][3]
                if(List[x][0]==List[z][0]):
                    List[x].append(List[z][3])
                    break
    
    for x in range(0,len(List)):
        List[x][3].labels(method=List[x][1]).set(0)# calls gauge object located at[x][3] and sets to 0
    


#Instatiates Target List and fileName parameter
tList=[]
fileName='TargetList.txt'

#Reads file creates Gauges then starts the HTTP server
readTargetFile(tList,fileName)
createGauges(tList)
start_http_server(8000)


while 1: # Simple Code that loops and pings addresses inside of list
    
    
    for obj in tList:
        
        obj[3].labels(method=obj[1]).set(ping(obj[2],0.05))                          
    time.sleep(100)
