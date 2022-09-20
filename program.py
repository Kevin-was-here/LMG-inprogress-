import time
import subprocess
import PySimpleGUI as sg
import os

endProgram = False
killList = []

def execute():
  """
  Kill function execute program
  pre: none
  post: none
  """
  for i in killList: 
      try: #Kill tasks that are in the killlist
          subprocess.run('TASKKILL /F /IM '+ i, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      except:
          print("oops")

def cleanup(progList):
  """
  Cleans up the program list from OS since it was obtained in wacky notation.
  pre:
    Proglist --> program list
  post:
    sorted program list
  """
  temp = []
  for i in progList: #loop through list
      if ".exe" in i:  
        #extract only programs with .exe (literally almost all of them)
        #probably shouldn't remove them if they don't have .exe anyway
          if not(i in temp):
              temp.append(i)
  temp.sort() #sort by alphabet
  return temp

def timeToWork(t, window):
    """
    Timer function takes the seconds and runs a countdown timer, displays the number of seconds remaining

    pre: timer in seconds, timer window
    post: none
    """
    global endProgram
    currTime = int(time.time())
    endTime = currTime + t
    listUpdate = True
    while endTime > currTime:
        #update time
        currTime = int(time.time())
        t = endTime - currTime
        mins = t // 60
        secs = t % 60
        timer = '{:02d}:{:02d}'.format(mins, secs)
        event, values = window.read(timeout=1)
        if listUpdate:
            window['death'].update(values=killList)
            listUpdate = False
        window.un_hide()
        window['timeText'].update("Time left: " + timer)
        execute()
        #for when program is closed mid timer
        if event == "Close" or event == sg.WIN_CLOSED:
            window.close()
            endProgram = True
            break
        if event == "goHome":
            window.hide()
            break
    
    if endTime <= currTime:
        window["timeText"].update("Congrats you're done good work!")
        window["goHome"].update(text="Back to Home")
        while True:
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                window.close()
                endProgram = True
                break
            if event == "goHome":
                window.hide()
                break

def editDeadProgram(window):
    global killList, endProgram

    while True:
        event, values = window.read(timeout=1)
        window.un_hide()
        if event == "Close" or event == sg.WIN_CLOSED:
            endProgram = True
            break
        elif event == "Back to Home":
                window.hide()
                break
        elif event == "Add":
            for i in values['prog']:
                if not(i in killList):
                    killList.append(i)
                    killList.sort()
                    window['death'].update(values=killList)
        elif event == "Remove":
            for i in values['death']:
                killList.remove(i)
                window['death'].update(values=killList)
        elif event == "Refresh":
            window['prog'].update(values=(cleanup(os.popen('wmic process get description, processid').read().split())))

def main():
    progList = cleanup(os.popen('wmic process get description, processid').read().split())
    readFile()
    open('killList.txt', 'w').close()
    #-------------------GUI layouts--------------------------
    homeLayout = [
        [sg.Text("Enter the time you want to work for: (in seconds)", key="text")],
        [sg.InputText(key="timeInput", size=(30))],
        [sg.Button("Start Timer"),sg.Button("Update Blocklist"), sg.Button("Close")],
        [sg.Text("Current items being murdered")],
        [sg.Listbox(values=killList, select_mode='extended', key='death', size=(30, 6))]
    ]

    timeLayout = [
        [sg.Text("hmm", key="timeText")],
        [sg.Button("Stop Timer",key="goHome"), sg.Button("Close")],
        [sg.Text("Current items being murdered")],
        [sg.Listbox(values=killList, select_mode='extended', key='death', size=(30, 6))]
    ]

    editLayout = [
        [sg.Text("Select the items to be blocked: ")],
        [sg.Listbox(values=progList, select_mode='extended', key='prog', size=(30, 15)), 
        sg.Listbox(values=killList, select_mode='extended', key='death', size=(30, 15))],
        [sg.Button("Back to Home"),sg.Button("Refresh"),sg.Button("Add"),sg.Button("Remove"), sg.Button("Close")]
    ]

    window1 = sg.Window("DO YOUR WORK!!", homeLayout, size=(325,250))
    window2 = sg.Window("DO YOUR WORK!!", timeLayout)
    window3 = sg.Window("DO YOUR WORK!!", editLayout)

    while True:
        event, values = window1.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
        elif event == "Start Timer":
            t = values["timeInput"]
            if(t.isdigit()):
                window1.hide()
                timeToWork(int(t), window2)
                if endProgram == True:
                    break
                window1.un_hide()
            else:
                window1["text"].update("Please enter a proper number (in seconds): ")
        elif event == "Update Blocklist":
            window1.hide()
            editDeadProgram(window3)
            if endProgram == True:
                break
            window1['death'].update(values=killList)
            window3['death'].update(values=killList)
            window1.un_hide()
        
    print("program End")
    addtoFile()
    window1.close()
    window2.close()
    window3.close()

def readFile():
  global killList
  f = open("killList.txt",'r')
  killList = f.readline().split()
  killList.sort()
  f.close()

def addtoFile():
  open(r"C:\Users\kloak\Desktop\Programming\LMG\killList.txt", 'w').close()
  with open(r"C:\Users\kloak\Desktop\Programming\LMG\killList.txt", 'wt') as fp:
        # write each item on a new line
    fp.write(' '.join(str(line) for line in killList))
  fp.close()


if __name__ == '__main__':
  main()