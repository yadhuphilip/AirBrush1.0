import cv2
import numpy as np


###################

def clearScreenCheck(xy):

    if xy[0]>=0 and xy[0]<59 and xy[1] >0 and xy[1] <74: return True
    return False

##################


cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)
trail = []
while True:

    _,frame = cap.read()
    ## Fliping the image for the sake
    frame = cv2.flip(frame, 1)


    blured = cv2.GaussianBlur(frame, (7,7),0)
    #blured = cv2.medianBlur(frame, 5)
    #blured = cv2.blur(frame, (10,10))
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
    cv2.rectangle(frame, (0,0),(60,75), (0,0,0), -1)
    if len(contours) >  0  and cv2.contourArea(max(contours, key = cv2.contourArea))>150:
        largest_contour = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(largest_contour)
        center = x +w//2 , y+ h//2
        trail.append((center))
        if clearScreenCheck(center):
            trail = []
        #cv2.rectangle(frame,(x,y),(x+w, y+h), (0,255,0), -1)
        cv2.circle(frame, (center), 8, (0,255,0), -1)
    if len(trail)>2:
        for i in range(1,len(trail[:-1])):
            x1,y1 = trail[i-1]
            x2,y2 = trail[i]
            if abs(x1-x2) >1 or abs(y2-y1)>1: cv2.line(frame, trail[i-1], trail[i], (0,0,255), 2)


    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()