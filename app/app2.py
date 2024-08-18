import tkinter as tk
from tkinter import Toplevel

class FullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Set the window to fullscreen
        self.root.bind("<Key>", self.on_key_press)  # Bind any key press event to the handler

        # Example label for the main screen
        self.label = tk.Label(root, text="Press any key to open a new tab.", font=("Helvetica", 24))
        self.label.pack(expand=True)

    def on_key_press(self, event):
        self.open_new_tab()  # Call the method to open a new tab when any key is pressed

    def open_new_tab(self):
        # Create a new top-level window (acting as a "tab")
        new_tab = Toplevel(self.root)
        new_tab.title("New Tab")
        new_tab.geometry("400x300")

        # Example content for the new tab
        label = tk.Label(new_tab, text="This is a new tab.", font=("Helvetica", 18))
        label.pack(expand=True, padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)
    root.mainloop()
