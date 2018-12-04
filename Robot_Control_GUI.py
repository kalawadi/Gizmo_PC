import serial
from tkinter import *
import csv

ser = serial.Serial('/dev/cu.usbmodem1411')  # open serial port

def robot_movement():

    buffer = m1.get()+m2.get()+m3.get()+m4.get()+m5.get()+m6.get()+'\n'
    print buffer
    ser.write(buffer)

def save_position():

    buffer = m1.get()+m2.get()+m3.get()+m4.get()+m5.get()+m6.get()
    print buffer
    with open('Robot_Movements_Act_1.csv', mode='a') as movements_file:
        position = csv.writer(movements_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        position.writerow([buffer])
        movements_file.close()

master = Tk()
master.title("Joints Positions")
Label(master, text="m1").grid(row=0)
Label(master, text="m2").grid(row=1)
Label(master, text="m3").grid(row=2)
Label(master, text="m4").grid(row=3)
Label(master, text="m5").grid(row=4)
Label(master, text="m6").grid(row=5)

m1 = Entry(master)
m2 = Entry(master)
m3 = Entry(master)
m4 = Entry(master)
m5 = Entry(master)
m6 = Entry(master)

m1.grid(row=0, column=1)
m2.grid(row=1, column=1)
m3.grid(row=2, column=1)
m4.grid(row=3, column=1)
m5.grid(row=4, column=1)
m6.grid(row=5, column=1)

Button(master, text='Send Command', command=robot_movement).grid(row=6, column=0, sticky=W, pady=4)
Button(master, text='Save Position', command=save_position).grid(row=6, column=1, sticky=W, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=6, column=2, sticky=W, pady=4)


mainloop( )