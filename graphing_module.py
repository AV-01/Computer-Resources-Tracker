import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import matplotlib.dates as md

def graphing(perVizVar, colorMode):
    root = ctk.CTk()
    root.geometry("1150x580")
    root.title("Dynamic Scatterplot")
    ctk.set_appearance_mode(colorMode)
    compDf = pd.read_csv("computer_data.csv")
    procData = pd.read_csv("process_data.csv")

    if perVizVar == "Minutes":
        times = pd.to_datetime(compDf.time)
        compDf = compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
        compDf.index = pd.to_datetime(compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    else:
        compDf.index = compDf['time']

    compDf['date_only'] = pd.to_datetime(compDf.index)
    date_only = compDf['date_only'].dt.date
    num_days = len(date_only.unique())
    print(num_days)
    compDf.dropna(inplace=True)
    # compDf.index = compDf['time']

    # compDf.index.to_series().dt.strftime('%Y-%m-%d')
    # compDf.index.to_series().apply(lambda x: x.strftime('%Y-%m-%d'))
    # compDf.index.to_series().apply(lambda x: x.strftime('%Y-%m-%d'))
    cpuFigure = plt.Figure(figsize=(6,3), dpi=100)
    cpuPlot = cpuFigure.add_subplot(111)
    cpuPlot.plot(compDf.index.astype(str),compDf['cpu'])
    # cpuPlot.plot(compDf.index,compDf['cpu'])
    cpuPlot.set_title("CPU Percentage over time")
    # cpuPlot.ylim(0,100)
    cpuPlot.set_ylabel("CPU Percentage")
    cpuPlot.set_xlabel("Time")

    # cpuPlot.xaxis_date()

    # Make space for and rotate the x-axis tick labels
    # cpuPlot.tick_params(labelrotation=45)
    cpuPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    cpuFigure.tight_layout()

    chart_type = FigureCanvasTkAgg(cpuFigure, root)
    chart_type.get_tk_widget().grid(row=0,column=0)

    ramFigure = plt.Figure(figsize=(6,3), dpi=100)
    ramPlot = ramFigure.add_subplot(111)
    ramPlot.set_title("RAM Percentage over time")
    ramPlot.set_ylabel("RAM Percentage")
    ramPlot.set_xlabel("Time")

    # ramPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    ramPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    # ramPlot.ylim(0,100)
    ramPlot.plot(compDf.index.astype(str),compDf['ram percent'])
    ramFigure.tight_layout()
    chart_type = FigureCanvasTkAgg(ramFigure, root)
    chart_type.get_tk_widget().grid(row=1,column=0)

    networkFigure = plt.Figure(figsize=(6,3), dpi=100)
    networkPlot = networkFigure.add_subplot(111)
    networkPlot.set_title("Network Usage in mb")
    networkPlot.set_ylabel("Megabytes")
    networkPlot.set_xlabel("Time")
    # networkPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    networkPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))

    # ramPlot.ylim(0,100)
    networkPlot.plot(compDf.index.astype(str),compDf['net_in'],label="Recieve")
    networkPlot.plot(compDf.index.astype(str),compDf['net_out'],label="Send")
    networkPlot.legend(loc='upper left')
    networkFigure.tight_layout()
    chart_type = FigureCanvasTkAgg(networkFigure, root)
    chart_type.get_tk_widget().grid(row=0,column=1)

    topProcesses = list(dict(procData['name'].value_counts()[:4]).keys())
    if perVizVar == "Minutes":
        df1 = procData[procData['name']==topProcesses[0]]
        times = pd.to_datetime(df1.time)
        df1 = df1.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
        df1.index = pd.to_datetime(df1.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

        df2 = procData[procData['name']==topProcesses[1]]
        times = pd.to_datetime(df2.time)
        df2 = df2.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
        df2.index = pd.to_datetime(df2.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

        df3 = procData[procData['name']==topProcesses[2]]
        times = pd.to_datetime(df3.time)
        df3 = df3.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
        df3.index = pd.to_datetime(df3.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))

        df4 = procData[procData['name']==topProcesses[3]]
        times = pd.to_datetime(df4.time)
        df4 = df4.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
        df4.index = pd.to_datetime(df4.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    else:
        df1 = procData[procData['name']==topProcesses[0]]
        df2 = procData[procData['name']==topProcesses[1]]
        df3 = procData[procData['name']==topProcesses[2]]
        df4 = procData[procData['name']==topProcesses[3]]
        df1.index = df1['time']
        df2.index = df2['time']
        df3.index = df3['time']
        df4.index = df4['time']

    processesFigure = plt.Figure(figsize=(6,3), dpi=100)

    processPlot = processesFigure.add_subplot(221)
    processPlot.set_title("RAM usage of processes in mb")
    processPlot.set_ylabel("RAM mb")
    processPlot.xaxis.set_major_locator(plt.MaxNLocator(num_days))
    # processPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # processPlot.xaxis.set_major_locator(md.MinuteLocator(interval = 5))

    processPlot.plot(df1.index.astype(str),df1['vms'],label=topProcesses[0])
    processPlot.legend(loc='upper left')

    processPlot2 = processesFigure.add_subplot(222)
    # processPlot2.set_title("RAM usage of processes in mb")
    processPlot2.set_ylabel("RAM mb")
    processPlot2.xaxis.set_major_locator(plt.MaxNLocator(num_days))
    # processPlot2.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # processPlot2.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    processPlot2.plot(df2.index.astype(str),df2['vms'],label=topProcesses[1])
    processPlot2.legend(loc='upper left')

    processPlot3 = processesFigure.add_subplot(223)
    # processPlot3.set_title("RAM usage of processes in mb")
    processPlot3.set_ylabel("RAM mb")
    processPlot3.xaxis.set_major_locator(plt.MaxNLocator(num_days))
    # processPlot3.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # processPlot3.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    processPlot3.plot(df3.index.astype(str),df3['vms'],label=topProcesses[2])
    processPlot3.legend(loc='upper left')

    processPlot4 = processesFigure.add_subplot(224)
    # processPlot4.set_title("RAM usage of processes in mb")
    # processPlot4.set_ylabel("RAM mb")
    processPlot4.xaxis.set_major_locator(plt.MaxNLocator(num_days))
    # processPlot4.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # processPlot4.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    processPlot4.plot(df4.index.astype(str),df4['vms'],label=topProcesses[3])
    processPlot4.legend(loc='upper left')

    processesFigure.tight_layout()

    chart_type = FigureCanvasTkAgg(processesFigure, root)
    chart_type.get_tk_widget().grid(row=1,column=1)

    root.mainloop()

# perVizVar = "Minutes"
# graphing(perVizVar, "Dark")
