import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import pyqrcode
import subprocess
import requests

win = Tk()
win.title("Scanner Server")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
url = "http://{ip}:5000/"
url = url.format(ip=(s.getsockname()[0]))
s.close()
print(url)
qr = pyqrcode.create(url)
img = BitmapImage(data = qr.xbm(scale=8))

img_lbl = Label(win)
img_lbl.config(image=img)
img_lbl.pack()

server = subprocess.Popen(['python3 ScannerServer.py --host=0.0.0.0'],shell=True)
win.mainloop()
server.terminate()