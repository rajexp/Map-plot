#!/usr/bin/env python
# Author      : Rajan Chauhan
# Version     : MAP_PLOT 1.0
# Recommended : Use for non-commercial and Educational Purpose
# Contact     : rajanchauhan11@gmail.com
import Tkinter as tk
import cv2
import thread
import urllib
import json
import math
import random
from PIL import Image, ImageTk
global ini_x ,ini_y
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()
        
    def createWidgets(self):
        global ini_x,ini_y
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.frame = tk.Frame(self)
        self.frame.rowconfigure(0,weight=1)
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid(row=0, column=0,columnspan=3,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frame.bind("<Configure>", self.update)
        self.image=cv2.imread('D:\World.jpg')
        self.original=Image.fromarray(self.image)
        resized = self.original.resize((ini_x,ini_y),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        
        self.map=tk.Label(self,image=self.img)
        self.map.rowconfigure(0,weight=1)
        self.map.columnconfigure(0,weight=1)
        self.map.grid(row=0,column=0,in_=self.frame,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.place=tk.StringVar()
        
        self.search_label=tk.Label(self,text="")
        self.search_label.grid(row=1,column=0,sticky=tk.N+tk.W)
        self.label=tk.Label(self,text="Find Places on Map : ")
        self.label.grid(row=1,column=1,sticky=tk.N+tk.E)
        self.w=tk.Entry(self,textvariable=self.place,highlightcolor="skyblue",highlightthickness=2)
        self.w.grid(row=1,column=2,sticky=tk.N+tk.E)
        self.w.bind('<Return>',self.plott)
    def coordinate(self,latitude,longitude):
        mapWidth  = self.image.shape[1]
        mapHeight = self.image.shape[0]
        x = int((longitude+180)*(mapWidth/360))
        latRad = latitude*math.pi/180;
        mercN = math.log(math.tan((math.pi/4)+(latRad/2)),math.e)
        y     = int((mapHeight/2)-(mapWidth*mercN/(2*math.pi)))+238
        cv2.circle(self.image,(x,y),3,(random.randint(50,255),random.randint(50,255),random.randint(100,255)),3)
    def get_latnlng(self,address):
        if len(address) < 1 :
            return
        serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
        url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
        try:
            uh = urllib.urlopen(url)
        except Exception,e:
            self.search_label.configure(text="Internet Connection Error")
            print e
        data = uh.read().decode('utf-8')
        print ('Retrieved',len(data),'characters')
        tree = json.loads(data)
        results = tree['results']
        try:
            id = results[0]['place_id']
            lat=results[0]['geometry']['location']['lat']
            lon=results[0]['geometry']['location']['lng']
        except:
            self.search_label.configure(text="No such place Found")
            #No place existed hence returning these values
            return 361,361
        return lat,lon
    def update(self,event=None):
        self.print_on_map()
    def print_on_map(self,event=None):
        x=self.frame.winfo_width()
        y=self.frame.winfo_height()
        self.original=Image.fromarray(self.image)
        resized = self.original.resize((x-4, y-4),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        self.map=tk.Label(self,image=self.img)
        self.map.grid(row=0,column=0,in_=self.frame,sticky=tk.N+tk.S+tk.E+tk.W)

    def plott(self ,event=None):
        address = str(self.w.get())
        if len(address)<1:
            self.w.configure(highlightcolor="red")
        else:
            self.search_label.configure(text=address)
            self.w.configure(highlightcolor="green")
        self.w.delete(0,len(self.w.get()))
        x,y=self.get_latnlng(address)
        self.coordinate(x,y)
        self.print_on_map()
ini_x=800
ini_y=600
app = Application()
app.master.title('World')
thread.start_new_thread(app.mainloop())
