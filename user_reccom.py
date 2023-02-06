import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import matplotlib.dates as md
from scipy.signal import find_peaks

class show_recomm:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1150x580")
        self.root.title("Dynamic Scatterplot")
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=3)
        ctk.set_appearance_mode("Dark")
        self.zombProc = pd.read_csv('zombie_resources.csv')
        self.frame1 = ctk.CTkFrame(self.root,corner_radius=3)
        self.frame1.grid(row=0, column=0, sticky="nsew",padx=5,pady=5)
        self.frame2 = ctk.CTkFrame(self.root,corner_radius=3)
        self.frame2.grid(row=0, column=1, sticky="nsew",padx=5,pady=5)
        self.reccomTitle = ctk.CTkLabel(self.frame1, text="Reccomendations:", font=ctk.CTkFont(size=20, weight="bold"))
        self.reccomTitle.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.zombRecomTitle = ctk.CTkLabel(self.frame2, text="Zombie Processes:", font=ctk.CTkFont(size=20, weight="bold"))
        self.zombRecomTitle.grid(row=0, column=0, padx=20, pady=(20, 10))
        unique_zombs = list(dict(self.zombProc['name'].value_counts()).keys())
        stringZomb = str(unique_zombs).replace('[','').replace("]","").replace("'","").replace(",",'\n').replace(" ","")
        self.zombDesc = ctk.CTkLabel(self.frame2, text="Zombie processes are processes that constantly consume RAM, but aren't being used by the user. \nThey're unhelpful because they make your computer run slower and do nothing to benefit you. \nHere is a list of some of the zombie processes on your computer:\n\n"+stringZomb,justify='left')
        self.zombDesc.grid(row=1, column=0, padx=20, pady=(20, 10))
        # self.zombList = ctk.CTkLabel(self.frame2, text=stringZomb,justify='left')
        # self.zombList.grid(row=2, column=0, padx=20, pady=(20, 10))
        self.partitionDataByCpu()
        self.root.mainloop()

    def partitionDataByCpu(self):
        compData = pd.read_csv('computer_data.csv')
        procData = pd.read_csv('process_data.csv')
        cpu0to25 = len(compData[(compData.cpu<=25) & (compData.cpu>=0)])
        cpu25to50 = len(compData[(compData.cpu>25) & (compData.cpu<=50)])
        cpu50to75 = len(compData[(compData.cpu>50) & (compData.cpu<=75)])
        cpu75to100 = len(compData[(compData.cpu>75)])
        pureCpu = compData.dropna(subset=['cpu'])
        cpuMedian = pureCpu['cpu'].mean()
        if cpuMedian<75:
            self.cpuReccom = "The CPU seems fine!"
        else:
            self.cpuReccom = "You might want to replace your CPU."

        cpuReccomDict = {cpu0to25:"cpu0to25",cpu25to50:"cpu25to50",cpu50to75:"cpu50to75",cpu75to100:"cpu75to100"}
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu0to25":
            self.cpuDetail = "between 0% and 25%."
        elif cpuReccomDict.get(max(cpuReccomDict)) == "cpu25to50":
            self.cpuDetail = "between 25% and 50%."
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu50to75":
            self.cpuDetail = "between 50% and 75%."
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu75to100":
            self.cpuDetail = "between 75% and 100%."
        # if
        self.cpuUserReccom = ctk.CTkLabel(self.frame1, text="CPU Reccomendation: "+self.cpuReccom+"\nCPU Details: Your average CPU usage is "+str(cpuMedian)+".\nMost of the time, your cpu usage was "+self.cpuDetail, justify='left')
        self.cpuUserReccom.grid(row=1, column=0, padx=20, pady=(20, 10))

        cpu0to25 = len(compData[(compData['ram percent']<=25) & (compData['ram percent']>=0)])
        cpu25to50 = len(compData[(compData['ram percent']>25) & (compData['ram percent']<=50)])
        cpu50to75 = len(compData[(compData['ram percent']>50) & (compData['ram percent']<=75)])
        cpu75to100 = len(compData[(compData['ram percent']>75)])
        pureCpu = compData.dropna(subset=['ram percent'])
        cpuMedian = pureCpu['ram percent'].mean()
        if cpuMedian<75:
            self.cpuReccom = "The RAM seems fine!"
        else:
            self.cpuReccom = "You might want to replace your RAM."

        cpuReccomDict = {cpu0to25:"cpu0to25",cpu25to50:"cpu25to50",cpu50to75:"cpu50to75",cpu75to100:"cpu75to100"}
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu0to25":
            self.cpuDetail = "between 0% and 25%."
        elif cpuReccomDict.get(max(cpuReccomDict)) == "cpu25to50":
            self.cpuDetail = "between 25% and 50%."
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu50to75":
            self.cpuDetail = "between 50% and 75%."
        if cpuReccomDict.get(max(cpuReccomDict)) == "cpu75to100":
            self.cpuDetail = "between 75% and 100%."
        # if
        self.ramUserReccom = ctk.CTkLabel(self.frame1, text="RAM Reccomendation: "+self.cpuReccom+"\nRAM Details: Your average RAM usage is "+str(cpuMedian)+".\nMost of the time, your RAM usage was "+self.cpuDetail, justify='left')
        self.ramUserReccom.grid(row=2, column=0, padx=20, pady=(20, 10))

        firstList = list(dict(procData['name'].value_counts()[:4]).keys())
        nextString = str(firstList).replace('[','').replace("]","").replace("'","").replace(",",'\n').replace(" ","")
        self.processesUserReccom = ctk.CTkLabel(self.frame1, text="Your most used processes were: \n"+nextString, justify='left')
        self.processesUserReccom.grid(row=3, column=0, padx=20, pady=(20, 10))
# reccoms = show_recomm()
# reccoms.partitionDataByCpu()
