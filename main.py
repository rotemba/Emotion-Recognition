import sqlite3
import time
import sys
import os
import csv


path = os.getcwd()
print("Hello world")

print (path)

print("my name is ofer")


def initTwitterDB(s):
    databaseexisted = os.path.isfile('twitter.db')
    if not databaseexisted:
        dbcon = sqlite3.connect("twitter.db")
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("CREATE TABLE TaskTimes(TaskID INTEGER PRIMARY KEY NOT NULL ,DoEvery INTEGER NOT NULL , NumTimes INTEGER NOT NULL )")
            cursor.execute("CREATE TABLE Tasks(TaskId INTEGER NOT NULL  REFERENCES  TaskTimes(TaskId),TaskName TEXT NOT NULL, Parameter INTEGER)")
            cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
            cursor.execute("CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),FirstName TEXT NOT NULL, LastName TEXT NOT NULL)")
            inputfilename = s
            with open(inputfilename) as inputfile:
                counter = 0;
                for line in inputfile:
                    line.replace("\n", "")
                    tablename = line.split(",")
                    length = len(tablename)
                    if tablename[0] == "room":
                        roomnum = int(tablename[1])
                        cursor.execute("INSERT INTO Rooms VALUES (?)", (int(tablename[1]),))
                        x = 2;
                        if length > x:
                            privatename = str(tablename[2])
                            lastname = str(tablename[3])
                            lastname.replace('\n','')
                            cursor.execute("INSERT INTO Residents VALUES (?,?,?)", (roomnum, privatename, lastname,))
                    else:  # update taskTimes and taskId
                        doevery = int(tablename[1])
                        if tablename[0] == "clean":
                            # handle clean task
                            numoftimes = int(tablename[2])
                            roomnum = 0
                        else:
                            numoftimes = int(tablename[3])
                            roomnum = int(tablename[2])
                        tasktype = tablename[0]
                        cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (counter, doevery, numoftimes,))
                        cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (counter, tasktype, roomnum,))
                        counter += 1


def main(s):
    initTwitterDB(s)



if __name__ == '__main__':
    twiter_path = "files/twitter_dict.csv"
    main(twiter_path)



