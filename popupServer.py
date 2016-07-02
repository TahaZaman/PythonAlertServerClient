try:
    import Tkinter as tk #py 2
except:
    import tkinter as tk #py 3
import socket
import threading
import string
try:
    import tkFileDialog as tkf #py 2
except:
    import tkinter.filedialog as tkf #py 3

import pickle as pk
from PIL import Image
import os
import sys

class server:
	def __init__(self,host,port,parent):
		self.clients = {}
		self.parent = parent
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.newClient = ""                                       
		self.sock.bind((host, port)) 
	
	def runServer(self):
		id = int(0) 
		self.sock.listen(5)

		while True:
			cs, addr = self.sock.accept()
			print ("Clinet " + str(addr[0]) + " connected as ID: " + str(id))
			print ("waiting")
			name = cs.recv(1024)
			self.clients[id] = cs
			self.newClient = str(id) + ":" + name.decode('ascii')
			self.parent.gui.updtContactList(self.newClient)	        			
			id = id + 1


	def sendAlert(self,  msg, addresslist,fileList):
		data = {}
		data['message'] = msg
		my_list = fileList.split(" ")
		print (my_list)
		x = 0
		for path in my_list:
			ext = os.path.splitext(path)[1].upper()
			print(ext[1:])
			if path != "" and (ext != ".PNG" or ext != ".JPG" or ext != ".JPEG" or ext != ".GIF"):		
				img = Image.open(path)
				image = {}
				image['data'] = img
				image['type'] = ext[1:]
				data['image' + str(x)] = image
				x = x + 1
				data['imagecount'] = x
		datapk = pk.dumps(data)
		my_list = addresslist.split(",")
		for addr in my_list:
			if addr != "":
				try:
					sc = self.clients[int(addr[0])]
					sc.send(str(sys.getsizeof(datapk)).encode('ascii'))
					sc.send(datapk)
				except socket.error:
					self.parent.gui.deletefromContactList(addr)
					self.parent.gui.deletefromSendList(addr)
					self.parent.gui.textArea.insert(tk.END, addr + " removed as no connection available\n")

		
	

class GUI:
	def __init__(self, top, parent):
		self.message = ""
		self.addressList = ""
		self.sendFlag = False
		
		self.parent = parent
		self.top = top
		wd = tk.Label(top, text = "Message to Send", font=(14))
		wd.grid(row="0", column="0" ,columnspan = "2")

		wd = tk.Label(top, text = "Send to", font=(14), padx= 10)
		wd.grid(row="1", column="0")
		
		self.sendListstr = tk.StringVar()
		wd=tk.Entry(top,width = 50, textvariable=self.sendListstr)
		self.sendList = wd
		
		wd.grid(row="1", column="1", padx= 10)
		wd.bind("<Key>", lambda event: "break")

		self.cntcListstr = tk.StringVar()
		self.cntcListstr.set("")
		wd = tk.Listbox(top,width=30, height = 30 , listvariable=self.cntcListstr)
		self.contacts = wd
		wd.bind('<Button-1>', self.updateList)
		wd.grid(row="1", column="2", rowspan = "3")
		
		
		wd = tk.Text(bg = 'light cyan', width = 50, height = 20)
		self.textArea = wd
		wd.grid(row = 2, pady = 10, padx = 20,  columnspan="2")

		self.sendImgList = tk.StringVar()
		wd=tk.Entry(top,width = 50, textvariable=self.sendImgList)
		self.sendimglist = wd
		wd.grid(row="3", padx= 10, columnspan="2")
		wd.bind("<Key>", lambda event: "break")

		wd= tk.Button(text = "Send", width =10, height = 1)
		self.button = wd
		wd.grid(row = 4 , column = 0, pady = 10, padx = 20)
		wd.bind('<Button-1>', self.sendMessageAlert)

		wd= tk.Button(text = "Open", width =10, height = 1)
		self.browsebtn = wd
		wd.grid(row = 4 , column = 1, pady = 10, padx = 20)
		wd.bind('<Button-1>', self.openFileDialog)
	
	def openFileDialog(self, event):
		filepath = tkf.askopenfilenames(parent=self.top)
		self.sendimglist.delete(0, tk.END)
		self.sendimglist.insert(tk.END, filepath)
		
		
	def updateList(self, event):
		s = self.contacts.get(tk.ACTIVE)
		if self.sendListstr.get().find(s) == -1 :
			self.sendList.insert(tk.END, self.contacts.get(tk.ACTIVE) + ",")

	def updtContactList(self, userID):
		
		b = self.parent.gui.cntcListstr.get()
		s = b.replace(',', '')
		s = s.replace('(', '')
		s = s.replace(')', '')
		s = s.replace("'", '')
		self.parent.gui.cntcListstr.set(s + " " +userID)

	def deletefromContactList(self, name):
		s = self.parent.gui.contacts.get(0, tk.END)
		g = ' '.join(s)
		d = g.replace(name, '')
		self.parent.gui.cntcListstr.set(d)

	def deletefromSendList(self, name):
		s = self.parent.gui.sendList.get()
		
		d = s.replace(name+',', '')
		self.parent.gui.sendListstr.set(d)
	
	def sendMessageAlert(self, event):
		self.message = self.textArea.get(1.0, tk.END)
		self.addressList = self.sendListstr.get()
		self.filelist = self.sendImgList.get()
		self.textArea.delete(1.0, tk.END)
		if(self.addressList and len(self.message) > 1 ):
			self.parent.server.sendAlert(self.message, self.addressList, self.filelist)
		else:
			self.textArea.insert(tk.END, "Please enter a message and atleast one recepients")
		
		


class app:
	def __init__(self):
		top = tk.Tk()		
		self.gui = GUI(top, self)
		host = socket.gethostname()                           
		port = 5000 
		self.server = server(host,port,self) 
		threading.Thread(target=self.server.runServer).start()		
		top.mainloop()
	
					



ap =app()