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
    while True:
        options=["Exit","angles between 2 emotions",'create a new vector','findClosestEmotion','findOppositeEmotion', 'get vector of emotion','buildNewVector']
        optDict={0: exit, 1: angels, 2: createVector, 3: findClosestEmotion,4: findOppositeEmotion, 5:getVector, 6:buildNewVector}
        print("please choose the query to run:")
        print options
        for i in options:
            print (  ""+str(options.index(i))+" - "+ i)
        #input("Press Enter to continue...")
        num_of_query = input("choose query :")
        print ("query chosen:: %s" % options[num_of_query])
        if num_of_query > 0:
            optDict[num_of_query](dbcon)
        else:
            break

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

def findOppositeEmotion(dbcon):
    print("this function will find the opposite emotion")
    emotion1 = raw_input("put emotion name please")
    with dbcon:
        cursor=dbcon.cursor()
        #CT EmotionsID.ID, Relations."Value" FROM EmotionsID JOIN Relations ON EmotionsID.ID = Relations.X WHERE Emotion_name =""")
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        id1=cursor.fetchone()
        print (emotion1 + " : " + str(id1[0]) )
        cursor.execute("SELECT * FROM Relations WHERE X = (?) ORDER BY VALUE ASC ", (id1[0],) )
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

def getVectorOfEmotion(dbcon, emotionID):
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM Twitter WHERE ID = ?", (emotionID,))
        vector=cursor.fetchone()
        return (vector[1:len(vector)])

def prettyFloat(num):
        return "%0.4f" % num

def print_nicely_vec(vec):
    print(map((lambda x: "%0.4f" % x), vec))

def askScalarsFromUsers():
    print("this function asks the user for scalars and emotions.")
    list= [(0.5,"fool"),(0.4,"numbness"),(0.1,"dissatisfaction")]
    sumOfScalars = sum(i for i, j in list)
    if sumOfScalars != 1:
        print("Sum of Scalars should be 1, please enter scalars again")
        list = askScalarsFromUsers()
    return list

def buildNewVector(dbcon):
    list = askScalarsFromUsers()
    listWithVecs=map(lambda x: getVectorOfEmotion(dbcon,emotionNameToEmotionID(dbcon,x[1])),list)
    listOfScalars=map(lambda x: x[0], list)
    print listOfScalars

    #print listWithVecs
    listOfNewVEcs=map(lambda scalar, vec: map(lambda x: scalar * x, vec),listOfScalars,listWithVecs )
    #print(listOfNewVEcs)
    result = listOfNewVEcs[0]
    for i in range(1,len(listOfNewVEcs)):
        result = map(sum,zip(result,listOfNewVEcs[i]))
    print_nicely_vec(result)
#    result = map(sum, zip(listOfNewVEcs[0], listOfNewVEcs[1],listOfNewVEcs[2]))
 #   print_nicely_vec(result)

def getVector(dbcon):
    print("this function will retrive the vector of emotion and print it.")
    emotion1 = raw_input("put emotion name please")
    vector= getVectorOfEmotion(dbcon,emotionNameToEmotionID(dbcon,emotion1))
    #print vector
    #print len(vector)
    newVector=map(prettyFloat,vector)
    print newVector
    return (vector)

def computeNewVec(dbcon): # expected format: list ( scalar, vector )
    print ("for now going to work on fool emotion with scalar of 0.5")
    foolVec=getVectorOfEmotion(dbcon,emotionNameToEmotionID(dbcon,"fool"))
    scalar=0.5
    newFoolVec=map((lambda x: x * scalar), foolVec)
    print("beofre:")
    print (foolVec)
    print ("after:")
    print (newFoolVec)
    print ("pretty print:")
    print (map((lambda x:  "%0.4f" % x ), newFoolVec))








def main():
    print(2)
    dbcon=initEmoitionsDB()
    print(3)
    basicQueries(dbcon)
    print(4)


if __name__ == '__main__':
    print(1)

    main()



