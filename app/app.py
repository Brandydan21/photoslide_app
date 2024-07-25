import tkinter as tk
import sqlite3
import os
from tkinter import * 
from tkinter import ttk
import ttkbootstrap as tb
from PIL import ImageTk, Image
from tkinter import messagebox
import threading
import time



# Creates the database if none is existing 
def create_database():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, path TEXT, phone_number TEXT)''')
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

def get_path_from_id(id):
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM images WHERE id={id}")
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows[0][3]
    
def get_image_paths() -> list:
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    rows = c.fetchall()
    conn.commit()
    conn.close()
    image_paths = []
    for row in rows:
        image_paths.append(row[3])

    return image_paths

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
        self.database: ttk.Frame = ttk.Frame(self.tabControl)
        self.delete_id: ttk.Frame = ttk.Frame(self.tabControl)
        self.image_paths = get_image_paths()
        self.current_index = 0
        self.max_index = len(self.image_paths)
        self.label = tk.Label(self.photo_page)
        self.label.pack(fill='both', expand=True)
        self.fullscreen = False
        self.root.bind('<Configure>', self.check_fullscreen)

       # self.create_photo_tab()
        self.create_add_photo_tab()
        self.create_timer_tab()
        self.create_database_tab()
        self.create_delete_tab()

        self.update_image() 
      
        
     

    def update_image(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        current_image_path = "./photo/" + self.image_paths[self.current_index]

        # Load the image file using Pillow
        image = Image.open(current_image_path)

        # Resize the image to fit the screen
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to the image to prevent garbage collection

        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.root.after(5000, self.update_image)

    def create_add_photo_tab(self):
        self.tabControl.add(self.add_photo, text ='Add Photo') 

        
        # Create form elements
        ttk.Label(self.add_photo, text="First Name:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.first_name_entry = ttk.Entry(self.add_photo)
        self.first_name_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.add_photo, text="Last Name:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.last_name_entry = ttk.Entry(self.add_photo)
        self.last_name_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.add_photo, text="Phone:").grid(column=0, row=2, padx=10, pady=10, sticky='w')
        self.phone = ttk.Entry(self.add_photo)
        self.phone.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(self.add_photo, text="Image Path:").grid(column=0, row=3, padx=10, pady=10, sticky='w')
        self.image_path_entry = ttk.Entry(self.add_photo)
        self.image_path_entry.grid(column=1, row=3, padx=10, pady=10)

        self.submit_button = ttk.Button(self.add_photo, text="Submit", command=self.submit_form)
        self.submit_button.grid(column=0, row=4, columnspan=2, pady=20)


    def create_timer_tab(self):

        self.tabControl.add(self.timer, text ='Timer') 
        self.tabControl.pack(expand = 1, fill ="both") 
        ttk.Label(self.timer, text="Display id:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.id_to_time = ttk.Entry(self.timer)
        self.id_to_time.grid(column=1, row=0, padx=10, pady=10)
        self.time_button = ttk.Button(self.timer, text="Display Image", command=self.hold_image)
        self.time_button.grid(column=0, row=4, columnspan=2, pady=20)


    def create_delete_tab(self):

        self.tabControl.add(self.delete_id, text ='Delete Id') 
        ttk.Label(self.delete_id, text="Delete id:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.id_to_delete = ttk.Entry(self.delete_id)
        self.id_to_delete.grid(column=1, row=0, padx=10, pady=10)

        self.delete_button = ttk.Button(self.delete_id, text="Delete", command=self.delete_submit)
        self.delete_button.grid(column=0, row=4, columnspan=2, pady=20)

    def create_database_tab(self):

        self.tabControl.add(self.database, text ='Database') 
        self.tabControl.pack(expand = 1, fill ="both") 
        tree = ttk.Treeview(self.database, columns=("ID", "First Name", "Last Name", "Path", "Phone"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("Path", text="Path")
        tree.heading("Phone", text="Phone")

        self.update_database_tab(tree)

        tree.pack(expand=True, fill='both')


    def update_database_tab(self,tree):
        
        for item in tree.get_children():
            tree.delete(item)
        
        # Fetch new data
        images = get_images()
        
        # Insert new data
        for image in images:
            tree.insert("", tk.END, values=image)
        
        # Schedule next update
        tree.after(5000, self.update_database_tab, tree) 

    def delete_submit(self):
        id_to_delete = self.id_to_delete.get()
        if id_to_delete:
            try:
                conn = sqlite3.connect('images.db')
                c = conn.cursor()
                c.execute("DELETE FROM images WHERE id=?", (id_to_delete,))
                conn.commit()
                messagebox.showinfo("Success", f"Deleted User Id: {id_to_delete}")
                self.id_to_delete.delete(0, tk.END)
                self.image_paths=get_image_paths()

            except:
                messagebox.showwarning("Error", "Can't connect to database")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "Please fill out all fields.")

    def hold_image(self):
        hold_paths = self.image_paths
        id = self.id_to_time.get()
        image_path_to_hold = get_path_from_id(id)
        self.image_paths = image_path_to_hold
        
        def revert_image_paths():
            time.sleep(10)
            self.image_paths = hold_paths

        threading.Thread(target=revert_image_paths).start()
        self.image_paths = hold_paths

     
    def submit_form(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        image_path = self.image_path_entry.get()
        phone = self.phone.get()
        
        if first_name and last_name and image_path:
            try:
                conn = sqlite3.connect('images.db')
                c = conn.cursor()
                c.execute("INSERT INTO images (first_name, last_name, path, phone_number) VALUES (?, ?, ?, ?)", (first_name,last_name,image_path, phone))
                conn.commit()

                messagebox.showinfo("Success", "Image added successfully!")
                self.first_name_entry.delete(0, tk.END)
                self.last_name_entry.delete(0, tk.END)
                self.phone.delete(0, tk.END)
                self.image_path_entry.delete(0, tk.END)
                self.image_paths=get_image_paths()
            except:
                messagebox.showwarning("Error", "Can't connect to database")
            finally:
                conn.close()
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

create_database()
root: Tk = tk.Tk()  
app = ImageApp(root)

root.mainloop()
