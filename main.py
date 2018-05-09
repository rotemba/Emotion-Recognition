from __future__ import division
import csv

from numpy import genfromtxt
from numpy import  random
import init
import methods
import algebra
import random
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from numpy import linalg
from scipy.spatial import distance
import os



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



def get_sql_query(video_num):
    if (video_num==1):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 1", init.dbcon)
    if (video_num==2):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 2", init.dbcon)
    if (video_num==3):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 3", init.dbcon)
    if (video_num==4):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 4", init.dbcon)
    if (video_num==5):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 5", init.dbcon)
    if (video_num==6):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 6", init.dbcon)
    if (video_num==7):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 7", init.dbcon)
    if (video_num==8):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 8", init.dbcon)
    if (video_num==9):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 9", init.dbcon)
    if (video_num==10):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 10", init.dbcon)
    if (video_num==11):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 11", init.dbcon)
    if (video_num==12):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 12", init.dbcon)
    if (video_num==13):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 13", init.dbcon)
    if (video_num==14):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 14", init.dbcon)
    if (video_num==15):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 15", init.dbcon)
    if (video_num==16):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 16", init.dbcon)
    if (video_num==17):
        df = pd.read_sql_query("select * from Video_analyze WHERE VideoID = 17", init.dbcon)
    return df

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




def angles():
    print ("angles between 2 vectors")
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID")
        data = cursor.fetchall()
        for row in data:
            print row[0]

    emotion1 = raw_input("put first emotions please")
    emotion2 = raw_input("put second emotions please")
    methods.angles_between_two_emotions(emotion1, emotion2)


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
        options=["Exit",
                 "angles between 2 emotions",
                 'create a new vector',
                 'findClosestEmotion',
                 'findOppositeEmotion',
                 'get vector of emotion',
                 'buildNewVector',
                 'show video analysys']
        optDict={0: exit,
                 1: angles,
                 2: createVector,
                 3: findClosestEmotion,
                 4: findOppositeEmotion,
                 5: getVector,
                 6: buildNewVector,
                 7: show_video_analysis }
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
    methods.getClosestVectorNamesCosine(result)



    return result # ROTEM : something wrong here, we need to take a look at it.

def show_video_analysis():
    print ("Video analysis function.")
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT * FROM Videos")
        data = cursor.fetchall()
        while True:

            print ("Video number\t\t Main emotion \t\t Video Path")
            for row in data:
                print ("%0d\t\t\t\t\t %s \t\t\t\t %s" % (row[0],row[1],row[2]))
            chosen_video = int(input("Please enter video number"))
            video_path= data[chosen_video-1][2]
            print video_path
            show_result_for_video(chosen_video, video_path)


def show_result_for_video(video_num, video_path):
    print ("showing result for video %0d:%s" % (video_num,video_path))
    df = get_sql_query(video_num)
    command = 'open ' + video_path
    visualizeData(video_num)
    #os.system(command)

    print ("finished showing visualize")

def convertScalarsToListtuples(list):
    list = list = [(float(list[0]),"neutral"), (float(list[1]),"happiness"),(float(list[2]),"sadness"),(float(list[3]),"anger"),
            (float(list[4]),"surprise"),(float(list[5]),"scare"),(float(list[6]),"disgust")]
    return list

# Neutral,Happy,Sad,Angry,Surprised,Scared,Disgusted
def getMixedVec(NeutralScalar = 0,HappyScalar = 0,SadScalar = 0,AngryScalar = 0 ,SurprisedScalar = 0 ,ScaredScalar = 0 ,DisgustedScalar = 0 ,given_list = 0 ):
    if given_list == 0:
        list_analyzed = [NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar]
    else:
        list_analyzed = given_list
    list_analyzed = convertScalarsToListtuples(list_analyzed)
    listWithVecs = map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x[1])), list_analyzed)

    listOfScalars = map(lambda x: x[0], list_analyzed)
    listOfNewVEcs = map(lambda scalar, vec: map(lambda x: scalar * x, vec), listOfScalars, listWithVecs)
    result = listOfNewVEcs[0]
    for i in range(1, len(listOfNewVEcs)):
        result = map(sum, zip(result, listOfNewVEcs[i]))

    return result


