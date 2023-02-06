import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import matplotlib.dates as md
import numpy as np
import matplotlib.animation as animation
import time
import threading

class fullGraphCreation:
    def __init__(self, aggType, colorMode, interval):
        self.aggType = aggType
        self.interval = interval
        self.quiting = False
        self.root = ctk.CTk()
        self.root.geometry("1150x580")
        self.root.title("Dynamic Scatterplot")
        ctk.set_appearance_mode(colorMode)
        self.compDf = pd.read_csv("computer_data.csv")
        self.procData = pd.read_csv("process_data.csv")
        if aggType == "Minutes":
            times = pd.to_datetime(self.compDf.time)
            self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.compDf.index = self.compDf['time']
        self.mainGraphing()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        print("before mainloop")
        # mainThread = threading.Thread(target=self.animate)
        # mainThread.start()
        ani = animation.FuncAnimation(self.cpuFigure,self.cpuUpdate, interval=1000)
        ani2 = animation.FuncAnimation(self.ramFigure,self.ramUpdate, interval=1000)
        ani3 = animation.FuncAnimation(self.networkFigure,self.networkUpdate, interval=1000)
        ani4 = animation.FuncAnimation(self.processesFigure,self.processUpdate, interval=1000)
        # self.testStuff()
        # print('remade')
        print("after thread start")
        self.root.mainloop()
        print("mainloop called")

    def clearAll(self):
        self.cpuPlot.clear()

    def cpuUpdate(self,f):
        self.cpuPlot.clear()
        self.compDf = pd.read_csv("computer_data.csv")
        if self.aggType == "Minutes":
            times = pd.to_datetime(self.compDf.time)
            self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.compDf.index = self.compDf['time']
        self.compDf['date_only'] = pd.to_datetime(self.compDf.index)
        date_only = self.compDf['date_only'].dt.date
        num_days = len(date_only.unique())
        df=self.compDf.dropna(subset=['cpu'])
        self.cpuPlot.plot(df.index.astype(str), df['cpu'])
        self.cpuPlot.set_title("CPU Percentage over time")
        self.cpuPlot.set_ylabel("CPU Percentage")
        self.cpuPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    def ramUpdate(self, f):
        self.ramPlot.clear()
        self.compDf = pd.read_csv("computer_data.csv")
        if self.aggType == "Minutes":
            times = pd.to_datetime(self.compDf.time)
            self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.compDf.index = self.compDf['time']
        self.compDf['date_only'] = pd.to_datetime(self.compDf.index)
        date_only = self.compDf['date_only'].dt.date
        num_days = len(date_only.unique())
        df=self.compDf.dropna(subset=['ram percent'])
        self.ramPlot.plot(df.index.astype(str),df['ram percent'])
        self.ramPlot.set_title("RAM Percentage over time")
        self.ramPlot.set_ylabel("RAM Percentage")
        self.ramPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    def networkUpdate(self,f):
        self.networkPlot.clear()
        self.compDf = pd.read_csv("computer_data.csv")
        if self.aggType == "Minutes":
            times = pd.to_datetime(self.compDf.time)
            self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.compDf.index = self.compDf['time']
        self.compDf['date_only'] = pd.to_datetime(self.compDf.index)
        date_only = self.compDf['date_only'].dt.date
        num_days = len(date_only.unique())
        df=self.compDf.dropna(subset=['net_in'])
        self.networkPlot.plot(df.index.astype(str),df['net_in'],label="Recieve")
        self.networkPlot.plot(df.index.astype(str),df['net_out'],label="Send")
        self.networkPlot.set_title("Network Usage in mb")
        self.networkPlot.set_ylabel("Megabytes")
        self.networkPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    def processUpdate(self,f):
        self.processPlot.clear()
        self.processPlot2.clear()
        self.processPlot3.clear()
        self.processPlot4.clear()
        self.procData = pd.read_csv("process_data.csv")
        topProcesses = list(dict(self.procData['name'].value_counts()[:4]).keys())
        if self.aggType == "Minutes":
            self.df1 = self.procData[self.procData['name']==topProcesses[0]]
            times = pd.to_datetime(self.df1.time)
            self.df1 = self.df1.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df1.index = pd.to_datetime(self.df1.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df2 = self.procData[self.procData['name']==topProcesses[1]]
            times = pd.to_datetime(self.df2.time)
            self.df2 = self.df2.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df2.index = pd.to_datetime(self.df2.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df3 = self.procData[self.procData['name']==topProcesses[2]]
            times = pd.to_datetime(self.df3.time)
            self.df3 = self.df3.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df3.index = pd.to_datetime(self.df3.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df4 = self.procData[self.procData['name']==topProcesses[3]]
            times = pd.to_datetime(self.df4.time)
            self.df4 = self.df4.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df4.index = pd.to_datetime(self.df4.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.df1 = self.procData[self.procData['name']==topProcesses[0]]
            self.df2 = self.procData[self.procData['name']==topProcesses[1]]
            self.df3 = self.procData[self.procData['name']==topProcesses[2]]
            self.df4 = self.procData[self.procData['name']==topProcesses[3]]
            self.df1.index = self.df1['time']
            self.df2.index = self.df2['time']
            self.df3.index = self.df3['time']
            self.df4.index = self.df4['time']

        num_days = 1
        self.processPlot.set_title("RAM usage of processes in mb")
        self.processPlot.set_ylabel("RAM mb")
        self.processPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot.plot(self.df1.index.astype(str),self.df1['vms'],label=topProcesses[0])
        self.processPlot.legend(loc='upper left')
        # print(topProcesses)
        # self.processPlot2.set_title("RAM usage of processes in mb")
        # self.processPlot2.set_ylabel("RAM mb")
        self.processPlot2.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot2.plot(self.df2.index.astype(str),self.df2['vms'],label=topProcesses[1])
        self.processPlot2.legend(loc='upper left')

        # self.processPlot3.set_title("RAM usage of processes in mb")
        self.processPlot3.set_ylabel("RAM mb")
        self.processPlot3.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot3.plot(self.df3.index.astype(str),self.df3['vms'],label=topProcesses[2])
        self.processPlot3.legend(loc='upper left')

        # self.processPlot4.set_title("RAM usage of processes in mb")
        # self.processPlot4.set_ylabel("RAM mb")
        self.processPlot4.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot4.plot(self.df4.index.astype(str),self.df4['vms'],label=topProcesses[3])
        self.processPlot4.legend(loc='upper left')

    def testStuff(self,f):
        self.cpuPlot.clear()
        self.ramPlot.clear()
        self.networkPlot.clear()
        self.processPlot.clear()
        self.processPlot2.clear()
        self.processPlot3.clear()
        self.processPlot4.clear()
        self.compDf = pd.read_csv("computer_data.csv")
        self.procData = pd.read_csv("process_data.csv")
        if self.aggType == "Minutes":
            times = pd.to_datetime(self.compDf.time)
            self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.compDf.index = self.compDf['time']
        self.compDf['date_only'] = pd.to_datetime(self.compDf.index)
        date_only = self.compDf['date_only'].dt.date
        num_days = len(date_only.unique())

        self.cpuPlot.plot(self.compDf.index.astype(str), self.compDf['cpu'])
        self.cpuPlot.set_title("CPU Percentage over time")
        self.cpuPlot.set_ylabel("CPU Percentage")
        # self.cpuPlot.set_xlabel("Time")
        self.cpuPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

        self.ramPlot.plot(self.compDf.index.astype(str),self.compDf['ram percent'])
        self.ramPlot.set_title("RAM Percentage over time")
        self.ramPlot.set_ylabel("RAM Percentage")
        # self.ramPlot.set_xlabel("Time")
        self.ramPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        # self.ramFigure.tight_layout()

        self.networkPlot.plot(self.compDf.index.astype(str),self.compDf['net_in'],label="Recieve")
        self.networkPlot.plot(self.compDf.index.astype(str),self.compDf['net_out'],label="Send")
        self.networkPlot.set_title("Network Usage in mb")
        self.networkPlot.set_ylabel("Megabytes")
        # self.networkPlot.set_xlabel("Time")
        self.networkPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

        topProcesses = list(dict(self.procData['name'].value_counts()[:4]).keys())
        if self.aggType == "Minutes":
            self.df1 = self.procData[self.procData['name']==topProcesses[0]]
            times = pd.to_datetime(self.df1.time)
            self.df1 = self.df1.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df1.index = pd.to_datetime(self.df1.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df2 = self.procData[self.procData['name']==topProcesses[1]]
            times = pd.to_datetime(self.df2.time)
            self.df2 = self.df2.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df2.index = pd.to_datetime(self.df2.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df3 = self.procData[self.procData['name']==topProcesses[2]]
            times = pd.to_datetime(self.df3.time)
            self.df3 = self.df3.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df3.index = pd.to_datetime(self.df3.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

            self.df4 = self.procData[self.procData['name']==topProcesses[3]]
            times = pd.to_datetime(self.df4.time)
            self.df4 = self.df4.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
            self.df4.index = pd.to_datetime(self.df4.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
        else:
            self.df1 = self.procData[self.procData['name']==topProcesses[0]]
            self.df2 = self.procData[self.procData['name']==topProcesses[1]]
            self.df3 = self.procData[self.procData['name']==topProcesses[2]]
            self.df4 = self.procData[self.procData['name']==topProcesses[3]]
            self.df1.index = self.df1['time']
            self.df2.index = self.df2['time']
            self.df3.index = self.df3['time']
            self.df4.index = self.df4['time']

        num_days = 1
        self.processPlot.set_title("RAM usage of processes in mb")
        self.processPlot.set_ylabel("RAM mb")
        self.processPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot.plot(self.df1.index.astype(str),self.df1['vms'],label=topProcesses[0])
        self.processPlot.legend(loc='upper left')
        # print(topProcesses)
        # self.processPlot2.set_title("RAM usage of processes in mb")
        # self.processPlot2.set_ylabel("RAM mb")
        self.processPlot2.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot2.plot(self.df2.index.astype(str),self.df2['vms'],label=topProcesses[1])
        self.processPlot2.legend(loc='upper left')

        # self.processPlot3.set_title("RAM usage of processes in mb")
        self.processPlot3.set_ylabel("RAM mb")
        self.processPlot3.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot3.plot(self.df3.index.astype(str),self.df3['vms'],label=topProcesses[2])
        self.processPlot3.legend(loc='upper left')

        # self.processPlot4.set_title("RAM usage of processes in mb")
        # self.processPlot4.set_ylabel("RAM mb")
        self.processPlot4.xaxis.set_major_locator(plt.MaxNLocator(num_days))
        self.processPlot4.plot(self.df4.index.astype(str),self.df4['vms'],label=topProcesses[3])
        self.processPlot4.legend(loc='upper left')
        # time.sleep(self.interval)
        # self.cpuPlot.clear()
    def mainGraphing(self):
        self.cpuFigure = plt.Figure(figsize=(6,3), dpi=100)
        self.cpuPlot = self.cpuFigure.add_subplot(111)

        self.ramFigure = plt.Figure(figsize=(6,3), dpi=100)
        self.ramPlot = self.ramFigure.add_subplot(111)

        self.networkFigure = plt.Figure(figsize=(6,3), dpi=100)
        self.networkPlot = self.networkFigure.add_subplot(111)

        self.cpuCanvas = FigureCanvasTkAgg(self.cpuFigure, self.root)
        self.cpuCanvas.get_tk_widget().grid(row=0,column=0)
        self.ramCanvas = FigureCanvasTkAgg(self.ramFigure, self.root)
        self.ramCanvas.get_tk_widget().grid(row=1,column=0)
        self.networkCanvas = FigureCanvasTkAgg(self.networkFigure, self.root)
        self.networkCanvas.get_tk_widget().grid(row=0,column=1)

        self.processesFigure = plt.Figure(figsize=(6,3), dpi=100)
        self.processPlot = self.processesFigure.add_subplot(221)
        self.processPlot2 = self.processesFigure.add_subplot(222)
        self.processPlot3 = self.processesFigure.add_subplot(223)
        self.processPlot4 = self.processesFigure.add_subplot(224)
        self.processCanvas = FigureCanvasTkAgg(self.processesFigure, self.root)
        self.processCanvas.get_tk_widget().grid(row=1,column=1)
    def on_closing(self):
        self.quiting = True
        self.root.destroy()

    def animate(self,f):
            print("called")
            self.compDf = pd.read_csv("computer_data.csv")
            self.procData = pd.read_csv("process_data.csv")
            if self.aggType == "Minutes":
                times = pd.to_datetime(self.compDf.time)
                self.compDf = self.compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
                self.compDf.index = pd.to_datetime(self.compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
            else:
                self.compDf.index = self.compDf['time']
            self.compDf['date_only'] = pd.to_datetime(self.compDf.index)
            date_only = self.compDf['date_only'].dt.date
            num_days = len(date_only.unique())

            self.cpuPlot.plot(self.compDf.index.astype(str), self.compDf['cpu'])
            self.cpuPlot.set_title("CPU Percentage over time")
            self.cpuPlot.set_ylabel("CPU Percentage")
            # self.cpuPlot.set_xlabel("Time")
            self.cpuPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            # self.cpuFigure.tight_layout()
            #
            # self.networkPlot.clear()
            self.ramPlot.plot(self.compDf.index.astype(str),self.compDf['ram percent'])
            self.ramPlot.set_title("RAM Percentage over time")
            self.ramPlot.set_ylabel("RAM Percentage")
            # self.ramPlot.set_xlabel("Time")
            self.ramPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            # self.ramFigure.tight_layout()

            self.networkPlot.plot(self.compDf.index.astype(str),self.compDf['net_in'],label="Recieve")
            self.networkPlot.plot(self.compDf.index.astype(str),self.compDf['net_out'],label="Send")
            self.networkPlot.set_title("Network Usage in mb")
            self.networkPlot.set_ylabel("Megabytes")
            # self.networkPlot.set_xlabel("Time")
            self.networkPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

            topProcesses = list(dict(self.procData['name'].value_counts()[:4]).keys())
            if self.aggType == "Minutes":
                self.df1 = self.procData[self.procData['name']==topProcesses[0]]
                times = pd.to_datetime(self.df1.time)
                self.df1 = self.df1.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
                self.df1.index = pd.to_datetime(self.df1.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

                self.df2 = self.procData[self.procData['name']==topProcesses[1]]
                times = pd.to_datetime(self.df2.time)
                self.df2 = self.df2.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
                self.df2.index = pd.to_datetime(self.df2.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

                self.df3 = self.procData[self.procData['name']==topProcesses[2]]
                times = pd.to_datetime(self.df3.time)
                self.df3 = self.df3.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
                self.df3.index = pd.to_datetime(self.df3.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

                self.df4 = self.procData[self.procData['name']==topProcesses[3]]
                times = pd.to_datetime(self.df4.time)
                self.df4 = self.df4.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
                self.df4.index = pd.to_datetime(self.df4.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
            else:
                self.df1 = self.procData[self.procData['name']==topProcesses[0]]
                self.df2 = self.procData[self.procData['name']==topProcesses[1]]
                self.df3 = self.procData[self.procData['name']==topProcesses[2]]
                self.df4 = self.procData[self.procData['name']==topProcesses[3]]
                self.df1.index = self.df1['time']
                self.df2.index = self.df2['time']
                self.df3.index = self.df3['time']
                self.df4.index = self.df4['time']

            num_days = 1
            self.processPlot.set_title("RAM usage of processes in mb")
            self.processPlot.set_ylabel("RAM mb")
            self.processPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            self.processPlot.plot(self.df1.index.astype(str),self.df1['vms'],label=topProcesses[0])
            self.processPlot.legend(loc='upper left')
            print(topProcesses)
            # self.processPlot2.set_title("RAM usage of processes in mb")
            # self.processPlot2.set_ylabel("RAM mb")
            self.processPlot2.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            self.processPlot2.plot(self.df2.index.astype(str),self.df2['vms'],label=topProcesses[1])
            self.processPlot2.legend(loc='upper left')

            # self.processPlot3.set_title("RAM usage of processes in mb")
            self.processPlot3.set_ylabel("RAM mb")
            self.processPlot3.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            self.processPlot3.plot(self.df3.index.astype(str),self.df3['vms'],label=topProcesses[2])
            self.processPlot3.legend(loc='upper left')

            # self.processPlot4.set_title("RAM usage of processes in mb")
            # self.processPlot4.set_ylabel("RAM mb")
            self.processPlot4.xaxis.set_major_locator(plt.MaxNLocator(num_days))
            self.processPlot4.plot(self.df4.index.astype(str),self.df4['vms'],label=topProcesses[3])
            self.processPlot4.legend(loc='upper left')

            print('updated')
            time.sleep(self.interval)
            self.cpuPlot.clear()
            self.ramPlot.clear()
            self.networkPlot.clear()
            self.processPlot.clear()
            self.processPlot2.clear()
            self.processPlot3.clear()
            self.processPlot4.clear()
            print("end of sleep")
        # ramPlot.clear()
        # ramPlot.plot(compDf.index.astype(str), compDf['cpu'])
        # networkPlot.clear()
        # networkPlot.plot(compDf.index.astype(str), compDf['cpu'])
        # print('updated')
# test = fullGraphCreation("Minutes","Dark",1)
#
#
#     def animate(i):
#         compDf = pd.read_csv('computer_data.csv')
#         times = pd.to_datetime(compDf.time)
#         compDf = compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
#         compDf.index = pd.to_datetime(compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
#         cpuPlot.clear()
#         cpuPlot.plot(compDf.index.astype(str), compDf['cpu'])
#         ramPlot.clear()
#         ramPlot.plot(compDf.index.astype(str), compDf['cpu'])
#         networkPlot.clear()
#         networkPlot.plot(compDf.index.astype(str), compDf['cpu'])
#         print('updated')
#
# # chart_type = FigureCanvasTkAgg(cpuFigure, root)
# # chart_type.get_tk_widget().grid(row=0,column=0)
# mainGraphing("Minutes","Dark",1000)
# ani = animation.FuncAnimation(cpuFigure, animate, interval=1000)
# root.mainloop()
