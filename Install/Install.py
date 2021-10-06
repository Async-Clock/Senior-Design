import os
import sys
import subprocess
import time
filename='Dash Project Files'
zipfilename='\\Dash-Windows-Files.zip'
filepath='"C:\\'+filename
nssmFilePath= filepath+'\\nssm.exe"'

widthpad=80
workingDirName = os.path.dirname(sys.argv[0])
selection=1

while(selection !=0):
    os.system('cls')
    print("-------Dash Project Installation Package-------".center(widthpad,'-'))
    print("".center(widthpad,'-'))
    print("".center(widthpad,'-'))

    print("Options:".ljust(widthpad,' '))
    print("0-Exit".ljust(widthpad,' '))
    print("1-Install".ljust(widthpad,' '))
    print("2-Create Services".ljust(widthpad,' '))

    selection=int(input())


    if(selection==1):
        temp=' mkdir '+ filepath+'"'
        output=subprocess.getoutput(temp)

        if(output==''):
            
            temp='xcopy "'+workingDirName+zipfilename+'" '+filepath+'"'
            temp2='tar -xf '+ filepath+zipfilename+'"'+' -C '+filepath+'"'
            temp3='del /f '+filepath+zipfilename+'"'
            output=subprocess.getoutput([temp,temp2,temp3])
            print(output)


        
            selection=input("Do you want install as services(y/n)")
            if(selection=='y'):
                temp=nssmFilePath + ' install Grafana '+ filepath+'\\grafana-8.1.5\\bin\\grafana-server.exe"'
                temp2=nssmFilePath + ' set Grafana AppDirectory '+ filepath+'\\grafana-8.1.5"'
                temp3=nssmFilePath + ' install Prometheus '+ filepath+'\\Prometheus\\prometheus.exe"'
                temp4=nssmFilePath + ' install Grafana '+ filepath+'\\PingerApp"'
                output=subprocess.getoutput([temp,temp2,temp3])
                print(output)
        
        
        else:
            print("C:\\Dash Project Files already exists")

    if(selection==2):
        temp=nssmFilePath + ' install Grafana '+ filepath+'\\grafana-8.1.5\\bin\\grafana-server.exe"'
        temp2=nssmFilePath + ' set Grafana AppDirectory '+ filepath+'\\grafana-8.1.5"'
        temp3=nssmFilePath + ' install Prometheus '+ filepath+'\\Prometheus\\prometheus.exe"'
        temp4=nssmFilePath + ' install Grafana '+ filepath+'\\grafana-8.1.5\\bin\\grafana-server.exe"'
        output=subprocess.getoutput([temp,temp2,temp3])
        print(output)

