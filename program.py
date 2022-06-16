from ctypes import alignment
from operator import mod
from select import select
import time
import subprocess
import PySimpleGUI as sg
import os

def cleanup(progList):
    temp = []
    for i in progList:
        if ".exe" in i:
            if not(i in temp):
                temp.append(i)
    return temp

def executeprog(progname):
    """
    Function takes a executable name and forcefully murders it

    Pre: Filename
    post: none
    """
    try:
        subprocess.run('TASKKILL /F /IM '+ progname, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except:
        print("oops")

def timeToWork(t):
    """
    Timer function takes the seconds and runs a countdown timer, displays the number of seconds remaining

    pre: timer in seconds
    post: none
    """
    currTime = int(time.time())
    endTime = currTime + t
    while endTime > currTime:
        #update time
        currTime = int(time.time())
        t = endTime - currTime
        mins = t // 60
        secs = t % 60
        timer = '{:02d}:{:02d}'.format(mins, secs)
        event, values = window.read(timeout=10)
        window['text'].update("Time left: " + timer)
        execute()
        #for when program is closed mid timer
        if event == "close" or event == sg.WIN_CLOSED:
            window.close()
            break
    
    window['text'].update("Time is up congrats")

def execute():
    """
    Kill function checks for if a program is open and sends the program name to be executed
    pre: none
    post: none
    """
    for i in killList:
        executeprog(i)
    
#main
killList = ["Minecraft.exe","RiotClientUx.exe",
                "BootstrapPackagedGame","VALORANT-Win64-Shipping.exe"]

progList = cleanup(os.popen('wmic process get description, processid').read().split())

#building a GUI
winLayout = [
    [sg.Text("Please enter how long you want to work for: ", key="text")],
    [sg.InputText()],
    [sg.Button("Start Timer"),sg.Button("Add Death"), sg.Button("Close")],
    [sg.Text("Current items being murdered")],
    [sg.Listbox(values=killList, select_mode='extended', key='fac', size=(30, 6))]
]

window = sg.Window("DO YOUR WORK!!", winLayout)
#t = input("Enter how many seconds you want to work for: ")
#timeToWork(int(t))

while True:
    event, values = window.read()
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event == "Start Timer":
        t = values[0]
        timeToWork(int(t))
    elif event == "Add Death":
        window.close()
        layout = [
            [sg.Text("Select the items to be killed: ", key="text")],
            [sg.Listbox(values=progList, select_mode='extended', key='prog', size=(30, 15)), 
            sg.Listbox(values=killList, select_mode='extended', key='death', size=(30, 15))],
            [sg.Button("Back to Timer"),sg.Button("Add to Death"),sg.Button("Remove Death"), sg.Button("Close")]
        ]
        window = sg.Window("DO YOUR WORK!!", layout)

window.close()
