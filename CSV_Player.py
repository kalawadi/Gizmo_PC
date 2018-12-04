import csv
import time
import serial

ser = serial.Serial('/dev/ttyACM0')  # open serial port
time.sleep(15) # to give time for the braccio.begin initialization

with open(actionfile) as movement_file: # nickname
    csv_reader = csv.reader(movement_file, delimiter=',') # importing all the numbers in the csv
    for row in csv_reader: # for is a loop command which runs as many rows as you have, row is variable generated from the csv reader and contains all the number rows of the file
        print row[0] # content of the row
        buffer= row[0] + '\n' # content, to send to arduino
        ser.write(buffer) # sending to arduino
        time.sleep(1) # for the arduino/robotic arm to have time
    print 'Finish' # gone through the entire csv file