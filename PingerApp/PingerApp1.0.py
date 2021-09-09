import time
import random
import struct
import select
import socket
from prometheus_client import start_http_server, Summary,Gauge

class pingTarget:
    def __init__(self,name='',IP='',isUP=0):
        self.name=name
        self.IP=IP
        self.isUp=isUP
        
def ping(addr, timeout=2, number=1, data=b''):
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
        
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


Targets=[]
Targets.append( pingTarget('EngineeringPS', '10.2.5.2',0))
Targets.append( pingTarget('EngineeringLTE', '10.2.5.1',0))
Targets.append( pingTarget('EngineeringMR', '10.2.5.3',0))
Targets.append( pingTarget('MorrisPS', '10.2.5.5',0))
Targets.append( pingTarget('MorrisLTE', '10.2.5.4',0))
Targets.append( pingTarget('MorrisMR', '10.2.5.6',0))
Targets.append( pingTarget('PowerPlantPS', '10.3.5.8',0))
Targets.append( pingTarget('PowerPlantLTE', '10.2.5.7',0))
Targets.append( pingTarget('PowerPlantMR1', '10.2.5.9',0))
Targets.append( pingTarget('PowerPlantMR2', '10.2.5.10',0))
Targets.append( pingTarget('PowerPlantMR3', '10.2.5.11',0))
Targets.append( pingTarget('RecreationPS','10.2.5.13',0))
Targets.append( pingTarget('RecreationLTE','10.2.5.12',0))
Targets.append( pingTarget('RecreationMR','10.2.5.14',0))
Targets.append( pingTarget('TrueBloodLTE', '10.2.5.17',0))



# Start up the server to expose the metrics.
start_http_server(8000)
Eng=Gauge('Engineering', 'isUP', ['method'])
Eng.labels(method='PS').set(0)
Eng.labels(method='LTE').set(0)
Eng.labels(method='MR').set(0)

Mor=Gauge('Morris', 'isUP', ['method'])
Mor.labels(method='PS').set(0)
Mor.labels(method='LTE').set(0)
Mor.labels(method='MR').set(0)

Pow=Gauge('PowerPlant', 'isUP', ['method'])
Pow.labels(method='PS').set(0)
Pow.labels(method='LTE').set(0)
Pow.labels(method='MR1').set(0)
Pow.labels(method='MR2').set(0)
Pow.labels(method='MR3').set(0)

Rec=Gauge('Recreation', 'isUP', ['method'])
Rec.labels(method='PS').set(0)
Rec.labels(method='LTE').set(0)
Rec.labels(method='MR').set(0)

Blo=Gauge('TrueBlood', 'isUP', ['method'])
Blo.labels(method='PS').set(0)
#Blo.labels(method='LTE').set(0)
#Blo.labels(method='MR').set(0)





while(1):

    
    Eng.labels(method='PS').set(ping(Targets[0].IP,0.01))
    Eng.labels(method='LTE').set(ping(Targets[1].IP,0.01))
    Eng.labels(method='MR').set(ping(Targets[2].IP,0.01))

    
    Mor.labels(method='PS').set(ping(Targets[3].IP,0.01))
    Mor.labels(method='LTE').set(ping(Targets[4].IP,0.01))
    Mor.labels(method='MR').set(ping(Targets[5].IP,0.01))

    
    Pow.labels(method='PS').set(ping(Targets[6].IP,0.01))
    Pow.labels(method='LTE').set(ping(Targets[7].IP,0.01))
    Pow.labels(method='MR1').set(ping(Targets[8].IP,0.01))
    Pow.labels(method='MR2').set(ping(Targets[9].IP,0.01))
    Pow.labels(method='MR3').set(ping(Targets[10].IP,0.01))

    
    Rec.labels(method='PS').set(ping(Targets[11].IP,0.01))
    Rec.labels(method='LTE').set(ping(Targets[12].IP,0.01))
    Rec.labels(method='MR').set(ping(Targets[13].IP,0.01))

   
    Blo.labels(method='PS').set(ping(Targets[14].IP,0.01))
    #Blo.labels(method='LTE').set(0)
    #Blo.labels(method='MR').set(0)
    
    print("done")
    time.sleep(1000)
