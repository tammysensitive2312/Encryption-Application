import tkinter as tk
from PIL import ImageTk, Image
from old.file_selector import FileSelector

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=300)
canvas.pack()

img = Image.open("../res/441956724_1233076297664250_2744444318462441104_n.png")
img = img.resize((600, 300))
photo = ImageTk.PhotoImage(img)

canvas.create_image(0, 0, anchor=tk.NW, image=photo)
root.photo = photo

file_selector = FileSelector(root)
root.mainloop()