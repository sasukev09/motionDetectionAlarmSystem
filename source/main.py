import threading # run multiple threads to handle the displaying of changes/data/alarm at teh same time
import winsound # for alarm sounds

# TODO TRY TO SEND A PHONE NOTIFICATION WHEN ALARM IS ACTIVATED

#external python modules
import cv2 # computer vision library
import imutils # minor manipulation of frames like resizing

# Assigning a camera to a index 
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Camera capture dimensions
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#starting frame
#get a grame and compare it to the next frame
# if you get enough differences to say this is motion

# Unnamed frame and start frame, returned by camera
_, start_frame = capture.read()
start_frame = imutils.resize(start_frame, width = 600)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)

alarm = False
notification = False
alarm_mode = False
alarm_counter = 0

# Here is where you send the notification
def alarm_activated():
    global alarm
    for _ in range(3): # loop that runs 5 times
        if not alarm_mode: # if not activated, stop
            break
        print("Alarm!!!")
        winsound.Beep(6000,4000)
    alarm = False

while True:

    _, frame = capture.read()
    frame = imutils.resize(frame, width = 600)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

        # calculating the frame difference
        diferencia = cv2.absdiff(frame_bw, start_frame)
        # everything above thres is white, and below black
        threshold = cv2.threshold(diferencia, 25,255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        # sensitivity to movement
        if threshold.sum() > 100000:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1 


        # if alarm active show threshold image
        cv2.imshow("Cam", threshold)
    else:
        #show frame without anything
        cv2.imshow("Cam" , frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target = alarm_activated).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break


capture.release()
cv2.destroyAllWindows()
