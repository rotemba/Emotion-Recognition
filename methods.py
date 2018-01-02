import init
import math
from numpy import linalg
from scipy.spatial import distance
import numpy as np






def angles_between_two_emotions (emotion1, emotion2):
    print ("angle between two emotions function")
    with init.dbcon:
        cursor=init.dbcon.cursor()
        id1=emotionNameToEmotionID(emotion1)
        id2=emotionNameToEmotionID(emotion2)
        print ("emotion1 :" + str(id1))
        print ("emotion2 :" + str(id2))
        cursor.execute("SELECT VALUE FROM Relations WHERE X = (?) AND  Y = (?)", (id1,id2,) )
        angle=cursor.fetchone()
        print ("angle between " + emotion1 + " and " + emotion2 +" is : " +str(angle[0]))



def workingWithVecs(vectotest):
    print("working with vecs function")
    #printVectorsSize()
    for i in range (1,20):
        angle = angleBetweenTwoVecs(vectotest,getVectorOfEmotion( i))
        print ("angle between requested vector, %s: %0.4f" % (emotionIDToName( i), angle))


def angleBetweenTwoVecs( vec1, vec2):
    #print ("angle between 2 vecs function.")

    sizeOfVec1=sizeOfSingleVec(vec1)
    sizeOfVec2=sizeOfSingleVec(vec2)
    from scipy import spatial
    result = 1 - spatial.distance.cosine(vec1, vec2)
    #mone=sum((a*b) for a, b in zip(vec1, vec2))
    #sizeOfVecs=(sizeOfVec1*sizeOfVec2)
    #ans=mone/sizeOfVecs
    #print ans
    return result


def printClosestVectorNames( vec):
    templist=[]
    for i in range (1,373):
        newangle= angleBetweenTwoVecs(vec,getVectorOfEmotion(i))
        #print ("angle between %0d, %0d: %0.4f" % (7, i, newangle))
        templist.append((newangle,i))

    from operator import itemgetter

    result = max(templist, key=itemgetter(0))  # faster solution
    result1 = (result[0], emotionIDToName(result[1]))
    return result1

def printClosestVectorByCosSimilarity(vec):
    templist=[]
    for i in range (1,373):
        newangle= angleBetweenTwoVecs(vec,getVectorOfEmotion(i))
        #print ("angle between %0d, %0d: %0.4f" % (7, i, newangle))
        templist.append((newangle,i))
    from operator import itemgetter


    result = max(templist, key=itemgetter(0))  # faster solution
    result1 = (result[0], emotionIDToName(result[1]))  #angel,emotion_name
    return result1


def emotionIDToName(emotionID):
    with init.dbcon:
        cursor=init.dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID WHERE ID = ?", (emotionID,))
        name=cursor.fetchone()
        #print("got id number:" + str(emotionID) +" - name: "+ name[0])
        return (str(name[0]))

def emotionNameToEmotionID(emotionName):
    if (emotionName=="Happy"):
        #print ("searching for happiness instead of Happy")
        return emotionNameToEmotionID("happiness")
    if (emotionName =='Sad'):
        return emotionNameToEmotionID('sadness')
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name = ?", (emotionName,))
        emotionID=cursor.fetchone()
        #print("got emotion name:" + emotionName +" - id: "+ str(emotionID[0]))
        return (emotionID[0])


def print_nicely_vec(vec):
    print(map((lambda x: "%0.4f" % x), vec))


def sizeOfSingleVec(vec):
    return math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, vec)))


def printVectorsSize():
    for i in range(1,374):
        vec=getVectorOfEmotion(i)
        sizeOfVec = sizeOfSingleVec(vec)
        print (str(i)+":vector-"+ emotionIDToName(i)+ " size: "+ str(sizeOfVec))





