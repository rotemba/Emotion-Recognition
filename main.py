import sqlite3
import os

from numpy import genfromtxt
import sqlite3
import os
import csv
from init import initEmoitionsDB


def angels_between_two_emotions (dbcon,emotion1, emotion2):
    print ("angel between two emotions function")
    with dbcon:
        cursor=dbcon.cursor()
        #CT EmotionsID.ID, Relations."Value" FROM EmotionsID JOIN Relations ON EmotionsID.ID = Relations.X WHERE Emotion_name =""")
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        id1=cursor.fetchone();
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion2,))
        id2 = cursor.fetchone();
        print (emotion1 + " : " + str(id1[0]) )
        print (emotion2 + " : " + str(id2[0]))

        cursor.execute("SELECT VALUE FROM Relations WHERE X = (?) AND  Y = (?)", (id1[0],id2[0],) )
        angel=cursor.fetchone()
        print ("angel between " + emotion1 + " and " + emotion2 +" is : " +str(angel[0]))


        #cursor.execute("""SELECT TaskTimes.TaskID,DoEvery,NumTimes,Tasks.TaskName,Parameter
        #                      FROM TaskTimes JOIN Tasks ON TaskTimes.TaskID = Tasks.TaskID
        #                      WHERE TaskTimes.NumTimes > 0 """)
    #SELECT * FROM Relations WHERE X = 181  ORDER BY VALUE  DESC
    #SELECT VALUE FROM Relations WHERE X = 180 AND Y = 40


def basicQueries(dbcon):
    options=["angles between 2 emotions",'create a new vector', 'get vector of emotion']
    optDict={1: angels, 2: createVector}
    print("please choose the query to run:")
    print options
    for i in options:
        print (  ""+str(options.index(i))+" - "+ i)
    num_of_query = input("choose query :")
    print ("query chosen:: %d", num_of_query)
    optDict[num_of_query](dbcon)

def angels (dbcon):
    print ("angels between 2 vectors")
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID")
        data= cursor.fetchall()
        for row in data:
            print row[0]



    emotion1 = raw_input("put first emotions please")
    emotion2 = raw_input("put second emotions please")
    angels_between_two_emotions(dbcon,emotion1,emotion2)


def createVector(dbcon):
    print("creating vector")


def main():
    print(1)
    dbcon=initEmoitionsDB()
    print(3)
    basicQueries(dbcon)



if __name__ == '__main__':
    print(2)

    main()



