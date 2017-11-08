import init
import math






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
    mone=sum((a*b) for a, b in zip(vec1, vec2))
    sizeOfVecs=(sizeOfVec1*sizeOfVec2)
    ans=mone/sizeOfVecs
    #print ans
    return ans


def printClosestVectorNames( vec):
    templist=[]
    for i in range (1,373):
        newangle= angleBetweenTwoVecs(vec,getVectorOfEmotion(i))
        #print ("angle between %0d, %0d: %0.4f" % (7, i, newangle))
        templist.append((newangle,i))

    from operator import itemgetter

    result = max(templist, key=itemgetter(0))  # faster solution
    result1 = (result[0], str(emotionIDToName(result[1])))
    return result1




def emotionIDToName( emotionID):
    with init.dbcon:
        cursor=init.dbcon.cursor()
        cursor.execute("SELECT Emotion_name FROM EmotionsID WHERE ID = ?", (emotionID,))
        name=cursor.fetchone()
        #print("got id number:" + str(emotionID) +" - name: "+ name[0])
        return (name[0])

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
        pair = (scalar,methods.emotionIDToName(emotionlistfromcsvbyID[i]))
        row+=1
        listOfTuplesPerFrame.append(pair)

    return listOfTuplesPerFrame