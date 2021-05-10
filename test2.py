import tkinter as tk

root = tk.Tk()
root.geometry("800x600")
root.mainloop()

while True:

    x1 = root.winfo_x()
    x = root.winfo_pointerx()
    
    print(x, x1)

