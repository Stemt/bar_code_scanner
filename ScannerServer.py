import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import pyqrcode
from flask import Flask
from flask import request
from multiprocessing import Process
import urllib
import cv2
from pyzbar.pyzbar import decode
import pyautogui
import playsound

sound = True
app = Flask(__name__)


def server_thread():
    app.run(host='0.0.0.0', ssl_context='adhoc')


server = Process(target=server_thread)

def paste_at_cursor(str):
    pyautogui.write(str)
    pyautogui.press('enter')

def preprocess_image():
    img = cv2.imread("image.jpeg")
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (threash, grey) = cv2.threshold(grey,127,255,cv2.THRESH_BINARY)
    img = cv2.cvtColor(grey,cv2.COLOR_GRAY2BGR)
    return img

def scan_beep():
    playsound.playsound('resources/beep.wav')

@app.route('/')
def hello_world():
    with open("resources/index.html", 'r') as doc:
        return doc.read()


@app.route('/img/', methods=['POST'])
def process_image():
    json_data = request.get_json()
    img_data = json_data['img_data']
    response = urllib.request.urlopen(img_data)
    with open('image.jpeg', 'wb') as f:
        f.write(response.file.read())
    
    img = preprocess_image()
    height,width = img.shape[:2]

    barcodes = decode((img[:,:,0].astype('uint8').tobytes(),width,height))
    print(barcodes)

    recognised = False
    for code in barcodes:
        if not recognised:
            barcode = code.data
            print("code: " + str(barcode))
            paste_at_cursor(barcode.decode())
            scan_beep() 

            recognised = True

    return '{}'

if __name__ == '__main__':
    win = Tk()
    win.title("BarScanner")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    url = "https://{ip}:5000/"
    url = url.format(ip=(s.getsockname()[0]))
    s.close()
    print(url)
    qr = pyqrcode.create(url)
    img = BitmapImage(data = qr.xbm(scale=8))

    img_lbl = Label(win)
    img_lbl.config(image=img)
    img_lbl.pack()
    label = Label(win,text=url)
    label.pack()

    server.start()
    win.mainloop()
    server.terminate()
    server.join()
    




