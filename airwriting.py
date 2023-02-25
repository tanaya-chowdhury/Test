"""
The canvas and camera frame opens and can write in air with finger and some useful commands are:
q - quit
c - clear canvas
s - start tracing finger and draw on canvas
z - stop tracing finger and drawing on canvas
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

canvas = np.ones([480, 640, 3], 'uint8') * 255
x, y = [], []

# Flag to indicate whether to detect the finger and draw on canvas or not
draw_flag = False

while True:
    if draw_flag:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = np.array([0, 48, 80], dtype=np.uint8)
        upper_range = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_range, upper_range)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 100:
            c = max(contours, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(c)

            if not x:
                x.append(x2)
                y.append(y2)
            else:
                if abs(x[-1] - x2) > 5 or abs(y[-1] - y2) > 5:
                    x.append(x2)
                    y.append(y2)

                if len(x) > 10:
                    x.pop(0)
                    y.pop(0)

                for i in range(1, len(x)):
                    if y[i] < 480 and x[i] < 640 and y[i - 1] < 480 and x[i - 1] < 640:
                        cv2.line(canvas, (x[i - 1], y[i - 1]), (x[i], y[i]), [0, 0, 0], 5)

        cv2.imshow("Camera", frame)
    cv2.imshow("Air-Writing", canvas)
    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    elif k == ord('c'):
        canvas = np.ones([480, 640, 3], 'uint8') * 255
        x, y = [], []
    elif k == ord('s'):
        draw_flag = True
    elif k == ord('z'):
        draw_flag = False

cv2.destroyAllWindows()
cap.release()
