import customtkinter
import os
import csv
import threading
import write_data
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as md
import test3 as  graphing_module
import graphing_module as static_graphing
import user_reccom

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.title("Resource Tracker")
root.geometry("1100x580")

root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

publicDataCooldown = 10
getCPU = True
getRAM = True
getNetwork = True
getProcess = True
run = False
quiting = False
perVizVar = "Minutes"
currentColorMode = "Dark"

def changeViz(choice):
    global perVizVar
    perVizVar = choice
    print(choice)

def dataCollecting():
    while not quiting:
        if run:
            print(publicDataCooldown)
            compSizeTitle.configure(text="Computer Data(CPU, RAM, Network): "+compFileSize()+" kb")
            procSizeTitle.configure(text = "Process Data: "+procFileSize()+" kb")
            fileSizeTitle.configure(text="Total Data Collected(kb): "+getFileSize())
            write_data.write_data(getCPU, getRAM, getNetwork, getProcess)
            time.sleep(publicDataCooldown)
        else:
            print(publicDataCooldown)
            time.sleep(publicDataCooldown)

def createStaticViz():
    static_graphing.graphing(perVizVar, "Dark")

def createDataViz():
    global perVizVar
    graphing_module.fullGraphCreation("Minutes","Dark",5)

def displayZombie():
    user_reccom.show_recomm()
    # vizWindow = customtkinter.CTkToplevel(root)
    # vizWindow.geometry("1150x580")
    # vizWindow.title("Visualizations")
    # compDf = pd.read_csv("computer_data.csv")
    # procData = pd.read_csv("process_data.csv")
    #
    # if perVizVar == "Minutes":
    #     times = pd.to_datetime(compDf.time)
    #     compDf = compDf.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
    #     compDf.index = pd.to_datetime(compDf.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    # else:
    #     compDf.index = compDf['time']
    # # compDf.index = compDf['time']
    #
    # cpuFigure = plt.Figure(figsize=(6,3), dpi=100)
    # cpuPlot = cpuFigure.add_subplot(111)
    # cpuPlot.plot(compDf.index,compDf['cpu'])
    # cpuPlot.set_title("CPU Percentage over time")
    # # cpuPlot.ylim(0,100)
    # cpuPlot.set_ylabel("CPU Percentage")
    # cpuPlot.set_xlabel("Time")
    #
    # cpuPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # cpuFigure.tight_layout()
    # chart_type = FigureCanvasTkAgg(cpuFigure, vizWindow)
    # chart_type.get_tk_widget().grid(row=0,column=0)
    #
    # ramFigure = plt.Figure(figsize=(6,3), dpi=100)
    # ramPlot = ramFigure.add_subplot(111)
    # ramPlot.set_title("RAM Percentage over time")
    # ramPlot.set_ylabel("RAM Percentage")
    # ramPlot.set_xlabel("Time")
    #
    # ramPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    #
    # # ramPlot.ylim(0,100)
    # ramPlot.plot(compDf.index,compDf['ram percent'])
    # ramFigure.tight_layout()
    # chart_type = FigureCanvasTkAgg(ramFigure, vizWindow)
    # chart_type.get_tk_widget().grid(row=1,column=0)
    #
    # networkFigure = plt.Figure(figsize=(6,3), dpi=100)
    # networkPlot = networkFigure.add_subplot(111)
    # networkPlot.set_title("Network Usage in mb")
    # networkPlot.set_ylabel("Megabytes")
    # networkPlot.set_xlabel("Time")
    # networkPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    #
    # # ramPlot.ylim(0,100)
    # networkPlot.plot(compDf.index,compDf['net_in'],label="Recieve")
    # networkPlot.plot(compDf.index,compDf['net_out'],label="Send")
    # networkPlot.legend(loc='upper left')
    # networkFigure.tight_layout()
    # chart_type = FigureCanvasTkAgg(networkFigure, vizWindow)
    # chart_type.get_tk_widget().grid(row=0,column=1)
    #
    # topProcesses = list(dict(procData['name'].value_counts()[:4]).keys())
    # if perVizVar == "Minutes":
    #     df1 = procData[procData['name']==topProcesses[0]]
    #     times = pd.to_datetime(df1.time)
    #     df1 = df1.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
    #     df1.index = pd.to_datetime(df1.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    #
    #     df2 = procData[procData['name']==topProcesses[1]]
    #     times = pd.to_datetime(df2.time)
    #     df2 = df2.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
    #     df2.index = pd.to_datetime(df2.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    #
    #     df3 = procData[procData['name']==topProcesses[2]]
    #     times = pd.to_datetime(df3.time)
    #     df3 = df3.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
    #     df3.index = pd.to_datetime(df3.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    #
    #     df4 = procData[procData['name']==topProcesses[3]]
    #     times = pd.to_datetime(df4.time)
    #     df4 = df4.groupby([times.dt.year,times.dt.month,times.dt.day,times.dt.hour, times.dt.minute]).mean()
    #     df4.index = pd.to_datetime(df4.index.map(lambda x: '{}/{}/{} {}:{}:00'.format(x[1], x[2],x[0],x[3],x[4])))
    # else:
    #     df1 = procData[procData['name']==topProcesses[0]]
    #     df2 = procData[procData['name']==topProcesses[1]]
    #     df3 = procData[procData['name']==topProcesses[2]]
    #     df4 = procData[procData['name']==topProcesses[3]]
    #     df1.index = df1['time']
    #     df2.index = df2['time']
    #     df3.index = df3['time']
    #     df4.index = df4['time']
    #
    # processesFigure = plt.Figure(figsize=(6,3), dpi=100)
    #
    # processPlot = processesFigure.add_subplot(221)
    # processPlot.set_title("RAM usage of processes in mb")
    # processPlot.set_ylabel("RAM mb")
    # processPlot.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # # processPlot.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    #
    # processPlot.plot(df1.index,df1['vms'],label=topProcesses[0])
    # processPlot.legend(loc='upper left')
    #
    # processPlot2 = processesFigure.add_subplot(222)
    # # processPlot2.set_title("RAM usage of processes in mb")
    # processPlot2.set_ylabel("RAM mb")
    # processPlot2.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # # processPlot2.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    # processPlot2.plot(df2.index,df2['vms'],label=topProcesses[1])
    # processPlot2.legend(loc='upper left')
    #
    # processPlot3 = processesFigure.add_subplot(223)
    # # processPlot3.set_title("RAM usage of processes in mb")
    # processPlot3.set_ylabel("RAM mb")
    # processPlot3.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # # processPlot3.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    # processPlot3.plot(df3.index,df3['vms'],label=topProcesses[2])
    # processPlot3.legend(loc='upper left')
    #
    # processPlot4 = processesFigure.add_subplot(224)
    # # processPlot4.set_title("RAM usage of processes in mb")
    # # processPlot4.set_ylabel("RAM mb")
    # processPlot4.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # # processPlot4.xaxis.set_major_locator(md.MinuteLocator(interval = 5))
    # processPlot4.plot(df4.index,df4['vms'],label=topProcesses[3])
    # processPlot4.legend(loc='upper left')
    #
    # processesFigure.tight_layout()
    #
    # chart_type = FigureCanvasTkAgg(processesFigure, vizWindow)
    # chart_type.get_tk_widget().grid(row=1,column=1)

