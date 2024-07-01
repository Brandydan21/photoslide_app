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
        #self.images: list = get_images()
        self.create_widgets()
        self.fullscreen = False
        self.root.bind('<Configure>', self.check_fullscreen)

        
    
    def create_widgets(self):
        tab1: ttk.Frame = ttk.Frame(self.tabControl)
        tab2: ttk.Frame = ttk.Frame(self.tabControl)

        self.tabControl.add(tab1, text ='Tab 1') 
        self.tabControl.add(tab2, text ='Tab 2') 
        self.tabControl.pack(expand = 1, fill ="both") 
        ttk.Label(tab1,  
          text ="Welcome to GeeksForGeeks").grid(column = 0, row = 0, padx = 30, pady = 30) 
        ttk.Label(tab2, 
          text ="Lets dive into the world of computers").grid(column = 0, row = 0,  padx = 30, pady = 30) 

    def check_fullscreen(self, event=None):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if width >= screen_width and height >= screen_height:
            self.tabControl.pack_forget()
        else:
            self.tabControl.pack(expand=1, fill="both")

    

root: Tk = tk.Tk()
app = ImageApp(root)
#Window Size

#create_database()
root.mainloop()
