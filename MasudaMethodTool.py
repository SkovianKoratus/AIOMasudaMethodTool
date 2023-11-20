import tkinter as tkt
#from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctkt
import time
from pygame import mixer
import ast
from pynput.keyboard import Key, Listener
import ttkbootstrap as ttk

mixer.init()

def exitAllProgram():
    global listener
    root.quit()
    root.destroy()
    if listener:
        listener.stop()  # stop thread
        listener.join()  # wait till thread really ends its job
        listener = None  # to inform that listener doesn't exist



huntCountSaveFile = "Data/huntCount.txt"

counting = False
paused = False
tempMinutes = 0
tempSeconds = 0
tempSwitchOn = False
listeningSwitch = False

def onRelease(key):
    if key == Key.up:
        huntCountUp()

    elif key==Key.down:
        huntCountDown()
    
    elif key==Key.alt_l:
        timerPause()
    
    elif key==Key.ctrl_l:
        timerCountdown()

def listenerStart():
    global listener

    if not listener:
        listener = Listener(on_release=onRelease)
        listener.start() # start thread

def listenerStop():
    global listener

    if listener:
        listener.stop()  # stop thread
        listener.join()  # wait till thread really ends its job
        listener = None  # to inform that listener doesn't exist


## -- system settings -- ##
# Sets the appearance of the program to the system default (light or dark)
ctkt.set_appearance_mode("dark")
# Sets the default color theme of the program
#ctkt.set_default_color_theme("dark-blue")



## -- App Frame -- ##
# initialize tkinter
root = ctkt.CTk()

# specifiy geometry
root.geometry("400x335")
# sets app title
root.title("Masuda Method Tool")

darkSwitch = PhotoImage(file="Images/darkModeSwitch.png")
lightSwitch = PhotoImage(file="Images/lightModeSwitch.png")
switchValue = True
lightDarkDifference = "transparent"

# Theme
def themeToggle():

    global switchValue
    global lightDarkDifference

    if switchValue == True:
        switch.configure(image=lightSwitch)
        style.theme_use("litera")
        ctkt.set_appearance_mode("light")
        lightDarkDifference = "white"
        switchValue = False
    
    else:
        switch.configure(image=darkSwitch)
        style.theme_use("darkly")
        ctkt.set_appearance_mode("dark")
        lightDarkDifference = "transparent"
        switchValue = True

    timerFrame.configure(bg_color=lightDarkDifference)
    timerStartButton.configure(bg_color=lightDarkDifference)
    timerPauseButton.configure(bg_color=lightDarkDifference)
    huntCounterFrame.configure(bg_color=lightDarkDifference)
    huntCounterUpButton.configure(bg_color=lightDarkDifference)
    huntCounterDownButton.configure(bg_color=lightDarkDifference)
    huntCounterClearButton.configure(bg_color=lightDarkDifference)
    titleFrame.configure(bg_color=lightDarkDifference)
    title.configure(bg_color=lightDarkDifference)
    switch.configure(bg_color=lightDarkDifference)



def fileDropdownOptions(x):
    global tempSwitchOn
    global listeningSwitch
    if x == "Always on Top" and tempSwitchOn == False:
        tempSwitchOn = True
        root.wm_attributes("-topmost", 1)
    elif x == "Always on Top" and tempSwitchOn == True:
        tempSwitchOn = False
        root.wm_attributes("-topmost", 0)
    elif x == "Toggle Listening" and listeningSwitch == True:
        listeningSwitch = False
        listenerStop()
    elif x == "Toggle Listening" and listeningSwitch == False:
        listeningSwitch = True
        listenerStart()
    else:
        exitAllProgram()

# fileFrame = ctkt.CTkFrame(root,bg_color="transparent",fg_color="transparent")
# fileFrame.pack(side="top",anchor="w")



# fileDropdown = ctkt.CTkComboBox(fileFrame, values=["Always On Top", "Exit"], command=fileDropdownOptions)
# fileDropdown.pack(side="left")

titleFrame = ctkt.CTkFrame(root,bg_color="transparent",fg_color="transparent")
titleFrame.pack(side="top")

