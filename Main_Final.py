# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2                          # opencv-python
import numpy as np                  # matrix calculations
import csv                          # CSV list for positions
import serial                       # Serial communication
import Tkinter as tk                # GUI

# initialize the camera and grab a reference to the raw camera capture
# modify camera position and rotation etc.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
camera.rotation = -90

# open serial port
ser = serial.Serial('/dev/ttyACM0')
time.sleep(15)                                              # to give time for the braccio.begin initialization
print 'turn on the robot'


def play_video():
    i = 0
    cap = cv2.VideoCapture('saltbae_video.avi')             # import video from directory
    totalFrames = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

    while i < totalFrames:
        _, video = cap.read()
        cv2.moveWindow('video', 80, 20)
        cv2.imshow('video', video)
        i += 1
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    robotic_arm_action("Robot_Act_2.csv") 

def color_rec():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)         # convert image BGR to HSV
        lower_green = np.array([30, 20, 50])                 # create a matrix with the three values
        upper_green = np.array([60, 255, 100])
        lower_red = np.array([30, 150, 100])
        upper_red = np.array([255, 255, 200])

        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        green_red = np.add(mask_green, mask_red)  # binary array
        res_green_red = cv2.bitwise_and(image, image, mask=green_red)
        res_green = cv2.bitwise_and(image, image, mask=mask_green)
        res_red = cv2.bitwise_and(image, image, mask=mask_red)

        pmc_green = np.count_nonzero(mask_green)
        pmc_red = np.count_nonzero(mask_red)

        if pmc_green > 2000:
            print "I found a broccoli"
            show_picture("broccoli.jpg")
            robotic_arm_action("Robot_Act_3.csv")
            rawCapture.truncate(0)
            

        if pmc_red > 1000:
            print "I found a tomato"
            show_picture("tomatoes.jpg")
            robotic_arm_action("Robot_Act_4.csv")
            time.sleep(2)
            robotic_arm_action("Robot_Act_5.csv")
            time.sleep(2)
            robotic_arm_action("Robot_Act_6.csv")
            rawCapture.truncate(0)
            show_picture("thankyou.jpg")
            break
            

        if pmc_green > 2000 and pmc_red > 1000:
            print "I made a salad"

        # show the frame
        #cv2.imshow("Frame", image)
        cv2.moveWindow('Green & Red', 80, 20)  
        #cv2.namedWindow('Green & Red', cv2.WINDOW_NORMAL)
        cv2.imshow('Green & Red', res_green_red)
        #cv2.imshow('res_green', res_green)
        #cv2.imshow('res_red', res_red)


        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
def robotic_arm_action(actionfile):
    with open(actionfile) as movement_file: # nickname
        csv_reader = csv.reader(movement_file, delimiter=',') # importing all the numbers in the csv
        for row in csv_reader:                                # for loop command runs all the available rows, row is variable generated from the csv reader
            print row[0]                                      # content of the row
            buffer= row[0] + '\n'                             # content to send to Arduino
            ser.write(buffer)                                 # sending to Arduino
            time.sleep(2)                                     # for the Arduino/robotic arm to have time
    print 'Finish'                                            # gone through the entire csv file
    
def show_picture(picturefile):
    img = cv2.imread(picturefile)
    cv2.moveWindow('Message', 50, 0)  
    cv2.namedWindow('Message', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Message', 800,600)
    #cv2.moveWindow('Message', 0, 0)              
    cv2.imshow('Message',img)
    cv2.waitKey(3000) & 0xFF == ord('q')
    cv2.destroyAllWindows()    
        
def main_loop():
    robotic_arm_action("Robot_Act_1.csv")
    play_video()
    color_rec()
    
root = tk.Tk()
root.geometry('100x30+695+0')
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="Quit", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)
start = tk.Button(frame,
                   text="Start",
                   command=main_loop)
start.pack(side=tk.LEFT)

root.mainloop()




