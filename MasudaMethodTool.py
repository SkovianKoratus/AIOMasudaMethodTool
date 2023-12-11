import tkinter as tkt
#from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctkt
import time
from pygame import mixer
# file loader
import ast
from pynput.keyboard import Key, Listener
import ttkbootstrap as ttk

# initialize mixer from pygame
mixer.init()

# Exit program function
def exitAllProgram():
    global listener
    global counting
    global paused
    if counting == True and paused == False:
        counting = False
        paused = True
    root.quit()
    root.destroy()
    if listener:
        listener.stop()  # stop thread
        listener.join()  # wait till thread really ends its job
        listener = None  # to inform that listener doesn't exist


# Global variables
huntCountSaveFile = "Data/huntCount.txt"

counting = False
paused = False
tempMinutes = 0
tempSeconds = 0
minsTotalSandwichReset = 0
tempVar = 0
tempSwitchOn = False
listeningSwitch = False

# -- for the listener -- #
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

# -- end listener -- #

## -- system settings -- ##
# Sets the appearance of the program to the system default (light or dark)
ctkt.set_appearance_mode("dark")



## -- App Frame -- ##
# initialize tkinter
root = ctkt.CTk()

# specifiy geometry
root.geometry("430x335")
# sets app title
root.title("Masuda Method Tool")

# light/dark mode global variables
darkSwitch = PhotoImage(file="Images/darkModeSwitch.png")
lightSwitch = PhotoImage(file="Images/lightModeSwitch.png")
switchValue = True
lightDarkDifference = "transparent"

# -- Theme -- #
def themeToggle():

    global switchValue
    global lightDarkDifference

    # toggles light/dark mode to light mode
    if switchValue == True:
        switch.configure(image=lightSwitch)
        style.theme_use("litera")
        ctkt.set_appearance_mode("light")
        lightDarkDifference = "white"
        switchValue = False
    
    # toggles light/dark mode to dark mode
    else:
        switch.configure(image=darkSwitch)
        style.theme_use("darkly")
        ctkt.set_appearance_mode("dark")
        lightDarkDifference = "transparent"
        switchValue = True

    # Setting color differences between light and dark mode.
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
    totalMinutes.configure(bg_color=lightDarkDifference)


# -- Settings drop down option definitions -- #
def fileDropdownOptions(x):
    global tempSwitchOn
    global listeningSwitch
    # toggles on the program window stay on top of all other windows
    if x == "Always on Top" and tempSwitchOn == False:
        tempSwitchOn = True
        root.wm_attributes("-topmost", 1)
    # toggles off the program window stay on top of all other windows
    elif x == "Always on Top" and tempSwitchOn == True:
        tempSwitchOn = False
        root.wm_attributes("-topmost", 0)
    # toggles off the listener for button inputs
    elif x == "Toggle Listening" and listeningSwitch == True:
        listeningSwitch = False
        listenerStop()
    # toggles on the listener for button inputs
    elif x == "Toggle Listening" and listeningSwitch == False:
        listeningSwitch = True
        listenerStart()
    # the exit button calls exitAllProgram function
    else:
        exitAllProgram()

# Frame for the title
titleFrame = ctkt.CTkFrame(root,bg_color="transparent",fg_color="transparent")
titleFrame.pack(side="top")

# Settings for the drop 
fileDropdownMenu = ttk.Menubutton(titleFrame,text="Settings")
fileDropdownMenu.pack(side="left",anchor="w")

# Creates menu
fileDropdownInsideMenu = ttk.Menu(fileDropdownMenu)

# Adds items in fileDropdownOptions to menu
fileMenuItem = StringVar()
for x in ["Always on Top", "Toggle Listening", "Exit"]:
    fileDropdownInsideMenu.add_radiobutton(label=x,command=lambda x=x: fileDropdownOptions(x))

fileDropdownMenu["menu"] = fileDropdownInsideMenu

# makes title label and puts it in the title frame in the middle
title = ctkt.CTkLabel(titleFrame, text="AIO Masuda Method Tool")

# Inserts element + padding
title.pack(side="left", padx=80)

# -- Default Style Settings -- #
style = ttk.Style()
style.theme_use('darkly')

# light/dark mode switch button
switch = ctkt.CTkButton(titleFrame, image=darkSwitch, bg_color="transparent",fg_color="transparent",text="",command=themeToggle,width=10,corner_radius=0)
switch.pack(padx=0, side="right")

# -- main tool tabs -- #
mainTool = ttk.Notebook(root,width=525,height=350)
mainTool.pack()

picnicCanvas = ctkt.CTkCanvas(mainTool, bg="#26242f", highlightthickness=0, width=525, height=540)
huntCanvas = ctkt.CTkCanvas(mainTool, bg="#26242f", highlightthickness=0, width=525, height=540)

picnicCanvas.pack(fill="both",expand=1)
huntCanvas.pack(fill="both",expand=1)

