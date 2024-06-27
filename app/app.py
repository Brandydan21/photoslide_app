import tkinter as tk
import sqlite3
import os
from tkinter import *
from PIL import Image
from PIL import ImageTk 

#Window Size

#root = tk.Tk()

#root.geometry("500x500")

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


def get_images():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    rows = c.fetchall()
    conn.commit()
    conn.close()

    pass

create_database()