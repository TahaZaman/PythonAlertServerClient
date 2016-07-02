import subprocess as sbp
import socket
import pickle as pk
from PIL import Image
import os
import webview as wb
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 5000))
sock.send("taha".encode('ascii'))

def createHTML():
    wb.create_window('Alert','alert.html')

while True:
    print("client main start")
    x = int(sock.recv(1024).decode('ascii'))
    data = sock.recv(x)
    fp = open('data.p', 'wb')
    fp.write(data)
    fp.close()
    #send to subprocess to display alert
    sbp.Popen("python clientsb.py -l data.p" , shell=False)
    
sock.close()