mainTool.add(picnicCanvas, text="Picnic")
mainTool.add(huntCanvas, text="Hunting")
# -- tabs end -- #

# main timer function ( might need to be reworked)
def timerCountdown():
    mixer.music.stop()
    global paused
    global counting
    global tempMinutes, tempSeconds
    counting = True
    
    global minute, second

    global minsTotalSandwichReset

    global tempVar

    if tempVar >= 30:
        tempVar = 0
        minsTotalSandwichReset.set(f"{tempVar}")
        totalMinutes.update()


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
                timerFrame.after(1000)
            else:
                secondT.set(f" 0{second} ")
                timerFrame.update()
                second -= 1
                totalinseconds -= 1
                timerFrame.after(1000)
                
            
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
        tempVar += 5
        minsTotalSandwichReset.set(f"{tempVar}")
        totalMinutes.update()
        if tempVar >= 30:
            minsTotalSandwichReset.set(f"Egg Power Over")
            totalMinutes.update()

# timer pause (might need to be reworked if timer reworked)
def timerPause():
    global counting
    global paused
    global minute, second
    global tempMinutes, tempSeconds

    if counting == True and paused == False:
        counting = False
        paused = True
        timerFrame.update()
        if second > 9:
            secondT.set(f" {second} ")
            tempSeconds = second
        else:
            secondT.set(f" 0{second} ")
            tempSeconds = second
        if minute > 9:
            minuteT.set(f" {minute} ")
            tempMinutes = minute
        else:
            minuteT.set(f" 0{minute} ")
            tempMinutes = minute

# default timer image display
minuteT = tkt.StringVar(value=" 05 ")
secondT = tkt.StringVar(value=" 00 ")

# default egg power display
minsTotalSandwichReset = tkt.StringVar(value="0")

# frame for the timer's values / labels
timerFrame = ctkt.CTkFrame(picnicCanvas, fg_color=lightDarkDifference,bg_color=lightDarkDifference)
timerFrame.pack()

# time labels
minuteLabel = ctkt.CTkLabel(timerFrame, textvariable=minuteT,height=50,font=("Arial", 50))
colonLabel = ctkt.CTkLabel(timerFrame, text=":",font=("Arial", 50))
secondLabel = ctkt.CTkLabel(timerFrame, textvariable=secondT,height=50,font=("Arial", 50))

# grid to align the labels
minuteLabel.grid(column=0, row=0,)
colonLabel.grid(column=1, row=0)
secondLabel.grid(column=2, row=0)

# Egg power label
totalMinutes = ctkt.CTkLabel(picnicCanvas, textvariable=minsTotalSandwichReset,height=50,font=("Arial", 10))
totalMinutes.pack()

# timer start button
timerStartButton = ctkt.CTkButton(picnicCanvas, text="Start", command=timerCountdown,bg_color=lightDarkDifference)
timerStartButton.pack()

# timer pause button
timerPauseButton = ctkt.CTkButton(picnicCanvas, text="Pause", command=timerPause,bg_color=lightDarkDifference)
timerPauseButton.pack()

# creates file to save hunt count to file
def saveHuntCount(huntCount, filename):
    with open(filename, "w") as f:
        f.write(str(huntCount))

# loads hunt count value from file
def loadHuntCount(filename):
    with open(filename, "r") as f:
        read = f.read()
    return read

# adds 1 to hunt counter
def huntCountUp():

    count = int(huntCounter.get())
    count += 1
    huntCounter.set(f"{count}")
    saveHuntCount(str(count),huntCountSaveFile)
    huntCounterLabel.update()

# subtracts 1 from hunt counter
def huntCountDown():

    count = int(huntCounter.get())
    count -= 1
    huntCounter.set(f"{count}")
    saveHuntCount(str(count),huntCountSaveFile)
    huntCounterLabel.update()

# sets hunt counter to 0
def huntCountClear():
    huntCounter.set("0")
    saveHuntCount(0,huntCountSaveFile)
    huntCounterLabel.update()
    

# hunt count frame
huntCounterFrame = ctkt.CTkFrame(huntCanvas, fg_color="transparent")
huntCounterFrame.pack()

# default hunt count (first time opening program)
huntCounter = tkt.StringVar(value="0")

# hunt count label for displaying hunt count
huntCounterLabel = ctkt.CTkLabel(huntCounterFrame, textvariable=huntCounter,font=("Arial", 50))
huntCounterLabel.pack()

# button for hunt count up
huntCounterUpButton = ctkt.CTkButton(huntCanvas, text="+1", command=huntCountUp)
huntCounterUpButton.pack()

# button for hunt count down
huntCounterDownButton = ctkt.CTkButton(huntCanvas, text="-1", command=huntCountDown)
huntCounterDownButton.pack()

# button for setting hunt count to 0
huntCounterClearButton = ctkt.CTkButton(huntCanvas, text="Clear", command=huntCountClear)
huntCounterClearButton.pack()

# main loop for the program (runs it)
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



