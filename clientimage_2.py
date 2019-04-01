import socket
import cv2
import sys

cascPath = 'C:\\Users\\BIPUL\\Documents\\socket programming\\haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h),(255,255,255),0)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        print('Captured')
        cv2.imwrite("face11.jpg", frame)
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()



s=socket.socket()
host='192.168.43.132'
port=5005
s.connect((host,port))
f=open('face11.jpg','rb')
print('sending..')
l=f.read(1024)
while(l):
    print('sending..')
    s.send(l)
    l=f.read(1024)
f.close()
print("done sending")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024))
print(s.recv(1024))
s.close()

a=socket.socket()
host='192.168.43.71'
port=6005
a.bind((host,port))
f=open('confidential.txt','wb')
a.listen(5)
while True:
    c, addr= a.accept()
    print('Got connection from', addr)
    print('receiving...')
    l=c.recv(1024)
    while(l):
        print("receiving...")
        f.write(l)
        l=c.recv(1024)
    f.close()
    print("done receiving")
    c.send(b'thanks for connecting')
    c.close()
    
