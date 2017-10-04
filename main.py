import sqlite3
import os

from numpy import genfromtxt
import sqlite3
import os
import csv
from init import initEmoitionsDB
import math

def basicQueries(dbcon):
    while True:
        options=["Exit","angles between 2 emotions",'create a new vector','findClosestEmotion','findOppositeEmotion', 'get vector of emotion','buildNewVector']
        optDict={0: exit, 1: angels, 2: createVector, 3: findClosestEmotion,4: findOppositeEmotion, 5:getVector, 6:buildNewVector}
        print("please choose the query to run:")
        print options
        for i in options:
            print (  ""+str(options.index(i))+" - "+ i)
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

def angels_between_two_emotions (dbcon,emotion1, emotion2):
    print ("angel between two emotions function")
    with dbcon:
        cursor=dbcon.cursor()
        id1=emotionNameToEmotionID(dbcon,emotion1)
        id2=emotionNameToEmotionID(dbcon,emotion2)
        print ("emotion1 :" + str(id1))
        print ("emotion2 :" + str(id2))
        cursor.execute("SELECT VALUE FROM Relations WHERE X = (?) AND  Y = (?)", (id1,id2,) )
        angel=cursor.fetchone()
        print ("angel between " + emotion1 + " and " + emotion2 +" is : " +str(angel[0]))

def createVector(dbcon):
    print("creating vector")

def findClosestEmotion(dbcon):
    print("this function will find the closest emotion")
    emotion1 = raw_input("put emotion name please")
    with dbcon:
        cursor=dbcon.cursor()
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
    counter = 1
    sumOfScalars = 0
    print("this function asks the user for scalars and emotions.")
    listOfTuples = list()
    while sumOfScalars < 1:
        emotion = raw_input("Please enter emotion number %d " % counter)
        scalar = float(input("Please enter coefficient for emotion %s " % emotion))
        while sumOfScalars + scalar > 1:
            print("Sum of Scalars should be 1, please enter scalar again")
            scalar = float(input("Please enter coefficient for emotion %s " % emotion))

        print ("you entered %s as coefficient %0.2f" % (emotion, scalar))
        counter += 1
        sumOfScalars += scalar
        pair = (scalar, emotion)
        listOfTuples.append(pair)

    return listOfTuples


def buildNewVector(dbcon):
    list = askScalarsFromUsers()
    listWithVecs=map(lambda x: getVectorOfEmotion(dbcon,emotionNameToEmotionID(dbcon,x[1])),list)
    listOfScalars=map(lambda x: x[0], list)
    listOfNewVEcs=map(lambda scalar, vec: map(lambda x: scalar * x, vec),listOfScalars,listWithVecs )
    result = listOfNewVEcs[0]
    for i in range(1,len(listOfNewVEcs)):
        result = map(sum,zip(result,listOfNewVEcs[i]))
    print_nicely_vec(result)
    printClosestVectorNames(dbcon,result)


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

def sizeOfSingleVec(vec):
    return math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, vec)))

def printVectorsSize(dbcon):
    for i in range(1,374):
        vec=getVectorOfEmotion(dbcon,i)
        sizeOfVec = sizeOfSingleVec(vec)
        print (str(i)+":vector-"+ emotionIDToName(dbcon,i)+ " size: "+ str(sizeOfVec))



def angelBetweenTwoVecs( vec1, vec2):
    #print ("angel between 2 vecs function.")

    sizeOfVec1=sizeOfSingleVec(vec1)
    sizeOfVec2=sizeOfSingleVec(vec2)
    mone=sum((a*b) for a, b in zip(vec1, vec2))
    sizeOfVecs=(sizeOfVec1*sizeOfVec2)
    ans=mone/sizeOfVecs
    #print ans
    return ans


def workingWithVecs(dbcon,vectotest):
    print("working with vecs function")
    #printVectorsSize(dbcon)
    for i in range (1,20):
        angel = angelBetweenTwoVecs(vectotest,getVectorOfEmotion(dbcon, i))
        print ("angel between requested vector, %s: %0.4f" % (emotionIDToName(dbcon, i), angel))




def printClosestVectorNames(dbcon, vec):
    print ("this function will find the closest vector.")
    templist=[]
    for i in range (1,373):
        newAngel= angelBetweenTwoVecs(vec,getVectorOfEmotion(dbcon,i))
        #print ("angel between %0d, %0d: %0.4f" % (7, i, newAngel))
        templist.append((newAngel,i))

    sorted_by_angel = sorted(templist, key=lambda tup: tup[0], reverse=True)

    #print(sorted_by_angel)
    for i in range(0,5):
        print ("#%0d - vec: %s. angel: %0.4f" % (i+1,emotionIDToName(dbcon,sorted_by_angel[i][1]),sorted_by_angel[i][0]))




def main():
    print(2)
    dbcon=initEmoitionsDB()
    print(3)
    basicQueries(dbcon)
    #workingWithVecs(dbcon)
    #printClosestVectorNames(dbcon,getVectorOfEmotion(dbcon,62))

    print(4)


if __name__ == '__main__':
    print(1)

    main()