# exitButton = ctkt.CTkButton(titleFrame,text="Exit",command=exitAllProgram, width=50,bg_color=lightDarkDifference,fg_color=lightDarkDifference,corner_radius=0,border_width=0,border_spacing=0)
# exitButton.pack(padx=0,pady=0, side="left")

fileDropdownMenu = ttk.Menubutton(titleFrame,text="Settings")
fileDropdownMenu.pack(side="left",anchor="w")

# Creates menu
fileDropdownInsideMenu = ttk.Menu(fileDropdownMenu)

# Adds items to menu
fileMenuItem = StringVar()
for x in ["Always on Top", "Toggle Listening", "Exit"]:
    fileDropdownInsideMenu.add_radiobutton(label=x,command=lambda x=x: fileDropdownOptions(x))

fileDropdownMenu["menu"] = fileDropdownInsideMenu

title = ctkt.CTkLabel(titleFrame, text="AIO Masuda Method Tool")
# Inserts element + padding ("pady" is distance from top of program )
title.pack(side="left", padx=80)

style = ttk.Style()
style.theme_use('darkly')
# style.configure('new.TNotebook', background = '#26242f', foreground = '#26242f', width = 20, borderwidth=0, focusthickness=0, focuscolor='#26242f')
#style.configure('TNotebook', width = 20, borderwidth=0, focusthickness=0, focuscolor='#26242f')
#style.map('TNotebook', foreground=[('active','#26242f')],background=[('active','#26242f')])
# style.configure('new.TNotebook.Tab', background="#26242f", foreground="white", borderwidth=0, focusthickness=0, focuscolor='#26242f')
#style.configure('TNotebook.Tab', borderwidth=0, focusthickness=0, focuscolor='#26242f')

# style.map("new.TNotebook", foreground= [("selected", "#26242f")], background=[("selected", "#26242f")])
#root.config(bg="#26242f")

switch = ctkt.CTkButton(titleFrame, image=darkSwitch, bg_color="transparent",fg_color="transparent",text="",command=themeToggle,width=10,corner_radius=0)
switch.pack(padx=0, side="right")

mainTool = ttk.Notebook(root,width=525,height=350)
mainTool.pack()

#picnicFrame = ctkt.CTkFrame(mainTool, width=525, height=540,fg_color="#26242f",bg_color="black") #fg_color="#26242f"
#huntFrame = ctkt.CTkFrame(mainTool, width=525, height=540,fg_color="#26242f",bg_color="black")
picnicCanvas = ctkt.CTkCanvas(mainTool, bg="#26242f", highlightthickness=0, width=525, height=540)
huntCanvas = ctkt.CTkCanvas(mainTool, bg="#26242f", highlightthickness=0, width=525, height=540)

picnicCanvas.pack(fill="both",expand=1)
huntCanvas.pack(fill="both",expand=1)
#picnicFrame.pack(fill="both",expand=1) #fill="both" #expand=1
#huntFrame.pack(fill="both",expand=1)

mainTool.add(picnicCanvas, text="Picnic")
mainTool.add(huntCanvas, text="Hunting")

def timerCountdown():
    mixer.music.stop()
    global paused
    global counting
    global tempMinutes, tempSeconds
    counting = True
    
    global minute, second

    if paused == False:
        minute, second = 5, 0
        minuteT.set(f" 0{minute} ")
        timerFrame.update()
    else:
        minute, second = tempMinutes, tempSeconds
        paused = False
    

    totalinseconds = minute * 60 + second

    while totalinseconds > -1 and counting:
        if second >= 0:

            if second > 9:
                secondT.set(f" {second} ")
                timerFrame.update()
                second -= 1
                totalinseconds -= 1
                time.sleep(1)
            else:
                secondT.set(f" 0{second} ")
                timerFrame.update()
                second -= 1
                totalinseconds -= 1
                time.sleep(1)
            
        elif minute > 0:
            if minute > 9:
                minute -= 1
                minuteT.set(f" {minute} ")
                second = 59
            else:
                minute -= 1
                minuteT.set(f" 0{minute} ")
                second = 59
    
    if totalinseconds == -1:
        mixer.music.load("Sounds/timerEndSound.mp3")
        mixer.music.play()

