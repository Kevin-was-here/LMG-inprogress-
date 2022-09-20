import time
import subprocess
import PySimpleGUI as sg
import os

endProgram = False
blockList = []

def execute():
  """
  Kill function execute program
  pre: none
  post: none
  """
  for i in blockList: 
    try: #Kill tasks that are in the blockList
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
  global endProgram   #var for user ending program mid session
  currTime = int(time.time()) #get current time
  endTime = currTime + t  #get end time
  listUpdate = True #bool to update list
  while endTime > currTime:
    #update time
    currTime = int(time.time()) #get new curr time
    t = endTime - currTime  #get new time

    #update time on timer
    mins = t // 60
    secs = t % 60
    timer = '{:02d}:{:02d}'.format(mins, secs)
    event, values = window.read(timeout=1)

    #update list if necessary
    if listUpdate:
      window['death'].update(values=blockList)
      listUpdate = False
    window.un_hide() #reveal time window
    window['timeText'].update("Time left: " + timer) #update text
    execute()
    
    #for when program is closed mid timer
    if event == "Close" or event == sg.WIN_CLOSED:
      window.close()
      endProgram = True
      break
    if event == "goHome":
      window.hide()
      break
  
  if endTime <= currTime: #when curr time is past end time
    window["timeText"].update("Congrats you're done good work!")
    window["goHome"].update(text="Back to Home") #go home
    while True: #awaits command
      event, values = window.read()
      if event == "Close" or event == sg.WIN_CLOSED:
        window.close()
        endProgram = True
        break
      if event == "goHome":
        window.hide()
        break

def editBlocklist(window):
  """
  Edits blocklist so the program blocks the proper stuff while timer is running

  Pre:
    window --> gui where the adding/deleting happens
  post: none
  """
  global blockList, endProgram #grab globals bc they suck

  while True:
      event, values = window.read(timeout=1)
      window.un_hide() #reveal the GUI for +/- to blocklist
      if event == "Close" or event == sg.WIN_CLOSED: #prog end
          endProgram = True
          break
      elif event == "Back to Home": #go back to main GUI
              window.hide()
              break
      elif event == "Add": #add to blocklist
          for i in values['prog']: #checks the values selected
              if not(i in blockList): #adds to block list if its not there
                  blockList.append(i)
                  blockList.sort()
                  window['death'].update(values=blockList) #updates blocklist on screen
      elif event == "Remove": #remove from blocklist
          for i in values['death']: #check values selected
              blockList.remove(i) #remove values from blocklist, nothing happens if they arent in list
              window['death'].update(values=blockList) #updates blocklist
      elif event == "Refresh": #updates the OS prog list will add new progs if they had been opened
          #fun one liner to get updated os list
          window['prog'].update(values=(cleanup(os.popen('wmic process get description, processid').read().split())))

def main():
  progList = cleanup(os.popen('wmic process get description, processid').read().split()) #get prog list
  readFile() #obtain blocklist
  open('blockList.txt', 'w').close() #clear blocklist files (used for saving the blocklist later)
  #-------------------GUI layouts--------------------------
  """
  Design decision to not 
  """
  homeLayout = [
      [sg.Text("Enter the time you want to work for: (in seconds)", key="text")],
      [sg.InputText(key="timeInput", size=(30))],
      [sg.Button("Start Timer"),sg.Button("Update Blocklist"), sg.Button("Close")],
      [sg.Text("Current items being blocked")],
      [sg.Listbox(values=blockList, select_mode='extended', key='death', size=(30, 6))]
  ]

  timeLayout = [
      [sg.Text("hmm", key="timeText")],
      [sg.Button("Stop Timer",key="goHome"), sg.Button("Close")],
      [sg.Text("Current items being murdered")],
      [sg.Listbox(values=blockList, select_mode='extended', key='death', size=(30, 6))]
  ]

  editLayout = [
      [sg.Text("Select the items to be blocked: ")],
      [sg.Listbox(values=progList, select_mode='extended', key='prog', size=(30, 15)), 
      sg.Listbox(values=blockList, select_mode='extended', key='death', size=(30, 15))],
      [sg.Button("Back to Home"),sg.Button("Refresh"),sg.Button("Add"),sg.Button("Remove"), sg.Button("Close")]
  ]

  window1 = sg.Window("DO YOUR WORK!!", homeLayout, size=(325,250))
  window2 = sg.Window("DO YOUR WORK!!", timeLayout)
  window3 = sg.Window("DO YOUR WORK!!", editLayout)

#------------------------------------------------------------------------

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
          editBlocklist(window3)
          if endProgram == True:
              break
          window1['death'].update(values=blockList)
          window3['death'].update(values=blockList)
          window1.un_hide()
      
  print("program End")
  addtoFile()
  window1.close()
  window2.close()
  window3.close()

def readFile():
  global blockList
  f = open("blockList.txt",'r')
  blockList = f.readline().split()
  blockList.sort()
  f.close()

def addtoFile():
  open(r"C:\Users\kloak\Desktop\Programming\LMG\BlockList.txt", 'w').close()
  with open(r"C:\Users\kloak\Desktop\Programming\LMG\BlockList.txt", 'wt') as fp:
        # write each item on a new line
    fp.write(' '.join(str(line) for line in blockList))
  fp.close()


if __name__ == '__main__':
  main()