mainThread = threading.Thread(target=dataCollecting)

def saveChangesDataCollection():
    global publicDataCooldown
    global getCPU
    global getRAM
    global getNetwork
    global getProcess
    publicDataCooldown = round(eraseSlider.get())
    print(publicDataCooldown)
    if cpu_checkbox.get() == 1:
        getCPU = True
        print("get cpu true")
    else:
        getCPU = False
        print('get cpu false')
    if ram_checkbox.get() == 1:
        getRAM = True
        print("get ram true")
    else:
        getRAM = False
        print('get ram false')
    if network_checkbox.get() == 1:
        getNetwork = True
        print("get network true")
    else:
        getNetwork = False
        print('get network false')
    if process_checkbox.get() == 1:
        getProcess = True
        print("get process true")
    else:
        getProcess = False
        print('get process false')
    # getCPU =

def tracking():
    global run
    if run == True:
        run = False
    elif run == False:
        run = True

def changeAppearence(new_appearance_mode: str):
    global currentColorMode
    currentColorMode = new_appearance_mode
    customtkinter.set_appearance_mode(new_appearance_mode)

def changeScaling(new_scaling: str):
    new_scaling_float = int(new_scaling) / 100
    customtkinter.set_widget_scaling(new_scaling_float)
    scaling_label.configure(text="Zoom: " + str(round(scaling_optionemenu.get()))+"%")
