import tkinter as tk
import sqlite3
import os
from tkinter import *
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
        self.root.title("Photo Slide App")
        #self.images: list = get_images()
        self.create_widgets()
    
    def create_widgets(self):
        #creates container to hold the pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill='both', expand=True)


        self.page1 = tk.Frame(self.container)
        self.page2 = tk.Frame(self.container)
        for frame in (self.page1, self.page2):
            frame.grid(row=0, column=0, sticky='nsew')

    

root: Tk = tk.Tk()
#app = ImageApp(root)
#Window Size
root.geometry("500x500")

#create_database()
root.mainloop()
