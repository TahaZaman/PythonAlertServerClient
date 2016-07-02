import socket
import pickle as pk
from PIL import Image
import sys
import webview as wb
import os

datapath = sys.argv[2]
data = open(datapath, 'rb').read()
#create Alert
dataupk = pk.loads(data)
html2 = """<html>
	<head>
        <link href="alert.css" rel="stylesheet"/>
    </head>
	<body>
		<p id="from">From: """
html2 = html2 + dataupk['host'] + """</p>
	    	<p id="priority">Priority </p>
		    <div id="msgDiv"> """
html2 = html2 + dataupk['message'] + """</div>
        <div id="imgDiv">"""

imgcount = dataupk['imagecount']
images = []
for i in range(0,imgcount):
    img = dataupk['image' + str(i)]['data']
    imagepath = 'image'+str(i) + '.' + str(dataupk['image' + str(i)]['type']).lower()
    img.save(imagepath, str(dataupk['image' + str(i)]['type']) )
    images.append(imagepath)
    html2 = html2 +"""<img src='""" + imagepath + """' />
     """
html2 = html2 + """</div>
            </body>
        </html> """


alertDoc = open('alert.html', 'w', encoding='utf-8')
alertDoc.write(html2)
alertDoc.close()
wb.create_window('Alert','alert.html')
wb.destroy_window()

print(datapath)
os.remove(datapath)
for ipath in images:
    print(ipath)
    os.remove(ipath)
    
os.remove('alert.html')