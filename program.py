import os


def closeFile(filename):
    try:
        os.system('TASKKILL /F /IM '+ filename)

    except:
        print("oops")


closeFile("firefox.exe")