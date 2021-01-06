import cv2
import numpy as np


cap = cv2.VideoCapture(0)
trail = []
while True:

    _,frame = cap.read()
    blured = cv2.blur(frame, (10,10))
    hsv = cv2.cvtColor(blured,  cv2.COLOR_BGR2HSV)

    ## Masking only light-Green
    lower = np.array([ 36, 44, 86], dtype = np.float32())
    upper = np.array([ 78, 132, 190], dtype = np.float32())    
    mask = cv2.inRange(hsv, lower, upper)
    masked  = cv2.bitwise_and(frame, frame, mask=mask)

    ## FINDING AND DRAWING CONTOURS    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    #print(len(contours))
    #cv2.drawContours(frame, contours, -1, (0,255,0), 2)
    ##Strengthen the selection
    if len(contours) > 0:
        largest_contour = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(largest_contour)
        center = x +w//2 , y+ h//2
        trail.append((center))
        #cv2.rectangle(frame,(x,y),(x+w, y+h), (0,255,0), -1)
        cv2.circle(frame, (center), 5, (0,255,0), -1)

    for each in trail[0:-2]:
        cv2.circle(frame, (each), 1, (0,0,255), -1)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()