def computeNewVec(): # expected format: list ( scalar, vector )
    print ("for now going to work on fool emotion with scalar of 0.5")
    foolVec = getVectorOfEmotion(emotionNameToEmotionID("fool"))
    scalar=0.5
    newFoolVec=map((lambda x: x * scalar), foolVec)
    print("beofre:")
    print (foolVec)
    print ("after:")
    print (newFoolVec)
    print ("pretty print:")
    print (map((lambda x:  "%0.4f" % x ), newFoolVec))


def getVectorOfEmotion( emotionID):
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT * FROM Twitter WHERE ID = ?", (emotionID,))
        vector=cursor.fetchone()
        return (vector[1:len(vector)])

def prettyFloat(num):
    return "%0.4f" % num


def buildVectorFromCSV(row):
    emotionlistfromcsvbyID = [246, 183, 295, 17, 329 , 299 , 114]
    listOfTuplesPerFrame = list()
    arr = init.readTableFromCSV()
    for i in range(1,8):
        scalar = arr[i][row]
        pair = (scalar,emotionIDToName(emotionlistfromcsvbyID[i]))
        row+=1
        listOfTuplesPerFrame.append(pair)

    return listOfTuplesPerFrame


def findMainEmotion(videoFrameArray):
    #print("going to find the main emotion in video")
    ListOfEmotions= ["neutral", "happiness","sadness","anger","surprise","scare","disgust"]
    SumOfEachEmotion= map(sum, zip(*videoFrameArray))
    emotionsWithoutNeutral=SumOfEachEmotion[1:]
    #print ListOfEmotions
    return ListOfEmotions[emotionsWithoutNeutral.index(max(emotionsWithoutNeutral))+1]


def getMixedVec(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):
    list = [(NeutralScalar,"neutral"), (HappyScalar,"happiness"),(SadScalar,"sadness"),(AngryScalar,"anger"),
            (SurprisedScalar,"surprise"),(ScaredScalar,"scare"),(DisgustedScalar,"disgust")]
    listWithVecs = listOfTheVecs
    listOfScalars = map(lambda x: x[0], list)
    listOfNewVEcs = map(lambda scalar, vec: map(lambda x: scalar * x, vec), listOfScalars, listWithVecs)
    #print (listOfNewVEcs)
    mixedVEc = map(sum, zip(*listOfNewVEcs))
    return mixedVEc

def euclidean_distance(first_vec,second_vec):
    if (len(first_vec) != len(second_vec)):
        print("!!ERROR!! vector lengths are not equal, vec_1 len %d , vec_2 len %d"%(len(first_vec),len((second_vec))))
        return -1
    dst = distance.euclidean(first_vec, second_vec)

    return dst


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


#def dkl (vec1, vec2):
#    vec1 = np.asarray(vec1, dtype=np.float)
#    vec2 = np.asarray(vec2, dtype=np.float)
#    return np.sum(np.where(vec1 != 0, vec1 * np.log(vec1 / vec2), 0))

def number_of_videos_in_raw_data():
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT * FROM Video_Data_Raw WHERE Frame_number = 1 ")
        id =cursor.fetchall()
        from operator import itemgetter
        id = max(id, key=itemgetter(0))  # faster solution
        return id[0]

def number_of_frames_in_a_video(video_number):
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT * FROM Video_Data_Raw WHERE VideoID = (?) ", (video_number, ))
        id =cursor.fetchall()
        from operator import itemgetter
        id = max(id, key=itemgetter(1))  # faster solution
        return id[1]

def calculate_dkl(vec1,vec2):
    if (sum(vec1) != 1.0):
        vec1 = normalize_vec(vec1)
    if (sum(vec2) != 1.0):
        vec2 = normalize_vec(vec2)
    sum_dkl=0
    for i in range(0,len(vec2)):
        sum_dkl+=vec2[i]*math.log(float(vec2[i])/float(vec1[i]))

    return sum_dkl



def normalize_vec(vec):
    norma = np.linalg.norm(vec)
    return map(lambda x: (x/(norma)), vec)

def analyze_emotion_to_emotion():
    print ("this function will stimulate the flow from emotion to other")


