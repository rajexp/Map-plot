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
        self.pack(fill=tk.BOTH,expand=True)
        self.createWidgets()
        
    def createWidgets(self):
        global ini_x,ini_y        
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X,expand=False)
        self.place=tk.StringVar()
        self.search_label=tk.Label(self.entry_frame,text=" ")
        self.search_label.pack(fill=tk.X,side=tk.LEFT)
        self.w=tk.Entry(self.entry_frame,textvariable=self.place,highlightcolor="skyblue",highlightthickness=1)
        self.w.pack(fill=tk.X,side=tk.RIGHT)
        self.message_label=tk.Label(self.entry_frame,text="Find Places on Map : ")
        self.message_label.pack(fill=tk.X,side=tk.RIGHT)
        self.w.bind('<Return>',self.plott)
        
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH,expand=True)
        self.image=cv2.imread('D:\World.jpg')
        self.original=Image.fromarray(self.image)
        resized = self.original.resize((ini_x,ini_y),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        self.map=tk.Label(self.frame,image=self.img)
        self.map.pack(fill=tk.BOTH,expand=True)
        self.bind('<Configure>',self.update)
    def coordinate(self,latitude,longitude):
        mapWidth  = self.image.shape[1]
        mapHeight = self.image.shape[0]
        x      = int((longitude+180)*(mapWidth/360))
        latRad = latitude*math.pi/180;
        mercN  = math.log(math.tan((math.pi/4)+(latRad/2)),math.e)
        y      = int((mapHeight/2)-(mapWidth*mercN/(2*math.pi)))+238
        cv2.circle(self.image,(x,y),3,(random.randint(50,255),random.randint(50,255),random.randint(50,255)),3)
    def get_latnlng(self,address):
        if len(address) < 1 :
            return
        serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
        url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
        try:
            uh = urllib.urlopen(url)
        except Exception,e:
            self.search_label.configure(text="Internet Connection Error")
        data = uh.read().decode('utf-8')
        print ('Retrieved',len(data),'characters')
        tree = json.loads(data)
        results = tree['results']
        try:
            id = results[0]['place_id']
            lat=results[0]['geometry']['location']['lat']
            lon=results[0]['geometry']['location']['lng']
        except:
            #Since Such place doesn't exist
            self.search_label.configure(text="No Such Place Found")
            return 361,361
        return lat,lon
    def update(self,event=None):
        print "Updated"
        self.print_on_map()
    def print_on_map(self,event=None):
        x=self.winfo_width()
        y=self.winfo_height()
        print x,y
        self.original=Image.fromarray(self.image)
        resized = self.original.resize((x-4, y-25),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        self.map.configure(image=self.img)
    def press(self, event=None):
        self.w.focus_set()
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
        
Toggle=True
ini_x=800
ini_y=600
app = Application()
app.master.title('World')
thread.start_new_thread(app.mainloop())
