#from init import initRelationTable
from numpy import genfromtxt
import sqlite3
import os
import csv
import methods
import glob
import methods

global dimensions_of_vector
global num_of_vectors

# Working with human space vectors.
dimensions_of_vector= 25
num_of_vectors = 415


# Working with the twiter vectors:
# dimensions_of_vector= 50
# num_of_vectors = 415







def initTwitterTable(dbcon):
    print ("init twitter table")

def initEmotionIDTable(dbcon):
    print("init emotions id table")



def initEmoitionsDB():
    databaseexisted = os.path.isfile('Emotions.db')
    global dbcon
    dbcon = sqlite3.connect("Emotions.db")
    if not databaseexisted:
        str = ("ID INTEGER NOT NULL REFERENCES  EmotionsID(ID), %s" % ','.join("X%d REAL" % i for i in range(dimensions_of_vector)))
        strOfVecs=(','.join("X%d REAL" % i for i in range(dimensions_of_vector)))
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("CREATE TABLE EmotionsID(ID INTEGER PRIMARY KEY NOT NULL ,Emotion_name VARCHAR(20) NOT NULL )")
            cursor.execute("CREATE TABLE Twitter (%s)" % str )
            cursor.execute("""CREATE TABLE Cos_Similarity(X INTEGER NOT NULL,
                                                                  Y INTEGER NOT NULL,
                                                                 Angle REAL NOT NULL)""")
            cursor.execute("CREATE TABLE Videos(VideoID INTEGER PRIMARY KEY NOT NULL, Main_motion VARCHAR(20) NOT NULL, Video_path VARCHAR (70) NOT NULL)")
            cursor.execute("CREATE TABLE Video_Vecs (VideoID INTEGER NOT NULL REFERENCES Videos(VideoID), Frame_number INTEGER NOT NULL, %s , PRIMARY KEY (VideoID, Frame_number))" % strOfVecs)
            cursor.execute("""CREATE TABLE Video_analyze (VideoID INTEGER NOT NULL REFERENCES Videos(VideoID), 
                                                          Frame_number INTEGER NOT NULL REFERENCES Video_Vecs(Frame_number),
                                                           Angle_To_Prev_Vec REAL NOT NULL,
                                                           Angle_To_Main_Emotion REAL NOT NULL,
                                                           first_knn VARCHAR(20) NOT NULL,
                                                           first_distance REAL NOT NULL,
                                                           second_knn VARCHAR(20) NOT NULL,
                                                           second_distance REAL NOT NULL,
                                                           third_knn VARCHAR(20) NOT NULL,
                                                           third_distance REAL NOT NULL,
                                                           fourth_knn VARCHAR(20) NOT NULL,
                                                           fourth_distance REAL NOT NULL,
                                                           fifth_knn VARCHAR(20) NOT NULL,
                                                           fifth_distance REAL NOT NULL,
                                                           sixth_knn VARCHAR(20) NOT NULL,
                                                           sixth_distance REAL NOT NULL,
                                                           seventh_knn VARCHAR(20) NOT NULL,
                                                           seventh_distance REAL NOT NULL,
                                                           eighth_knn VARCHAR(20) NOT NULL,
                                                           eighth_distance REAL NOT NULL,
                                                           ninth_knn VARCHAR(20) NOT NULL,
                                                           ninth_distance REAL NOT NULL,
                                                           tenth_knn VARCHAR(20) NOT NULL,
                                                           tenth_distance REAL NOT NULL,
                                                           cos_similarity_emotion VARCHAR(20) NOT NULL,
                                                           angle REAL NOT NULL,
                                                           DKL_VALUE REAL NOT NULL)""")
            cursor.execute("""CREATE TABLE Video_Data_Raw (VideoID INTEGER NOT NULL REFERENCES Videos(VideoID),
                                                          Frame_number INTEGER NOT NULL REFERENCES Video_Vecs(Time),
                                                          Neutral REAL NOT NULL,
                                                          Happy REAL NOT NULL,
                                                          Sad REAL NOT NULL,Angry REAL NOT NULL,
                                                          Surprised REAL NOT NULL,Scared REAL NOT NULL,
                                                          DisgustedNeutral REAL NOT NULL)""")


            print("DONE creating the tables")
            #twiter_path = "files/twitter_dict.csv"

            #pathOfTwitter = "files/Twitter_normalize.csv"
            pathOfTwitter = "files/humanSpace-414-25d.csv"
            pathOfEmotionRealations="files/emotionsAngelsToDB.csv"
            fileObject = csv.reader(pathOfTwitter)

            twitDict = genfromtxt(pathOfTwitter, delimiter=',', dtype=None)
            row_count = num_of_vectors
            print ("Inserting data to table")

            str = '?'
            for x in range(0, dimensions_of_vector):
                str = str + ',?'

            for row in range(1, row_count):
                if (dimensions_of_vector==50):
                    cursor.execute('''INSERT INTO Twitter VALUES (%s)''' % str,(row, twitDict[row][1],twitDict[row][2],twitDict[row][3],twitDict[row][4],twitDict[row][5],twitDict[row][6],twitDict[row][7],twitDict[row][8],twitDict[row][9],twitDict[row][10],
                                      twitDict[row][11],twitDict[row][12],twitDict[row][13],twitDict[row][14],twitDict[row][15],twitDict[row][16],twitDict[row][17],twitDict[row][18],twitDict[row][19],twitDict[row][20],
                                      twitDict[row][21],twitDict[row][22],twitDict[row][23],twitDict[row][24],twitDict[row][25],twitDict[row][26],twitDict[row][27],twitDict[row][28],twitDict[row][29],twitDict[row][30],
                                      twitDict[row][31],twitDict[row][32],twitDict[row][33],twitDict[row][34],twitDict[row][35],twitDict[row][36],twitDict[row][37],twitDict[row][38],twitDict[row][39],twitDict[row][40],
                                      twitDict[row][41],twitDict[row][42],twitDict[row][43],twitDict[row][44],twitDict[row][45],twitDict[row][46],twitDict[row][47],twitDict[row][48],twitDict[row][49],twitDict[row][50]))
                else:
                    cursor.execute('''INSERT INTO Twitter VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' , (
                    row, twitDict[row][1], twitDict[row][2], twitDict[row][3], twitDict[row][4], twitDict[row][5],
                    twitDict[row][6], twitDict[row][7], twitDict[row][8], twitDict[row][9], twitDict[row][10],
                    twitDict[row][11], twitDict[row][12], twitDict[row][13], twitDict[row][14], twitDict[row][15],
                    twitDict[row][16], twitDict[row][17], twitDict[row][18], twitDict[row][19], twitDict[row][20],
                    twitDict[row][21], twitDict[row][22], twitDict[row][23], twitDict[row][24], twitDict[row][25]))

            print ("Twitter vectors are inside the DB")
            for row in range(1, row_count):
                cursor.execute('''INSERT INTO EmotionsID(ID, Emotion_name) VALUES (?,?)''' ,(row,twitDict[row][0]))
            dbcon.commit()
            print ("Twitter emotions names are inside the DB")
            print ("creating cartesian emotions table")
            relationArray = genfromtxt(pathOfEmotionRealations, delimiter=',')
            rows = len(relationArray)
            cols = len(relationArray)
            #print relationArray
            for row in range(0, rows):
                for col in range(0, cols):
                    cursor.execute("INSERT  INTO Cos_Similarity VALUES (?,?,?)", (row+1, col+1, relationArray[row][col]))
                    # print ("added value (%f) to the DB" % relationArray[row][col])
            dbcon.commit()
            #TODO: UNCOMMENT!!
            insertAllVideosToDB('/files/ShortVideos', '\t')
            #insertAllVideosToDB('/files/newShortVideos', '\t')
            print ("end of the table creation.")
    else:
        print ("db exists")


def readTableFromCSV(): #TODO add argument as an file path
    with open('files/Participant_8_csv_format.csv', 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        arr = [[] for _ in range(8)]
        print arr
        for row in readCSV:
            for index in range(0, 8):
                if row[1] == 'FIND_FAILED' or row[1] == 'FIT_FAILED':
                    break
                data = row[index]
                arr[index].append(data)

    arr_duplicate = [[] for _ in range(8)]
    for i in range(0, len(arr)):
        for index, item in enumerate(arr[i]):
            if i > 0 and index > 0:
                arr_duplicate[i].append(float(item))
            else:
                arr_duplicate[i].append(item)

    return arr_duplicate


def InsertVideoAndAnalyze (ListOfFrames, videoNumber,filename):
    name_of_main_emotion = methods.findMainEmotion(ListOfFrames)


    print ("proccesing video [%0d]:%s\nmain emotion:%s." % (videoNumber, filename,name_of_main_emotion))
    id = methods.emotionNameToEmotionID(name_of_main_emotion)
    vector_of_main_emotion = methods.getVectorOfEmotion(methods.emotionNameToEmotionID(name_of_main_emotion))
    ListOfEmotions = ["neutral", "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    prev_vec = methods.getMixedVec(ListOfFrames[0][0], ListOfFrames[0][1], ListOfFrames[0][2], ListOfFrames[0][3],
                           ListOfFrames[0][4], ListOfFrames[0][5], ListOfFrames[0][6],listOfGeneralVecs)
    arr=ListOfFrames
    video_path = 'files/Videos/'+filename[(filename.index("ShortVideos" )+12):filename.index("_")] + ".mp4"
    with dbcon:
        cursor=dbcon.cursor()
        cursor.execute("INSERT OR REPLACE INTO Videos VALUES (?,?,?)", (videoNumber, name_of_main_emotion,video_path))
        for i in range (0, len(ListOfFrames)):
            arr[i]=methods.normalize_vec( arr[i], 1)
            #print ("framte number: %0d / %0d" %(i,len(arr[0])))
            #if videoFrameArray[i][1]== 'FIND_FAILED' or videoFrameArray[i][1] == 'FIT_FAILED':
            #        print ("cant put inside DB")
            #        break
            #print videoFrameArray[i]
            cursor.execute("""INSERT INTO Video_Data_Raw VALUES (?,?,?,?,?,?,?,?,?)""",(videoNumber,i+1,
                                        arr[i][0],arr[i][1],arr[i][2],arr[i][3],arr[i][4],
                                        arr[i][5],arr[i][6]))
            #Neutral,Happy,Sad,Angry,Surprised,Scared,Disgusted
            mixedVec=methods.getMixedVec(arr[i][0],arr[i][1],arr[i][2],arr[i][3],arr[i][4],arr[i][5],arr[i][6],listOfGeneralVecs)

            if (dimensions_of_vector==50):
                cursor.execute(
                    """INSERT OR REPLACE INTO Video_Vecs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (videoNumber, i, mixedVec[0], mixedVec[1], mixedVec[2], mixedVec[3], mixedVec[4], mixedVec[5], mixedVec[6], mixedVec[7], mixedVec[8], mixedVec[9], mixedVec[10],
                     mixedVec[11], mixedVec[12], mixedVec[13], mixedVec[14], mixedVec[15], mixedVec[16], mixedVec[17],mixedVec[18], mixedVec[19], mixedVec[20],
                     mixedVec[21], mixedVec[22], mixedVec[23], mixedVec[24], mixedVec[25], mixedVec[26], mixedVec[27],mixedVec[28], mixedVec[29], mixedVec[30],
                     mixedVec[31], mixedVec[32], mixedVec[33], mixedVec[34], mixedVec[35], mixedVec[36], mixedVec[37],mixedVec[38], mixedVec[39], mixedVec[40],
                     mixedVec[41], mixedVec[42], mixedVec[43], mixedVec[44], mixedVec[45], mixedVec[46], mixedVec[47],mixedVec[48], mixedVec[49]))
            else:
                cursor.execute("""INSERT OR REPLACE INTO Video_Vecs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (videoNumber,i,mixedVec[0],mixedVec[1],mixedVec[2],mixedVec[3],mixedVec[4],mixedVec[5],mixedVec[6],mixedVec[7],mixedVec[8],mixedVec[9],mixedVec[10],
                mixedVec[11],mixedVec[12],mixedVec[13],mixedVec[14],mixedVec[15],mixedVec[16],mixedVec[17],mixedVec[18],mixedVec[19],mixedVec[20],
                mixedVec[21],mixedVec[22],mixedVec[23],mixedVec[24]))
            angleToPrevVec=methods.angleBetweenTwoVecs(prev_vec,mixedVec)
            angleToMainVec = methods.angleBetweenTwoVecs(vector_of_main_emotion, mixedVec)
            #print ("dkl distance between the vecs is: %0.6f" % (methods.dkl(prev_vec, mixedVec)))
            calculate_dkl = methods.calculate_dkl(arr[max(i-1,0)],arr[i])#TODO be SURE about order

            prev_vec = mixedVec
            cossimilary = methods.printClosestVectorNames(mixedVec)
            ten_knn_emotions=methods.get_three_closest_knn(mixedVec)
            closestVectorByCosSimilarity = methods.printClosestVectorNames(mixedVec)
            closestVectorCosSimName= closestVectorByCosSimilarity[1]
            closestVectorCosSimAngel= closestVectorByCosSimilarity[0]

            #print ("closest by cos-similarity:%s.\t angel:%0.4f" %(closestVectorCosSimName,closestVectorCosSimAngel))
            #order = [x[1] for x in nearest_emotion]
            #if (i%20==0):
                #print ("frame %0d: angle to prev:%0.3f. angle to main emotion:%0.3f" %(i,angleToPrevVec,angleToMainVec))
            cursor.execute("INSERT INTO Video_analyze VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(videoNumber,i,angleToPrevVec, angleToMainVec,
                                                                                           methods.emotionIDToName(ten_knn_emotions[0][1]),ten_knn_emotions[0][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[1][1]), ten_knn_emotions[1][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[2][1]), ten_knn_emotions[2][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[3][1]), ten_knn_emotions[3][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[4][1]), ten_knn_emotions[4][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[5][1]), ten_knn_emotions[5][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[6][1]), ten_knn_emotions[6][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[7][1]), ten_knn_emotions[7][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[8][1]), ten_knn_emotions[8][0],
                                                                                           methods.emotionIDToName(ten_knn_emotions[9][1]), ten_knn_emotions[9][0],
                                                                                            closestVectorCosSimName,closestVectorCosSimAngel,calculate_dkl))


    dbcon.commit()
    print ("finished proccesing video [%0d] " % videoNumber)



def insertAllVideosToDB(path_of_files, delimeter):
    print ("loading all video data to DB.")
    cwd = os.getcwd()
    print (cwd)
    path = cwd+path_of_files
    print (path)
    videoIndex = 0
    for filename in glob.glob(os.path.join(path, '*detailed.txt')):
        print(filename)
        videoIndex += 1
        print ("printing csv data of video[%0d]" % videoIndex)
        with open(filename, 'rU') as csvfile:
            readCSV = csv.reader(csvfile, dialect=csv.excel_tab)
            row_count = 0
            vecsDistribution = []
            for row in readCSV:
                row_count += 1

                if row_count > 9 :
                    print (row[0:8])
                    if (row[0] == 'Video Time'):
                        continue
                    if row[1] == 'FIND_FAILED' or row[1] == 'FIT_FAILED':
                        print ("**[Video %0d][%s] has no values, skipping this frame!**" % (videoIndex,row[0]))
                        continue
                    else:
                        rowCastedToFloat=map((lambda x: float(x)) ,row[1:8])
                        #print (rowCastedToFloat)
                        vecsDistribution.append(rowCastedToFloat)
                    #print ("sum of row: %0.4f" % (sum (map((lambda x : float(x)),  row[1:8]))))


                    #print(map((lambda x: "%0.4f" % x), vec))
        InsertVideoAndAnalyze(vecsDistribution, videoIndex, filename)