def updateCooldown(newCooldown):
    # global publicDataCooldown
    # publicDataCooldown = round(newCooldown)
    deleteDataTitle.configure(text = "Data Collection Cooldown in seconds: "+str(round(newCooldown)))

def getFileSize():
    compDataSize = os.path.getsize('C:\\Users\\aryav\\Downloads\\Programming Projects\\Python\\Resource Tracker\\computer_data.csv')
    procDataSize = os.path.getsize('C:\\Users\\aryav\\Downloads\\Programming Projects\\Python\\Resource Tracker\\process_data.csv')
    totalSize = compDataSize+procDataSize
    return str(round(totalSize/1000))

def compFileSize():
    compDataSize = os.path.getsize('C:\\Users\\aryav\\Downloads\\Programming Projects\\Python\\Resource Tracker\\computer_data.csv')
    return str(round(compDataSize/1000))

def procFileSize():
    compDataSize = os.path.getsize('C:\\Users\\aryav\\Downloads\\Programming Projects\\Python\\Resource Tracker\\process_data.csv')
    return str(round(compDataSize/1000))

def deleteCompDataFileData():
    open('computer_data.csv', 'w').close()
    compHeader = ['time','cpu','net_in','net_out','ram percent','ram gb']
    with open('computer_data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(compHeader)
    compSizeTitle.configure(text="Computer Data (CPU, RAM, Network): "+compFileSize()+" kb")
    procSizeTitle.configure(text = "Process Data: "+procFileSize()+" kb")
    fileSizeTitle.configure(text="Total Data Collected (kb): "+getFileSize())

def deleteProcDataFileData():
    open('process_data.csv', 'w').close()
    procHeader = ['time','name','pid','mem','vms','cpu']
    with open('process_data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(procHeader)
    compSizeTitle.configure(text="Computer Data (CPU, RAM, Network): "+compFileSize()+" kb")
    procSizeTitle.configure(text = "Process Data: "+procFileSize()+" kb")
    fileSizeTitle.configure(text="Total Data Collected (kb): "+getFileSize())

sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
title = customtkinter.CTkLabel(sidebar_frame, text="Resource Tracker", font=customtkinter.CTkFont(size=20, weight="bold"))
title.grid(row=0, column=0, padx=20, pady=(20, 10))
sidebar_button_1 = customtkinter.CTkButton(sidebar_frame,text="Create Visualizations (Dynamic)",command = createDataViz)
sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
sidebar_button_2 = customtkinter.CTkButton(sidebar_frame,text="Create Visualizations (Static)",command = createStaticViz)
sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
showZombieButton = customtkinter.CTkButton(sidebar_frame,text="Zombie Resources",command = displayZombie)
showZombieButton.grid(row=3, column=0, padx=20, pady=10)
trackData = customtkinter.CTkSwitch(master=sidebar_frame,text="Track Resource Data",command=tracking)
trackData.grid(row=4, column=0, padx=20, pady=10)
appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                               command=changeAppearence)
# scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                       # command=changeScaling)
# scaling_optionemenu = customtkinter.CTkSlider(sidebar_frame, from_=50, to=150, command=changeScaling)
# scaling_optionemenu.set(100)
# scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
appearance_mode_optionemenu.set("Dark")
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
# scaling_label = customtkinter.CTkLabel(sidebar_frame, text="Zoom: " + str(scaling_optionemenu.get())+"%" , anchor="w")
# scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

userguide_frame = customtkinter.CTkFrame(root)
userguide_frame.grid(row=0, column=1, padx=(20, 20), columnspan=1,pady=(20, 0), sticky="nsew")
userguide_frame.grid_columnconfigure(1, weight=2)
userguide_frame.grid_columnconfigure((2, 3), weight=0)
userguid_title = customtkinter.CTkLabel(userguide_frame, text="User Guide", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
userguid_title.pack(pady=(20,0))
tabview = customtkinter.CTkTabview(userguide_frame,width=userguide_frame.cget('width'))
tabview.pack(expand=1, fill="both", padx=(20,20), pady=(0, 20))
# tabview.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
tabview.add("Basic Info")
tabview.add("Visualizations")
tabview.add("Privacy Policy")
tabview.add("Misc.")
# The whole idea of this program is to monitor your computer's health and give you data in the form of visualizations. There are many ways to interpret this data, but ultimately it will be up to you to look and understand what the data means. All of the code is written in \nPython, and we collect the data in the background while you use your computer to do your business. All the data is stored locally in a text file.
basicInfo = customtkinter.CTkLabel(tabview.tab('Basic Info'), text = "The whole idea of this program is to monitor your computer's health and give you data in the form of visualizations. There are many ways \nto interpret this data, but ultimately it will be up to you to look and understand what the data means. All of the code is written in \nPython, and we collect the data in the background while you use your computer to do your business. All the data is stored locally in a text \nfile, so the data can only be accessed on this computer. Only you have the data and only you can look at the data visualizations. This \nprogram was created for monitoring resource data over a long period of time, so it will take a while before this program is able to have all \nthe data it needs. If this program takes up too much space, there is an option to cleanse the data so that it takes less space, but since all \nthe data is stored as a text file, the data will never take up too much space.",justify='left')
basicInfo.grid(row=0,column=0,pady=(10,0))
vizInfo = customtkinter.CTkLabel(tabview.tab('Visualizations'), text = "The data is going to be shown in multiple forms of visualizations. However, the main graph is going to be line graphs. Depending on how \nmuch data there is, the graph can be for minutes, hours, and even weeks. It all depends on how much data there is. The visualizations \nwill show all the data for CPU usage, RAM usage, Network usage, and process data. For more information about what that means, look \ninto the \"Misc.\" To see the visualizations, just click the \"Create Visualizations\" button on the far left. It will create the visualizations with \nthe most up-to-date visualizations possible by opening them in a new window.",justify='left')
vizInfo.grid(row=0,column=0,pady=(10,0))
vizInfo = customtkinter.CTkLabel(tabview.tab('Privacy Policy'), text = "Your data belongs to you and is stored on your computer. We will not sell your data to third parties. This is less a policy and more of a \npromise that we aren't bad guys that are stealing your data.",justify='left')
vizInfo.grid(row=0,column=0,pady=(10,0))
miscInfo = customtkinter.CTkLabel(tabview.tab('Misc.'), text = "To start monitoring your resource usage, turn on the switch that's on the far left. The monitoring will stop if this window is closed. \n\\nThere are many ways to interpret the results being shown. However, the easiest way is to look at CPU and RAM usage. CPU is the brain \nof your computer and RAM is the short term memory. CPU allows your computer to do all the work it needs to do, and RAM allows that \nwork to be done quickly. If you consistently have high CPU and RAM usage, that means your computer is consistently working hard, \nwhich means it may run slowly. Network usage data is also collected, along with information about what applications were being run at \nthe time. You can use this information to see which programs use the most CPU and RAM, and when you're using the internet the most. \nKeep in mind that the data can mean a lot of things!",justify='left')
miscInfo.grid(row=0,column=0,pady=(10,0))

# tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
# tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

settings_frame = customtkinter.CTkFrame(root)
settings_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
userguid_title = customtkinter.CTkLabel(settings_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
userguid_title.pack(pady=(20,0))
settings_tabview = customtkinter.CTkTabview(settings_frame,width=userguide_frame.cget('width'))
settings_tabview.pack(expand=1, fill="both", padx=(20,20), pady=(0, 20))
# settings_tabview.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
settings_tabview.add("General")
settings_tabview.add("Data Collection")
# settings_tabview.add("Visualizations")

fileSizeTitle = customtkinter.CTkLabel(settings_tabview.tab("General"), text="Total Data Collected (kb): "+getFileSize(), font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
fileSizeTitle.grid(row=0,column=1,pady=5)
compSizeTitle = customtkinter.CTkLabel(settings_tabview.tab("General"), text="Computer Data (CPU, RAM, Network): "+compFileSize()+" kb", font=customtkinter.CTkFont(size=15), anchor="center")
compSizeTitle.grid(row=1,column=0,pady=5)
deleteCompData = customtkinter.CTkButton(settings_tabview.tab("General"),text="Delete All Computer Data",command=deleteCompDataFileData)
deleteCompData.grid(row=2,column=0,pady=5)
procSizeTitle = customtkinter.CTkLabel(settings_tabview.tab("General"), text="Process Data: "+procFileSize()+" kb", font=customtkinter.CTkFont(size=15), anchor="center")
procSizeTitle.grid(row=1,column=2,pady=5,padx=20)
deleteProcData = customtkinter.CTkButton(settings_tabview.tab("General"),text="Delete All Process Data",command=deleteProcDataFileData)
deleteProcData.grid(row=2,column=2,pady=5,padx=20)

dataColTitle = customtkinter.CTkLabel(settings_tabview.tab("Data Collection"), text="Resources to collect:", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
dataColTitle.grid(row=0,column=0,pady=5)
cpu_checkbox = customtkinter.CTkCheckBox(master=settings_tabview.tab("Data Collection"), text="CPU Percentage")
cpu_checkbox.grid(row=1,column=0,pady=5)
cpu_checkbox.select()
ram_checkbox = customtkinter.CTkCheckBox(master=settings_tabview.tab("Data Collection"), text="RAM Usage")
ram_checkbox.grid(row=2,column=0,pady=5)
ram_checkbox.select()
network_checkbox = customtkinter.CTkCheckBox(master=settings_tabview.tab("Data Collection"), text="Network Usage")
network_checkbox.grid(row=1,column=1,pady=5)
network_checkbox.select()
process_checkbox = customtkinter.CTkCheckBox(master=settings_tabview.tab("Data Collection"), text="Process Data")
process_checkbox.grid(row=2,column=1,pady=5)
process_checkbox.select()
dataColSubmit = customtkinter.CTkButton(settings_tabview.tab("Data Collection"),text="Save All Changes", command = saveChangesDataCollection)
dataColSubmit.grid(row=3,column=0,pady=5)
deleteDataTitle = customtkinter.CTkLabel(settings_tabview.tab("Data Collection"), text="Data Collection Cooldown in seconds: 10", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
deleteDataTitle.grid(row=0,column=5,padx=20,pady=5)
eraseSlider = customtkinter.CTkSlider(settings_tabview.tab("Data Collection"), from_=0, to=60,command=updateCooldown)
eraseSlider.set(10)
eraseSlider.grid(row=1,column=5, pady=5, padx=20)

# vizColTitle = customtkinter.CTkLabel(settings_tabview.tab("Visualizations"), text="Create Visualizations per:", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
# vizColTitle.grid(row=0,column=0,pady=5)
# vizOptions = customtkinter.CTkOptionMenu(settings_tabview.tab("Visualizations"), values=["Minutes", "Seconds"], command=changeViz)
# vizOptions.grid(row=1,column=0,pady=5)
# vizWarning = customtkinter.CTkLabel(settings_tabview.tab("Visualizations"), text="Warning: Choosing Seconds will mess up the x axis, but provide more detail.", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
# vizWarning.grid(row=2,column=0,pady=5)
def on_closing():
    global quiting
    quiting = True
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

mainThread.start()
root.mainloop()
