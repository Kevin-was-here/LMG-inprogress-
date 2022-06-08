import time
import subprocess

def closeFile(filename):
    try:
        subprocess.run('TASKKILL /F /IM '+ filename, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    except:
        print("oops")

def timeToWork(t):

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Time left: " + timer, end = "\r")
        closeFile("chrome.exe")
        time.sleep(1)
        t -= 1
    
    print("Time is up congrats")

t = input("Enter how many seconds you want to work for: ")
timeToWork(int(t))
