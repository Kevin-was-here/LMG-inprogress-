import os

def openFile():
    try:
        os.startfile('hi.txt')

    except:
        print("oops")

def closeFile():
    try:
        os.system('TASKKILL /F /IM firefox.exe')

    except:
        print("oops")



closeFile()