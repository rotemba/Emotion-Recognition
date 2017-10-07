import sqlite3
import os

from numpy import genfromtxt
import sqlite3
import os
import csv
from init import initEmoitionsDB
from init import readTableFromCSV
import math

def basicQueries():
    while True:
        options=["Exit","angles between 2 emotions",'create a new vector','findClosestEmotion','findOppositeEmotion', 'get vector of emotion','buildNewVector']
        optDict={0: exit, 1: angels, 2: createVector, 3: findClosestEmotion,4: findOppositeEmotion, 5:getVector, 6:buildNewVector}
        print("please choose the query to run:")
        print options
        for i in options:
            print (  ""+str(options.ingitdex(i))+" - "+ i)
        num_of_query = input("choose query :")
        print ("query chosen:: %s" % options[num_of_query])
        if num_of_query > 0:
            optDict[num_of_query]()
        else:
            break



def angels ():
    print ("angels between 2 vectors")
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID")
        data= cursor.fetchall()
        for row in data:
            print row[0]



    emotion1 = raw_input("put first emotions please")
    emotion2 = raw_input("put second emotions please")
    angels_between_two_emotions(emotion1,emotion2)

def angels_between_two_emotions (emotion1, emotion2):
    print ("angel between two emotions function")
    with dbcon:
        cursor=dbcon.cursor()
        id1=emotionNameToEmotionID(emotion1)
        id2=emotionNameToEmotionID(emotion2)
        print ("emotion1 :" + str(id1))
        print ("emotion2 :" + str(id2))
        cursor.execute("SELECT VALUE FROM Relations WHERE X = (?) AND  Y = (?)", (id1,id2,) )
        angel=cursor.fetchone()
        print ("angel between " + emotion1 + " and " + emotion2 +" is : " +str(angel[0]))

def createVector():
    print("creating vector")

def findClosestEmotion():
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
            print (str(i)+":[" + emotion1 + "," + emotionIDToName( data[1]) + "] similarity:" + str(data[2]))

def findOppositeEmotion():
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
            print (str(i)+":[" + emotion1 + "," + emotionIDToName( data[1]) + "] similarity:" + str(data[2]))


def emotionIDToName( emotionID):
    with dbcon:
        cursor=dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID WHERE ID = ?", (emotionID,))
        name=cursor.fetchone()
        #print("got id number:" + str(emotionID) +" - name: "+ name[0])
        return (name[0])


def buildVectorFromCSV(row):
    emotionlistfromcsvbyID = [246, 183, 295, 17, 329 , 299 , 114]
    listOfTuplesPerFrame = list()
    arr = readTableFromCSV()
    for i in range(1,8):
        scalar = arr[i][row]
        pair = (scalar,emotionIDToName(emotionlistfromcsvbyID[i]))
        row+=1
        listOfTuplesPerFrame.append(pair)

    return listOfTuplesPerFrame



def emotionNameToEmotionID(emotionName):
    with dbcon:
        cursor=dbcon.cursor()
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotionName,))
        emotionID=cursor.fetchone()
        #print("got emotion name:" + emotionName +" - id: "+ str(emotionID[0]))
        return (emotionID[0])

def buildListContainsAll():
    num_of_emotion = 373
    value = float(1/float(7))
    listOfTuples = list()
    for i in range(1,num_of_emotion):
        if (i == 246) or (i == 183) or (i == 295) or (i == 17) or (i == 114) or (i == 299) or (i == 329):
            pair = (value,emotionIDToName(i))
            listOfTuples.append(pair)
    print listOfTuples
    return listOfTuples


def askScalarsFromUsers():
    counter = 1
    sumOfScalars = 0
    print("this function asks the user for scalars and emotions.")
    listOfTuples = list()
    while sumOfScalars < 1:
        emotion = raw_input("Please enter the name of emotion number %d " % counter)
        if emotion =='all':
            return buildListContainsAll()
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