def timerPause():
    global counting
    global paused
    global minute, second
    global tempMinutes, tempSeconds

    if counting == True and paused == False:
        counting = False
        paused = True
        if second > 9:
            secondT.set(f" {second} ")
            timerFrame.update()
            tempSeconds = second
        else:
            secondT.set(f" 0{second} ")
            timerFrame.update()
            tempSeconds = second
        if minute > 9:
            minuteT.set(f" {minute} ")
            tempMinutes = minute
        else:
            minuteT.set(f" 0{minute} ")
            tempMinutes = minute





minuteT = tkt.StringVar(value=" 05 ")
secondT = tkt.StringVar(value=" 00 ")

timerFrame = ctkt.CTkFrame(picnicCanvas, fg_color=lightDarkDifference,bg_color=lightDarkDifference)
timerFrame.pack()

minuteLabel = ctkt.CTkLabel(timerFrame, textvariable=minuteT,height=50,font=("Arial", 50))
colonLabel = ctkt.CTkLabel(timerFrame, text=":",font=("Arial", 50))
secondLabel = ctkt.CTkLabel(timerFrame, textvariable=secondT,height=50,font=("Arial", 50))

minuteLabel.grid(column=0, row=0,)
colonLabel.grid(column=1, row=0)
secondLabel.grid(column=2, row=0)

timerStartButton = ctkt.CTkButton(picnicCanvas, text="Start", command=timerCountdown,bg_color=lightDarkDifference)
timerStartButton.pack()

timerPauseButton = ctkt.CTkButton(picnicCanvas, text="Pause", command=timerPause,bg_color=lightDarkDifference)
timerPauseButton.pack()

def saveHuntCount(huntCount, filename):
    with open(filename, "w") as f:
        f.write(str(huntCount))

def loadHuntCount(filename):
    with open(filename, "r") as f:
        read = f.read()
    return read

def huntCountUp():

    count = int(huntCounter.get())
    count += 1
    huntCounter.set(f"{count}")
    saveHuntCount(str(count),huntCountSaveFile)
    huntCounterLabel.update()

def huntCountDown():

    count = int(huntCounter.get())
    count -= 1
    huntCounter.set(f"{count}")
    saveHuntCount(str(count),huntCountSaveFile)
    huntCounterLabel.update()

def huntCountClear():
    huntCounter.set("0")
    saveHuntCount(0,huntCountSaveFile)
    huntCounterLabel.update()
    


huntCounterFrame = ctkt.CTkFrame(huntCanvas, fg_color="transparent")
huntCounterFrame.pack()

huntCounter = tkt.StringVar(value="0")

huntCounterLabel = ctkt.CTkLabel(huntCounterFrame, textvariable=huntCounter,font=("Arial", 50))
huntCounterLabel.pack()

huntCounterUpButton = ctkt.CTkButton(huntCanvas, text="+1", command=huntCountUp)
huntCounterUpButton.pack()

huntCounterDownButton = ctkt.CTkButton(huntCanvas, text="-1", command=huntCountDown)
huntCounterDownButton.pack()

huntCounterClearButton = ctkt.CTkButton(huntCanvas, text="Clear", command=huntCountClear)
huntCounterClearButton.pack()


# timerLabel = ctkt.CTkLabel(picnicFrame, text=)
# # Inserts element + padding ("pady" is distance from top of program )
# timerLabel.pack(padx=1, pady=1)



if __name__ == "__main__":
    
    try:
        hCount = ast.literal_eval(loadHuntCount(huntCountSaveFile))
        huntCounter.set(int(hCount))
    except:
        hCount = {}

    listener = None  # to keep listener

    root.protocol("WM_DELETE_WINDOW", exitAllProgram)
    root.mainloop()

    if listener: # if listener is not None:
        listener.stop()  # stop thread
        listener.join()  # wait till thread really ends its job



