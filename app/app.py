import tkinter as tk
import sqlite3
import os
from tkinter import * 
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image
from PIL import ImageTk 


# Creates the database if none is existing 
def create_database():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, path TEXT)''')

    conn.commit()
    conn.close()

# Adds new image
def add_image(first_name,last_name, image_name):
    image_path = "./images/" + image_name
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("INSERT INTO images (first_name, last_name, path) VALUES (?, ?, ?)", (first_name,last_name,image_path))
    conn.commit()
    conn.close()


def get_images() -> list:
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows

class ImageApp:
    def __init__(self,root):
        self.root: Tk = root
        self.style = tb.Style('superhero')
        self.root.title("Photo Slide App")
        self.root.geometry("500x500")
        self.tabControl = ttk.Notebook(self.root)
        self.current_tab_index = 0
        #self.images: list = get_images()
        self.tab1: ttk.Frame = ttk.Frame(self.tabControl)
        self.tab2: ttk.Frame = ttk.Frame(self.tabControl)
        self.tab3: ttk.Frame = ttk.Frame(self.tabControl)

        self.create_photo_tab()
        self.create_add_photo_tab()
        self.create_timer_page()
        
        
        self.fullscreen = False
        self.root.bind('<Configure>', self.check_fullscreen)
    
    def create_photo_tab(self):
        self.tabControl.add(self.tab1,text ='Photo') 
        ttk.Label(self.tab1, text ="Photo").grid(column = 0, row = 0, padx = 30, pady = 30) 

    def create_add_photo_tab(self):

        self.tabControl.add(self.tab2, text ='Add Photo') 
        self.tabControl.pack(expand = 1, fill ="both") 
        ttk.Label(self.tab2, text ="Add Photo").grid(column = 0, row = 0,  padx = 30, pady = 30) 

    def create_timer_page(self):

        self.tabControl.add(self.tab3, text ='Timer') 
        self.tabControl.pack(expand = 1, fill ="both") 
        ttk.Label(self.tab3, text ="Timer").grid(column = 0, row = 0,  padx = 30, pady = 30) 


    def check_fullscreen(self, event=None):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
    #still bugged
    def check_fullscreen(self, event=None):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if width >= screen_width and height >= screen_height:
            if self.tabControl.index("current") != 0:
                self.current_tab_index = self.tabControl.index("current")
            for i in range(1, self.tabControl.index("end")):
                self.tabControl.hide(i)
            self.tabControl.select(0)
        else:
            if not self.tabControl.tab(1, "state") == "normal":
                for i in range(1, self.tabControl.index("end")):
                    self.tabControl.add(self.tabControl.winfo_children()[i])
                self.tabControl.select(self.current_tab_index)


root: Tk = tk.Tk()
app = ImageApp(root)
#Window Size

#create_database()
root.mainloop()
