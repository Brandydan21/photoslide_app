import tkinter as tk
import sqlite3
import os
from tkinter import * 
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image
from PIL import ImageTk 
from tkinter import messagebox



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
        self.photo_page: ttk.Frame = ttk.Frame(self.root)
        self.add_photo: ttk.Frame = ttk.Frame(self.tabControl)
        self.timer: ttk.Frame = ttk.Frame(self.tabControl)

        self.create_photo_tab()
        self.create_add_photo_tab()
        self.create_timer_page()
        
        
        self.fullscreen = False
        self.root.bind('<Configure>', self.check_fullscreen)
    
    def create_photo_tab(self):
        ttk.Label(self.photo_page, text ="Photo").grid(column = 0, row = 0, padx = 30, pady = 30) 

    def create_add_photo_tab(self):
        self.tabControl.add(self.add_photo, text ='Add Photo') 

        
        # Create form elements
        ttk.Label(self.add_photo, text="First Name:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.first_name_entry = ttk.Entry(self.add_photo)
        self.first_name_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.add_photo, text="Last Name:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.last_name_entry = ttk.Entry(self.add_photo)
        self.last_name_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.add_photo, text="Image Path:").grid(column=0, row=2, padx=10, pady=10, sticky='w')
        self.image_path_entry = ttk.Entry(self.add_photo)
        self.image_path_entry.grid(column=1, row=2, padx=10, pady=10)

        self.submit_button = ttk.Button(self.add_photo, text="Submit", command=self.submit_form)
        self.submit_button.grid(column=0, row=3, columnspan=2, pady=20)


    def create_timer_page(self):

        self.tabControl.add(self.timer, text ='Timer') 
        self.tabControl.pack(expand = 1, fill ="both") 
        ttk.Label(self.timer, text ="Timer").grid(column = 0, row = 0,  padx = 30, pady = 30) 


    def submit_form(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        image_path = self.image_path_entry.get()
        
        if first_name and last_name and image_path:
            add_image(first_name, last_name, image_path)
            messagebox.showinfo("Success", "Image added successfully!")
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.image_path_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please fill out all fields.")




    
    def check_fullscreen(self, event=None):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if width >= screen_width and height >= screen_height:
            self.tabControl.pack_forget()
            self.photo_page.pack(expand=1, fill="both")
        else:
            self.photo_page.pack_forget()
            self.tabControl.pack(expand=1, fill="both")

root: Tk = tk.Tk()
app = ImageApp(root)
#Window Size

#create_database()
root.mainloop()
