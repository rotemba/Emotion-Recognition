import csv

from numpy import genfromtxt
import init
import methods
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from numpy import linalg
from scipy.spatial import distance



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
        options=["Exit","angles between 2 emotions",'create a new vector','findClosestEmotion','findOppositeEmotion', 'get vector of emotion','buildNewVector']
        optDict={0: exit, 1: angles, 2: createVector, 3: findClosestEmotion,4: findOppositeEmotion, 5:getVector, 6:buildNewVector}
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
    methods.printClosestVectorNames(result)

def findMainEmotion(videoFrameArray):
    print("going to find the main emotion in video")

    onlyEmotions=videoFrameArray[2:]
    sumOfAllEmotions=map(lambda emotion: sum(map(lambda x: float(x), emotion[1:])), onlyEmotions)
    main_emotion=onlyEmotions[sumOfAllEmotions.index(max(sumOfAllEmotions))][0]
    for i in range (1,7):
        print ("feeling: %s, sum: %0.2f " %(videoFrameArray[i][0], sum(map(lambda x: float(x), (videoFrameArray[i])[1:]))))


    return main_emotion

# Neutral,Happy,Sad,Angry,Surprised,Scared,Disgusted
def getMixedVec(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar):
    list = [(float(NeutralScalar),"neutral"), (float(HappyScalar),"happiness"),(float(SadScalar),"sadness"),(float(AngryScalar),"anger"),
            (float(SurprisedScalar),"surprise"),(float(ScaredScalar),"scare"),(float(DisgustedScalar),"disgust")]
    #print list
    listWithVecs = map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x[1])), list)

    listOfScalars = map(lambda x: x[0], list)
    listOfNewVEcs = map(lambda scalar, vec: map(lambda x: scalar * x, vec), listOfScalars, listWithVecs)
    result = listOfNewVEcs[0]
    for i in range(1, len(listOfNewVEcs)):
        result = map(sum, zip(result, listOfNewVEcs[i]))



    return result

def euclidean_distance(first_vec,second_vec):
    if (len(first_vec) != len(second_vec)):
        print("!!ERROR!! vector lengths are not equal, vec_1 len %d , vec_2 len %d"%(len(first_vec),len((second_vec))))
        return -1
    dst = distance.euclidean(first_vec, second_vec)

    return dst


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
            cossimilary = methods.printClosestVectorNames(mixedVec)
            nearest_emotion = find_shortes_dist(mixedVec)
            emotion_name = methods.emotionIDToName(nearest_emotion[1])
            dist_value = nearest_emotion[0]
            #order = [x[1] for x in nearest_emotion]
            #if (i%20==0):
                #print ("frame %0d: angle to prev:%0.3f. angle to main emotion:%0.3f" %(i,angleToPrevVec,angleToMainVec))
            cursor.execute("INSERT INTO Video_analyze VALUES (?,?,?,?,?,?,?,?)",(video_number,i
                                                 ,angleToPrevVec, angleToMainVec ,emotion_name,dist_value,cossimilary[1],cossimilary[0]))

    init.dbcon.commit()

    print ("end of the table creation.")

def find_shortes_dist(vec):
    distance_list = list()
    with init.dbcon:
        cursor = init.dbcon.cursor()
        for ii in range(1,374):
            cursor.execute("SELECT * FROM Twitter WHERE ID = ?",  (ii,))

            emotion = cursor.fetchone()
            emotion= emotion[1:]
            dist = euclidean_distance(vec,list(emotion))
            distance_list.append((dist,ii))

        from operator import itemgetter

        return min(distance_list, key=itemgetter(0))  # faster solution
        #distance_list.sort(key=lambda x: x[0])


def visualizeData():
    print ("visualize data function")
    df = pd.read_sql_query("select * from Video_analyze ;", init.dbcon)
    print(df)
    plot_data = df['Angle_To_Main_Emotion']
    plot_data2 = df['Angle_To_Prev_Vec']
    plt.figure(1)
    plt.subplot(211)
    #plt.xlabel('Frame_number')
    plt.ylabel('angle_To_Main_Emotion')
    plt.title('angle_To_Main_Emotion')
    plt.plot(plot_data, 'g' ,label='My Data')

    plt.figure(1)
    plt.subplot(212)
    plt.xlabel('Frame_number')
    plt.ylabel('Cos similarity')
    plt.title('angle_To_Prev_Vec')
    plt.plot(plot_data2, 'b' ,label='My Data')
    plt.show()


def main():
    print pd.__file__
    init.initEmoitionsDB()

    #basicQueries()
    #workingWithVecs()
    ##printClosestVectorNames(getVectorOfEmotion(62))
    readVideoToDB('files/shortEmotion1.csv',1)
    visualizeData()


if __name__ == '__main__':

    main()