def buildNewVector():
    list = askScalarsFromUsers()
    listWithVecs=map(lambda x: getVectorOfEmotion(emotionNameToEmotionID(x[1])),list)
    listOfScalars=map(lambda x: x[0], list)
    listOfNewVEcs=map(lambda scalar, vec: map(lambda x: scalar * x, vec),listOfScalars,listWithVecs )
    result = listOfNewVEcs[0]
    for i in range(1,len(listOfNewVEcs)):
        result = map(sum,zip(result,listOfNewVEcs[i]))
    print_nicely_vec(result)
    printClosestVectorNames(result)


def getVector():
    print("this function will retrive the vector of emotion and print it.")
    emotion1 = raw_input("put emotion name please")
    vector= getVectorOfEmotion(emotionNameToEmotionID(emotion1))
    newVector=map(prettyFloat,vector)
    print newVector
    return (vector)

def computeNewVec(): # expected format: list ( scalar, vector )
    print ("for now going to work on fool emotion with scalar of 0.5")
    foolVec=getVectorOfEmotion(emotionNameToEmotionID("fool"))
    scalar=0.5
    newFoolVec=map((lambda x: x * scalar), foolVec)
    print("beofre:")
    print (foolVec)
    print ("after:")
    print (newFoolVec)
    print ("pretty print:")
    print (map((lambda x:  "%0.4f" % x ), newFoolVec))


def angelBetweenTwoVecs( vec1, vec2):
    #print ("angel between 2 vecs function.")

    sizeOfVec1=sizeOfSingleVec(vec1)
    sizeOfVec2=sizeOfSingleVec(vec2)
    mone=sum((a*b) for a, b in zip(vec1, vec2))
    sizeOfVecs=(sizeOfVec1*sizeOfVec2)
    ans=mone/sizeOfVecs
    #print ans
    return ans


def workingWithVecs(vectotest):
    print("working with vecs function")
    #printVectorsSize()
    for i in range (1,20):
        angel = angelBetweenTwoVecs(vectotest,getVectorOfEmotion( i))
        print ("angel between requested vector, %s: %0.4f" % (emotionIDToName( i), angel))




def printClosestVectorNames( vec):
    print ("this function will find the closest vector.")
    templist=[]
    for i in range (1,373):
        newAngel= angelBetweenTwoVecs(vec,getVectorOfEmotion(i))
        #print ("angel between %0d, %0d: %0.4f" % (7, i, newAngel))
        templist.append((newAngel,i))

    sorted_by_angel = sorted(templist, key=lambda tup: tup[0], reverse=True)

    #print(sorted_by_angel)
    for i in range(0,5):
        print ("#%0d - vec: %s. angel: %0.4f" % (i+1,emotionIDToName(sorted_by_angel[i][1]),sorted_by_angel[i][0]))

    for i in range (368, 372):
        print ("#%0d - vec: %s. angel: %0.4f" % (i + 1, emotionIDToName(sorted_by_angel[i][1]), sorted_by_angel[i][0]))



def main():
    print(2)
    global dbcon
    dbcon=initEmoitionsDB()
    print(3)
    basicQueries()
    #workingWithVecs()
    ##printClosestVectorNames(getVectorOfEmotion(62))

    print(4)


if __name__ == '__main__':
    print(1)

    main()




def getVectorOfEmotion( emotionID):
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM Twitter WHERE ID = ?", (emotionID,))
        vector=cursor.fetchone()
        return (vector[1:len(vector)])


def prettyFloat(num):
        return "%0.4f" % num


def print_nicely_vec(vec):
    print(map((lambda x: "%0.4f" % x), vec))


def sizeOfSingleVec(vec):
    return math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, vec)))


def printVectorsSize():
    for i in range(1,374):
        vec=getVectorOfEmotion(i)
        sizeOfVec = sizeOfSingleVec(vec)
        print (str(i)+":vector-"+ emotionIDToName(i)+ " size: "+ str(sizeOfVec))

