import sqlite3
import os

from numpy import genfromtxt
import sqlite3
import os
import csv
import init
import methods

def findOppositeEmotion():
    print("this function will find the opposite emotion")
    emotion1 = raw_input("put emotion name please")
    with init.dbcon:
        cursor = init.dbcon.cursor()
        # CT EmotionsID.ID, Relations."Value" FROM EmotionsID JOIN Relations ON EmotionsID.ID = Relations.X WHERE Emotion_name =""")
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        id1 = cursor.fetchone()
        print (emotion1 + " : " + str(id1[0]))
        cursor.execute("SELECT * FROM Relations WHERE X = (?) ORDER BY VALUE ASC ", (id1[0],))
        for i in range(1, 4):
            data = cursor.fetchone()
            print (str(i) + ":[" + emotion1 + "," + methods.emotionIDToName(data[1]) + "] similarity:" + str(data[2]))


def findClosestEmotion():
    print("this function will find the closest emotion")
    emotion1 = raw_input("put emotion name please")
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotion1,))
        id1 = cursor.fetchone()
        print (emotion1 + " : " + str(id1[0]))
        cursor.execute("SELECT * FROM Relations WHERE X = (?) ORDER BY VALUE DESC ", (id1[0],))
        for i in range(1, 4):
            data = cursor.fetchone()
            print (str(i) + ":[" + emotion1 + "," + methods.emotionIDToName(data[1]) + "] similarity:" + str(data[2]))




def angels():
    print ("angels between 2 vectors")
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID")
        data = cursor.fetchall()
        for row in data:
            print row[0]

    emotion1 = raw_input("put first emotions please")
    emotion2 = raw_input("put second emotions please")
    methods.angels_between_two_emotions(emotion1, emotion2)


def getVector():
    print("this function will retrive the vector of emotion and print it.")
    emotion1 = raw_input("put emotion name please")
    vector= methods.getVectorOfEmotion(methods.emotionNameToEmotionID(emotion1))
    newVector=map(methods.prettyFloat,vector)
    print newVector
    return (vector)

def createVector():
    print("creating vector")

def basicQueries():
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
            optDict[num_of_query]()
        else:
            break



def buildVectorFromCSV(row):
    emotionlistfromcsvbyID = [246, 183, 295, 17, 329 , 299 , 114]
    listOfTuplesPerFrame = list()
    arr = init.readTableFromCSV()
    for i in range(1,8):
        scalar = arr[i][row]
        pair = (scalar,methods.emotionIDToName(emotionlistfromcsvbyID[i]))
        row+=1
        listOfTuplesPerFrame.append(pair)

    return listOfTuplesPerFrame





def buildListContainsAll():
    num_of_emotion = 373
    value = float(1/float(7))
    listOfTuples = list()
    for i in range(1,num_of_emotion):
        if (i == 246) or (i == 183) or (i == 295) or (i == 17) or (i == 114) or (i == 299) or (i == 329):
            pair = (value,methods.emotionIDToName(i))
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
    listWithVecs=map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x[1])),list)
    listOfScalars=map(lambda x: x[0], list)
    listOfNewVEcs=map(lambda scalar, vec: map(lambda x: scalar * x, vec),listOfScalars,listWithVecs )
    result = listOfNewVEcs[0]
    for i in range(1,len(listOfNewVEcs)):
        result = map(sum,zip(result,listOfNewVEcs[i]))

    methods.print_nicely_vec(result)
    methods.printClosestVectorNames(result)






def main():
    print(2)

    init.initEmoitionsDB()
    print(3)
    basicQueries()
    #workingWithVecs()
    ##printClosestVectorNames(getVectorOfEmotion(62))


if __name__ == '__main__':
    print(1)

    main()


