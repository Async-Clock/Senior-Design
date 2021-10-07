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
SLEEP=8

while(selection !=0):
    os.system('cls')
    print("-------Dash Project Installation Package-------".center(widthpad,'-'))
    print("".center(widthpad,'-'))
    print("".center(widthpad,'-'))

    print("Options:".ljust(widthpad,' '))
    print("0-Exit".ljust(widthpad,' '))
    print("1-Install".ljust(widthpad,' '))
    print("2-Uninstall".ljust(widthpad,' '))
    print("3-Create Services".ljust(widthpad,' '))
    print("4-Remove Services".ljust(widthpad,' '))
    

    selection=int(input())


    if(selection==1):
        temp=' mkdir '+ filepath+'"'
        output=subprocess.getoutput(temp)

        if(output==''):
            
            temp='xcopy "'+workingDirName+zipfilename+'" '+filepath+'"'
            output=subprocess.getoutput(temp)
            print(output)

            temp='tar -xf '+ filepath+zipfilename+'"'+' -C '+filepath+'"'
            output=subprocess.getoutput(temp)
            print(output)

            temp='del /f '+filepath+zipfilename+'"'
            output=subprocess.getoutput(temp)
            print(output)

            selection=input("Do you want install as services(y/n)")
            if(selection=='y'):
                temp=nssmFilePath + ' install Grafana '+ filepath+'\\grafana-8.1.5\\bin\\grafana-server.exe"'
                temp2=nssmFilePath + ' install Prometheus '+ filepath+'\\Prometheus\\prometheus.exe"'
                temp3=nssmFilePath + ' install PingerApp '+ filepath+'\\PingerApp\\PingerApp.exe"'
                output=subprocess.getoutput(temp)
                print(output)
                output=subprocess.getoutput(temp2)
                print(output)
                output=subprocess.getoutput(temp3)
                print(output)
                print("Please Restart the PC to Update services")
                time.sleep(SLEEP)
        
        
        else:
            print("C:\\Dash Project Files already exists please remove it using Uninstall")
            time.sleep(SLEEP)


    if(selection==2):
        temp=nssmFilePath + ' remove Grafana '+'confirm'
        temp2=nssmFilePath + ' remove Prometheus '+'confirm'
        temp3=nssmFilePath + ' remove PingerApp '+ 'confirm'
        output=subprocess.getoutput(temp)
        print(output)
        output=subprocess.getoutput(temp2)
        print(output)
        output=subprocess.getoutput(temp3)
        print(output)
        temp='rmdir /q /s '+filepath+'"'
        output=subprocess.getoutput(temp)
        print(output)
        print("Please Restart the PC to Update services")
        time.sleep(SLEEP)


    if(selection==3):
        temp=nssmFilePath + ' install Grafana '+ filepath+'\\grafana-8.1.5\\bin\\grafana-server.exe"'
        temp2=nssmFilePath + ' install Prometheus '+ filepath+'\\Prometheus\\prometheus.exe"'
        temp3=nssmFilePath + ' install PingerApp '+ filepath+'\\PingerApp\\PingerApp.exe"'
        output=subprocess.getoutput(temp)
        print(output)
        output=subprocess.getoutput(temp2)
        print(output)
        output=subprocess.getoutput(temp3)
        print(output)
        print("Please Restart the PC to Update services")
        time.sleep(SLEEP)
    

    if(selection==4):
        temp=nssmFilePath + ' remove Grafana '+'confirm'
        temp2=nssmFilePath + ' remove Prometheus '+'confirm'
        temp3=nssmFilePath + ' remove PingerApp '+ 'confirm'
        output=subprocess.getoutput(temp)
        print(output)
        output=subprocess.getoutput(temp2)
        print(output)
        output=subprocess.getoutput(temp3)
        print(output)
        print("Please Restart the PC to Update services")
        time.sleep(SLEEP)

