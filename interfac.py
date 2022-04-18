#import explorerhat

import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from control.matlab import *
from tkinter import *
import tkinter as tk
def getValue(value):
    print(value)


def Stop ():
    print ('STOP Motor  avec ki=',Ki.get(),'Kd=',Kd.get())
def Start():
    w0 = 22.511
    m = 0.6865
    K = 1.2
    tau = 0.4
    N = 15000
    T = np.linspace(0, 15, N)
    T0 = 0.26
#Fonction de transfert d'ordre 3 
    num3 = np.array([K * w0 ** 2])
    den3 = np.convolve([tau, 1], [1, 2 * w0 * m, w0 ** 2])
    H3 = tf(num3, den3)
    print('H3(S)', H3)
    ### Correcteur PID ###
    kpi = Ki.get()
    kpid = Kd.get()
    taud = 0.125 * T0
    Tpid = 0.5 * T0
    num = [kpi * Tpid * taud, kpi * Tpid, kpid]
    den = np.array([Tpid, 0])
    H = tf(num, den)
    Hpid3 = H3 * H
    print('Hpid3(S)', Hpid3)
    HBFpid3 = feedback(Hpid3, 1)
    print('HBFpid3(S)', HBFpid3)
    Y3, T = step(HBFpid3, T)
    Y4, T = impulse(HBFpid3, T)
    fig = Figure(figsize=(1, 1), dpi=100)
    fig.add_subplot(121).plot(T, Y3)
    fig.add_subplot(122).plot(T, Y4)
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
############GUI########################################
 #Creer une premiere fenetre 
# window=Tk()
#personnaliser cette fenetre 
master = Tk(className=' GUI for MCC Control ')
master.geometry("870x670")
master.minsize(870,670)
master.maxsize(870,670)
master.config(background='#BEDFEC')
#master.iconbitmap("isimm.ico")
#Créer la frame 
frame=Frame(master,bg='#41B77F')

#label 
label_title=Label(master, text="Welcome to GUI for MCC control ",font=("Courrier",40),bg='#BEDFEC',fg='#696969')
label_title.pack()

#Création des boutons 
StartButton=tk.Button(master, text='Start',font=("Courrier",15),fg="#CEE7F1",bg="#4682B4",command=Start,width=15, height=3).place(x=30, y=202)
StopButton=tk.Button(master, text='Stop',font=("Courrier",15), fg="#CEE7F1",bg="#4682B4",command=Stop,width=15, height=3).place(x=665, y=202)


#tk.Label(master,text="""  """,fg="white",bg="#9ACD32", justify = tk.LEFT, padx = 400,pady=5,relief=SUNKEN).pack()


#Création des sliders 
tk.Label(master,text="""Choisir la valeur de Ki:""",fg="#4682B4",bg="#BEDFEC", justify = tk.LEFT, padx = 121,pady=10,font=("Arial",14)).pack()
Ki=Scale(master,label="Ki",from_=0,to=10, command=getValue,fg="#CEE7F1",bg="#4682B4",activebackground="#CEE7F1",troughcolor="white",orient=HORIZONTAL ,length=400)
Ki.set(5)#initial value
Ki.pack()


tk.Label(master,text="""Choisir la valeur de Kd:""",fg="#4682B4",bg="#BEDFEC", justify = tk.LEFT, padx = 121,pady=10,font=("Arial",14)).pack()
Kd=Scale(master,label="Kd",from_=0,to=10, command=getValue,fg="#CEE7F1",bg="#4682B4",activebackground="#CEE7F1",troughcolor="white",orient=HORIZONTAL ,length=400)
Kd.set(5)#initial value
Kd.pack()


tk.Label(master,text="""Choisir la valeur de Kp:""",fg="#4682B4",bg="#BEDFEC", justify = tk.LEFT, padx = 121,pady=10,font=("Arial",14)).pack()
Kd=Scale(master,label="Kp",from_=0,to=10, command=getValue,fg="#CEE7F1",bg="#4682B4",activebackground="#CEE7F1",troughcolor="white",orient=HORIZONTAL ,length=400)
Kd.set(5)#initial value
Kd.pack()

tk.Label(master,text="""  """,fg="white",bg="#BEDFEC", justify = tk.LEFT, padx = 400,pady=1).pack()
#tk.Label(master,text="""Courbes:""",fg="#4682B4",bg="#BEDFEC", justify = tk.LEFT, padx = 360,pady=5,font=("Arial",15)).pack()


#creation d'une barre de menu
menu_bar =Menu(master) 
#creer un premier menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Start", command=Start)
file_menu.add_command(label="Stop", command=Stop)
file_menu.add_command(label="Quitter", command=master.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

#configuration de l'ajout cu menu bar
master.config(menu=menu_bar)
#affichage 
master.mainloop()