def readVideoToDB(video_path, video_number):
    print("%0d:inserting %s to db " % (video_number,video_path))
    videoFrameArray = genfromtxt(video_path, delimiter=',')
    with open(video_path, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        arr = [[] for _ in range(8)]
        print arr
        for row in readCSV:
            for index in range(0, 8):
                if row[1] == 'FIND_FAILED' or row[1] == 'FIT_FAILED':
                    break
                data = row[index]
                arr[index].append(data)
    name_of_main_emotion=findMainEmotion(arr)
    print ("main emotion:%s" % name_of_main_emotion)
    id = methods.emotionNameToEmotionID(name_of_main_emotion)
    print id
    vector_of_main_emotion=methods.getVectorOfEmotion(methods.emotionNameToEmotionID(name_of_main_emotion))
    prev_vec= getMixedVec(arr[1][1],arr[2][1],arr[3][1],arr[4][1],arr[5][1],arr[6][1],arr[7][1])
    with init.dbcon:
        cursor=init.dbcon.cursor()
        cursor.execute("INSERT OR REPLACE INTO Videos VALUES (?,?)", (video_number, name_of_main_emotion))
        for i in range (1, len(arr[0])):
            #print ("framte number: %0d / %0d" %(i,len(arr[0])))
            if videoFrameArray[i][1]== 'FIND_FAILED' or videoFrameArray[i][1] == 'FIT_FAILED':
                    print ("cant put inside DB")
                    break
            #print videoFrameArray[i]
            cursor.execute("""INSERT INTO Video_Data_Raw VALUES (?,?,?,?,?,?,?,?,?)""",(video_number,i,
                                        arr[1][i],arr[2][i],arr[3][i],arr[4][i],arr[5][i],
                                        arr[6][i],arr[7][i]))
            #Neutral,Happy,Sad,Angry,Surprised,Scared,Disgusted
            mixedVec=getMixedVec(arr[1][i],arr[2][i],arr[3][i],arr[4][i],arr[5][i],arr[6][i],arr[7][i])

            cursor.execute("""INSERT OR REPLACE INTO Video_Vecs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                           (video_number,i,mixedVec[0],mixedVec[1],mixedVec[2],mixedVec[3],mixedVec[4],mixedVec[5],mixedVec[6],mixedVec[7],mixedVec[8],mixedVec[9],mixedVec[10],
            mixedVec[11],mixedVec[12],mixedVec[13],mixedVec[14],mixedVec[15],mixedVec[16],mixedVec[17],mixedVec[18],mixedVec[19],mixedVec[20],
            mixedVec[21],mixedVec[22],mixedVec[23],mixedVec[24],mixedVec[25],mixedVec[26],mixedVec[27],mixedVec[28],mixedVec[29],mixedVec[30],
            mixedVec[31],mixedVec[32],mixedVec[33],mixedVec[34],mixedVec[35],mixedVec[36],mixedVec[37],mixedVec[38],mixedVec[39],mixedVec[40],
            mixedVec[41],mixedVec[42],mixedVec[43],mixedVec[44],mixedVec[45],mixedVec[46],mixedVec[47],mixedVec[48],mixedVec[49]))
            angleToPrevVec=methods.angleBetweenTwoVecs(prev_vec,mixedVec)
            angleToMainVec = methods.angleBetweenTwoVecs(vector_of_main_emotion, mixedVec)
            prev_vec = mixedVec
            cossimilary = methods.getClosestVectorNamesCosine(mixedVec)
            nearest_emotion = methods.find_shortes_dist(mixedVec)
            emotion_name = methods.emotionIDToName(nearest_emotion[1])
            dist_value = nearest_emotion[0]
            closestVectorByCosSimilarity = methods.getClosestVectorNamesCosine(mixedVec)
            closestVectorCosSimName= methods.emotionIDToName(closestVectorByCosSimilarity[1])
            closestVectorCosSimAngel= closestVectorByCosSimilarity[0]
            print ("closest by cos-similarity:%s.\t angel:%0.4f" %(closestVectorCosSimName,closestVectorCosSimAngel))
            #order = [x[1] for x in nearest_emotion]
            #if (i%20==0):
                #print ("frame %0d: angle to prev:%0.3f. angle to main emotion:%0.3f" %(i,angleToPrevVec,angleToMainVec))
            cursor.execute("INSERT INTO Video_analyze VALUES (?,?,?,?,?,?,?,?)",(video_number,i
                                                 ,angleToPrevVec, angleToMainVec ,emotion_name,dist_value,cossimilary[1],cossimilary[0]))

    init.dbcon.commit()

    print ("end of the table creation.")

def visualizeData(videoid):
    print ("visualize data function")

    df = get_sql_query(videoid)
    print df
    # print(data)
    plot_data1 = df['Angle_To_Main_Emotion']
    plot_data2 = df['Angle_To_Prev_Vec']
    plot_data3 = df['DKL_VALUE']

    plt.figure(figsize=(12, 12))
    plt.subplot(3, 1, 1)
    #plt.xlabel('Frame_number')
    plt.ylabel('angle_To_Main_Emotion')
    plt.title('angle_To_Main_Emotion')
    plt.plot(plot_data1, 'g' ,label='My Data')

    plt.subplot(3,1,2)
    #plt.xlabel('Frame_number')
    plt.ylabel('Cos similarity')
    plt.title('angle_To_Prev_Vec')
    plt.plot(plot_data2, 'b' ,label='My Data')


    plt.subplot(3,1,3)
    plt.xlabel('Frame_number')
    plt.ylabel('DKL')
    plt.title('DKL_VALUE')
    plt.plot(plot_data3, 'R' ,label='My Data')
    plt.show()


def creatAndInsertFakeVideos(fromIndex , toIndex, video_index):
    path = 'ShortVideos/fake'+str(video_index)+'_not_exist'
    print ("ID [%0d] :creating fake:%s , from:%0d -> %0d" %(video_index,path,fromIndex,toIndex))
    frames = []
    x = 0.05
    frame=[0.001,0.001,0.001,0.001,0.001,0.001,0.001]
    frame[fromIndex]=1
    newframe = map(lambda x: float("%0.5f" % x), frame)
    frames.append(newframe)
    for i in range(0, 21):
        newframe = map(lambda x: float("%0.5f" % x), frame)
        #newframe = map(lambda x: float(x), newframe)
        if (i == 20):
            newframe[fromIndex] = 0.0001
        frames.append(newframe)
        frame[fromIndex]-=x
        frame[toIndex]+=x
    init.InsertVideoAndAnalyze(frames, video_index, path)


def fakeVideos():
    index=50
    for i in range(0, 7):
        for j in range(i + 1, 7):
            index+=1
            creatAndInsertFakeVideos(i,j,index)

def createRandomFrame():
    result_list = list()
    c = [0,0,0,0,0,0,0]
    for j in range(1,10):
        for i in range(0,len(c)):
            c[i] = random.random()
        c = methods.normalize_vec_l1(c)
        frame_vector = getMixedVec(given_list= c)
        print c
        result = methods.getClosestVectorNamesCosine(frame_vector)
        result_list.append( result[1] )
        print result[1]

    from collections import Counter
    emotion_counts = Counter(result_list)
    print emotion_counts
    df = pd.DataFrame.from_dict(emotion_counts, orient='index')
    df.plot()



def main():

    print pd.__file__
    init.initEmoitionsDB()
    algebra.main()
    #basicQueries()
    #workingWithVecs()
    ##getClosestVectorNamesCosine(getVectorOfEmotion(62))
    #readVideoToDB('files/shortEmotion1.csv',1)
    #init.insertAllVideosToDB()
    #visualizeData(1)
    #DKL_method()
    #fakeVideos()
    #algebra.map_euclid_distances()
    #createRandomFrame()

    
if __name__ == '__main__':

    main()

