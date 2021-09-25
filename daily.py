import tkinter as tk

def createButtons(frame):
    frame.hi_there = tk.Button(frame)
    frame.hi_there["text"] = "Hello World\n(click me)"
    frame.hi_there["command"] = say_hi()
    frame.hi_there.pack(side="top")
    frame.quit = tk.Button(frame, text="QUIT", fg="red",command=frame.master.destroy)
    frame.quit.pack(side="bottom")

def say_hi():
    print("hi there, everyone!")