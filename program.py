import time
import subprocess
import PySimpleGUI as sg
import os

"""
Function takes a executable name and forcefully murders it

Pre: Filename
post: none
"""
def executeprog(progname):
    try:
        subprocess.run('TASKKILL /F /IM '+ progname, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except:
        print("oops")

"""
Timer function takes the seconds and runs a countdown timer, displays the number of seconds remaining

pre: timer in seconds
post: none
"""
def timeToWork(t):

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Time left: " + timer, end = "\r")
        execute()
        time.sleep(0.5)
        t -= 1
    
    print("Time is up congrats")

"""
Kill function checks for if a program is open and sends the program name to be executed
pre: none
post: none
"""
def execute():
    progList = ["Minecraft.exe","RiotClientUx.exe",
                "BootstrapPackagedGame","VALORANT-Win64-Shipping.exe"]

    for i in progList:
        executeprog(i)
    
#main

#building a GUI
winLayout =  [[sg.Text("Hello from PysimpelGuI")],[sg.Button("close")]]
window = sg.Window("DO YOUR WORK!!", winLayout)
#t = input("Enter how many seconds you want to work for: ")
#timeToWork(int(t))

while True:
    event, values = window.read()
    if event == "close" or event == sg.WIN_CLOSED:
        break

window.close()