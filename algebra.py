import numpy as np
import methods
#def getMixedVec1(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):

def main():
    #emotion = raw_input("put emotion name please to replace with neutral")
    emotion = "neutral"
    pathOfTwitter = "files/Twitter_only_vecs.csv"
    #twitDict = np.genfromtxt(pathOfTwitter, delimiter=',', dtype=None)
    twitDict = np.genfromtxt(pathOfTwitter, dtype=float, delimiter=',')
    ListOfEmotions = [emotion, "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    vectors = np.array(listOfGeneralVecs)
    basis = gram_schmidt( vectors)
    list_of_distance_from_space = list()
    count =0
    for v in twitDict:
        v = v - np.sum(np.dot(v, b)*b for b in basis )
        if (np.linalg.norm(v) > 1e-10):
            list_of_distance_from_space.append(np.linalg.norm(v))
        else:
            list_of_distance_from_space.append(0)
            count+=1

    print count
    print max(list_of_distance_from_space)
    print np.mean(list_of_distance_from_space)
    print np.std(list_of_distance_from_space)
    import matplotlib.pyplot as plt
    plt.hist(list_of_distance_from_space, bins=20)
    plt.title('Histogram, bins size is: 0.05')
    plt.ylabel('Frequency')
    plt.xlabel('Distance')
    plt.show()


def get_orthoNormal():
    Happy = (0,2,0,2,0,0,0)
    print np.linalg.norm(Happy)
    print Happy
def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        #print v
        w = v - np.sum(np.dot(v, b)*b for b in basis )
        if (w > 1e-10).any():
            basis.append(w/np.linalg.norm(w))
    return np.array(basis)
