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
        #SELECT EmotionsID.ID, Relations."Value" FROM EmotionsID JOIN Relations ON EmotionsID.ID = Relations.X WHERE Emotion_name =""")
        #cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        #id1=cursor.fetchone();
        id1=emotionNameToEmotionID(dbcon,emotion1)
        #cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion2,))
        #id2 = cursor.fetchone();
        id2=emotionNameToEmotionID(dbcon,emotion2)
        #print (emotion1 + " : " + str(id1[0]) )
        #print (emotion2 + " : " + str(id2[0]))
        print ("emotion1 :" + str(id1))
        print ("emotion2 :" + str(id2))
        cursor.execute("SELECT VALUE FROM Relations WHERE X = (?) AND  Y = (?)", (id1,id2,) )
        angel=cursor.fetchone()
        print ("angel between " + emotion1 + " and " + emotion2 +" is : " +str(angel[0]))


        #cursor.execute("""SELECT TaskTimes.TaskID,DoEvery,NumTimes,Tasks.TaskName,Parameter
        #                      FROM TaskTimes JOIN Tasks ON TaskTimes.TaskID = Tasks.TaskID
        #                      WHERE TaskTimes.NumTimes > 0 """)
    #SELECT * FROM Relations WHERE X = 181  ORDER BY VALUE  DESC
    #SELECT VALUE FROM Relations WHERE X = 180 AND Y = 40


def basicQueries(dbcon):
    options=["nothing","angles between 2 emotions",'create a new vector','findClosestEmotion', 'get vector of emotion']
    optDict={1: angels, 2: createVector, 3: findClosestEmotion}
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

def findClosestEmotion(dbcon):
    print("this function will find the closest emotion")
    emotion1 = raw_input("put emotion name please")
    with dbcon:
        cursor=dbcon.cursor()
        #CT EmotionsID.ID, Relations."Value" FROM EmotionsID JOIN Relations ON EmotionsID.ID = Relations.X WHERE Emotion_name =""")
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        id1=cursor.fetchone()
        print (emotion1 + " : " + str(id1[0]) )
        cursor.execute("SELECT * FROM Relations WHERE X = (?) ORDER BY VALUE DESC ", (id1[0],) )
        for i in range(1,4):
            data = cursor.fetchone()
            print (str(i)+":[" + emotion1 + "," + emotionIDToName(dbcon, data[1]) + "] similarity:" + str(data[2]))


def emotionIDToName(dbcon, emotionID):
    with dbcon:
        cursor=dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID WHERE ID = ?", (emotionID,))
        name=cursor.fetchone()
        #print("got id number:" + str(emotionID) +" - name: "+ name[0])
        return (name[0])



def emotionNameToEmotionID(dbcon,emotionName):
    with dbcon:
        cursor=dbcon.cursor()
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotionName,))
        emotionID=cursor.fetchone()
        #print("got emotion name:" + emotionName +" - id: "+ str(emotionID[0]))
        return (emotionID[0])


def main():
    print(1)
    dbcon=initEmoitionsDB()
    print(3)
    basicQueries(dbcon)



if __name__ == '__main__':
    print(2)

    main()



