import socket
import cv2
import numpy as np 
import sqlite3
import os
print("The Server is ready")
s=socket.socket()
host='192.168.43.71'
port=5005
s.bind((host,port))
f=open('imag_11.jpg','wb')
s.listen(5)
while True:
    z, addr= s.accept()
    print('Got connection from', addr)
    print('receiving...')
    l=z.recv(1024)
    while(l):
        print("receiving...")
        f.write(l)
        l=z.recv(1024)
    f.close()
    print("done receiving")
    z.send(b'thanks for connecting')





    flag=0
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    fname = "recognizer/trainingData.yml"
    if not os.path.isfile(fname):
      print("Please train the data first")
      exit(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    
    img = cv2.imread('imag_11.jpg')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(fname)
    
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
        ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
        c.execute("select name from users where id = (?);", (ids,))
        result = c.fetchall()
        name = result[0][0]
        if conf < 50:
        
        
              cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
              print('Authenticated')
              z.send(b'You are authorized')
              b=socket.socket()
              host='192.168.43.55'
              port=6005
              b.connect((host,port))
              x=open('confidential.txt','rb')
              print('sending..')
              l=x.read(1024)
              while(l):
                print('sending..')
                b.send(l)
                l=x.read(1024)
              x.close()
              print("done sending")
              b.shutdown(socket.SHUT_WR)
              print(b.recv(1024))
              b.close()
              break  
        else:

              cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
              print('not Authenticated')
              z.send(b'You are not authorized')
              b=socket.socket()
              host='192.168.43.55'
              port=6005
              b.connect((host,port))
              x=open('dummy.txt','rb')
              print('sending..')
              l=x.read(1024)
              while(l):
                print('sending..')
                b.send(l)
                l=x.read(1024)
              x.close()
              print("done sending")
              b.shutdown(socket.SHUT_WR)
              print(b.recv(1024))
              b.close()
              break
             
    
    cv2.imshow('Face Recognizer',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    

    z.close()
    
