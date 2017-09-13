import sqlite3
import time
import sys
import os
import csv
import numpy
import math
from numpy import genfromtxt
from init import initRelationTable





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


def createEmotionRelationDB(table1, table2):
    print("going to create the DB function")
    databaseexisted = os.path.isfile('emotions.db')
    if not databaseexisted:
        print("going to create the DB")
        dbcon = sqlite3.connect("emotions.db")
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""CREATE TABLE Relations(X INTEGER NOT NULL,
                                                     Y INTEGER NOT NULL,
                                                    Value REAL NOT NULL)""")
            print ("creating cartesian emotions table")
            relationArray = genfromtxt(table1, delimiter=',')
            rows = len(relationArray)
            cols = len(relationArray)

            print relationArray
            for row in range(0,rows):
                for col in range(0,cols):
                    cursor.execute("INSERT  INTO Relations VALUES (?,?,?)", (row, col, relationArray[row][col]))
                    print ("added value (%d) to the DB",  relationArray[row][col])
            print ("end of the prog")
            cursor.execute("SELECT * FROM Relations WHERE X = (?)", 30)
            data = cursor.fetchall()
            print(data)
    print ("DB EXIST")








def basic_actions_on_db(dbcon):
    print ("basic actions on DB function")
    with dbcon:
        cursor = dbcon.cursor()
        number = 30
        cursor.execute("SELECT * FROM Relations WHERE X=180 ORDER BY VALUE DESC")
        # SELECT * FROM Relations WHERE X = 181  ORDER BY VALUE  DESC
        print cursor.fetchall()
        #data= cursor.fetchall()
        #print (data)

    print ("end of basic actions on DB function")



def angel_between_two_emotions(emotion1, emotion2):
    #the emotions are strings and need to change them to numbers and then make the query

# expected input example: [1,2,3,4] and [6,7,8,9].
def vectorian_angel_between_two_vectors(vec1,vec2):
    #each vector is 50 dims and we need to return a number.
    #link with better implementation:
    # TODO: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    return angle (vec1,vec2)


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))




def main(s):
    #initTwitterDB(s)
    print("here 2nd")
    dbcon = initRelationTable()

    basic_actions_on_db(dbcon)
    pathOfCartesianEmotions="files/cartesian.csv"
    #createEmotionRelationDB(pathOfEmotionRealations,pathOfCartesianEmotions)
    print("end of main")



if __name__ == '__main__':
    print("here 1st")

    twiter_path = "files/twitter_dict.csv"
    main(twiter_path)



