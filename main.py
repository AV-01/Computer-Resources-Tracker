from tkinter import *
import tkinter.font as font
from tkinter import messagebox
import time
import threading
import write_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = Tk()
run = False
quiting = False
def dataCollecting():
    while not quiting:
        if run:
            write_data.write_data()
            time.sleep(10)
        else:
            time.sleep(10)

mainThread = threading.Thread(target=dataCollecting)

def tracking():
    global run
    if run == True:
        run = False
        status.config(text="Data collecting: Stopped")
    elif run == False:
        run = True
        status.config(text="Data collecting: Started")

def createViz():
    vizWindow = Toplevel(root)
    vizWindow.title("Vizualization")
    vizWindow.geometry("400x400")
    # title = Label(vizWindow, text ="Vizualizations").grid()
    compData = pd.read_csv('computer_data.csv')
    figure = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, vizWindow)
    chart_type.get_tk_widget().pack()
    df = compData[['time','cpu','ram percent']].groupby('time').sum()
    df.plot(kind='line', legend=True, ax=ax)
    ax.set_title('CPU and RAM usage')
    # Network
    figure = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, vizWindow)
    chart_type.get_tk_widget().pack()
    df = compData[['time','net_in','net_out']].groupby('time').sum()
    df.plot(kind='line', legend=True, ax=ax)
    ax.set_title('Network Usage')
    # vizWindow.mainloop()


h1Font = font.Font(size=30)
h2Font = font.Font(size=20)

title = Label(root, text='Resource Tracker')
title['font'] = h1Font
# Main fram creation
mainFrame = LabelFrame(root, text="",padx=10,pady=10)
mainLabel = Label(mainFrame, text='Main')
mainLabel['font'] = h2Font
status = Label(mainFrame, text = 'Data collecting: Stopped')
trackerSwitch = Button(mainFrame, text = "Click to toggle resource tracking",command=tracking)
# Vizualization frame creation
vizFrame = LabelFrame(root, text="",padx=10,pady=10)
vizLabel = Label(vizFrame, text='Vizualization')
vizLabel['font'] = h2Font
vizInfo = Label(vizFrame, text = 'Create Vizualizations of your data so far')
createVizButton = Button(vizFrame, text = "Create",command=createViz)

title.pack()
# Create main frame
mainFrame.pack()
mainLabel.pack()
status.pack()
trackerSwitch.pack()
# Create viz frame
vizFrame.pack()
vizLabel.pack()
vizInfo.pack()
createVizButton.pack()
# title.place(x=150,y=0)
# trackerSwitch.place(x=120, y=200)

root.minsize(400, 400)
root.maxsize(400, 400)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        global quiting
        quiting = True
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

mainThread.start()
root.mainloop()
