import tkinter as tk
import sqlite3
from tkinter import * 
from tkinter import ttk
import ttkbootstrap as tb
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog
import shutil
import os




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
    try:
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM images WHERE id={id}")
        rows = c.fetchall()
        conn.commit()
        conn.close()
        if rows:
            return rows[0][3]
        else:
            return None
    except:
        return None
    
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
        self.current_index = 0
        self.image_paths = get_image_paths()
        self.max_index = len(self.image_paths)
        self.label = tk.Label(self.photo_page)
        self.label.pack(fill='both', expand=True)
        self.fullscreen = False
        self.root.bind('<Configure>', self.check_fullscreen)
        self.is_static = False

       # self.create_photo_tab()
        self.create_add_photo_tab()
        self.create_timer_tab()
        self.create_database_tab()
        self.update_image() 
      
    

    def update_image(self):
        if self.is_static == False:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.image_paths = get_image_paths()

            if self.image_paths != []:
                current_image_path = "./photo/" + self.image_paths[self.current_index]
                # Load the image file using Pillow
                try:
                    image = Image.open(current_image_path)

                    # Resize the image to fit the screen
                    image = image.resize((screen_width, screen_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)

                    # Update the label with the new image
                    self.label.config(image=photo)
                    self.label.image = photo  # Keep a reference to the image to prevent garbage collection

                    self.current_index = (self.current_index + 1) % len(self.image_paths)
                    self.root.after(5000, self.update_image)
                except:
                    self.current_index = (self.current_index + 1) % len(self.image_paths)
                    self.root.after(5000, self.update_image)
            else:
                self.current_index = 0
                self.label.config(image=None)
                self.label.image = None
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
        
        self.image_file_button = ttk.Button(self.add_photo, text="Choose Image", command=self.choose_image_file)
        self.image_file_button.grid(column=2, row=3, padx=10, pady=10)

        self.submit_button = ttk.Button(self.add_photo, text="Submit", command=self.submit_form)
        self.submit_button.grid(column=0, row=5, columnspan=2, pady=20)



    def choose_image_file(self):
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.gif'),
            ('All files', '*.*')
        )

        file_path = filedialog.askopenfilename(title="Open Image File", initialdir='/', filetypes=filetypes)
        if file_path:
            self.image_path_entry.delete(0, 'end')
            self.image_path_entry.insert(0, file_path)


    def create_timer_tab(self):

        self.tabControl.add(self.timer, text ='Timer') 
        self.tabControl.pack(expand = 1, fill ="both") 
        
        ttk.Label(self.timer, text="Display id:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.id_to_time = ttk.Entry(self.timer)
        self.id_to_time.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.timer, text="Display Time (mins):").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.time_entry = ttk.Entry(self.timer)
        self.time_entry.grid(column=1, row=1, padx=10, pady=10)

        self.time_button = ttk.Button(self.timer, text="Display Image", command=self.hold_image)
        self.time_button.grid(column=2, row=1,padx=10, pady=10)


        self.cancel_button = ttk.Button(self.timer, text="Cancel", command=self.cancel_hold)
        self.cancel_button.grid(column=1, row=4 ,padx=10, pady=10)
       

    def create_database_tab(self):

        self.tabControl.add(self.database, text ='Database') 
        self.tabControl.pack(expand = 1, fill ="both") 
        self.tree = ttk.Treeview(self.database, columns=("ID", "First Name", "Last Name", "Phone"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Phone", text="Phone")
      
        self.update_database_tab()
        self.delete_user_button = ttk.Button(self.database, text="Delete", command=self.delete_submit)
        self.delete_user_button.pack(padx=10, pady=10)

        

    def update_database_tab(self):
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch new data
        images = get_images()
        images = [image[:3] + image[4:] for image in images]       
        self.tree.config(height=len(images))

        
        # Insert new data
        for image in images:
            self.tree.insert("", tk.END, values=image)
        
        self.tree.pack(expand=False, fill='x',padx=10, pady=10)
        

        


    def delete_submit(self):
        selected_items = self.tree.selection()  # Get selected item
        try:
            if selected_items: 
                for selected_item in selected_items:
                    item_values = self.tree.item(selected_item, "values")  # Get the values of the selected item
                    image_id = item_values[0]  # Assuming the first column is the unique ID
                    path_to_delete = "./photo/" + get_path_from_id(image_id)
                    
                    if os.path.exists(path_to_delete):
                        os.remove(path_to_delete)

                    self.tree.delete(selected_item)
                    conn = sqlite3.connect('images.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM images WHERE id=?", (image_id,))
                    conn.commit()                
                    self.image_paths=get_image_paths()

                self.update_database_tab()

        except:
            messagebox.showwarning("Error", "Can't connect to database")


    #After restart loop loop image is bugged
    def restart_loop(self):
        self.is_static = False
        self.update_image()

    def check_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def cancel_hold(self):
        if self.is_static:
            self.restart_loop()
            messagebox.showwarning("Success", "Cancelled")


    def hold_image(self):
        id = self.id_to_time.get()
        time = self.time_entry.get()
        check_time = self.check_int(time)
        if id and time:   

            try:
                image_path_to_hold = get_path_from_id(id)

                if image_path_to_hold:
                    if check_time:
                        self.is_static = True
                        time = int(time) * 60 * 1000

                        screen_width = self.root.winfo_screenwidth()
                        screen_height = self.root.winfo_screenheight()
                        current_image_path = "./photo/" + image_path_to_hold

                        image = Image.open(current_image_path)

                        image = image.resize((screen_width, screen_height), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)

                        self.label.config(image=photo)
                        self.label.image = photo 
                        
                        messagebox.showinfo("Success", f"Id: {id} will display for {int(time/60/1000)} minutes")
                        self.id_to_time.delete(0, tk.END)
                        self.time_entry.delete(0, tk.END)
                        self.root.after(time, self.restart_loop)
                    else:
                        messagebox.showwarning("Error", "Please enter a whole number")
   
                else:
                    messagebox.showwarning("Error", "id is invalid")

            except:
                messagebox.showwarning("Error", "Can't connect to database")


        else:
            messagebox.showwarning("Error", "Please fill out all fields.")

        
    def submit_form(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        image_path = self.image_path_entry.get()
        phone = self.phone.get()
        
        target_directory = os.path.join(os.path.dirname(__file__), 'photo')
           
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        if image_path:
            target_path = os.path.join(target_directory, os.path.basename(image_path))
            shutil.copy(image_path, target_path)



        if first_name and last_name and image_path:
            try:
                conn = sqlite3.connect('images.db')
                c = conn.cursor()
                c.execute("INSERT INTO images (first_name, last_name, path, phone_number) VALUES (?, ?, ?, ?)", (first_name,last_name,os.path.basename(image_path), phone))
                conn.commit()

                messagebox.showinfo("Success", "Image added successfully!")
                self.update_database_tab()

                self.first_name_entry.delete(0, tk.END)
                self.last_name_entry.delete(0, tk.END)
                self.phone.delete(0, tk.END)
                self.image_path_entry.delete(0, tk.END)
                self.current_index = 0
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
