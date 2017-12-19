import numpy as np
import methods
#def getMixedVec1(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):

def main():
    ListOfEmotions = ["neutral", "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    print listOfGeneralVecs

def get_orthoNormal():
    Neutral = methods.getMixedVec(1,0,0,0,0,0,0)
    Happy = methods.getMixedVec(0,1,0,0,0,0,0)
    print Happy
def gram_schmidt(vectors):
    basis = []
    w = list()
    for v in vectors:
        #print v
        w = v - np.sum(np.dot(v, b)*b for b in basis )
        if (w > 1e-10).any():
            basis.append(w/np.linalg.norm(w))
    return np.array(basis)
