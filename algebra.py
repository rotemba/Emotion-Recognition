import numpy as np
import methods
#def getMixedVec1(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):

def main():

    #emotion = raw_input("put emotion name please to replace with neutral")
    emotion = "neutral"
    pathOfTwitter = "files/Twitter_only_vecs.csv"
    #twitDict = np.genfromtxt(pathOfTwitter, delimiter=',', dtype=None)
    twitDict = np.genfromtxt(pathOfTwitter, dtype=float, delimiter=',')
    svd_routine(twitDict)
    ListOfEmotions = [emotion, "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    vectors = np.array(listOfGeneralVecs)
    # FIXME read from same file as init, than we would not do this -1 here
    # before_per = twitDict[methods.emotionNameToEmotionID("neutral") - 1]
    #print listOfGeneralVecs[1],methods.printClosestVectorByCosSimilarity(listOfGeneralVecs[1])
    basis = gram_schmidt(vectors)
    #twitDict = pertubation(twitDict,ListOfEmotions)
    print("showing the diff")
    print (listOfGeneralVecs[1] - twitDict[methods.emotionNameToEmotionID("neutral")-1])
    list_of_distance_from_space = list()
    count =0
    for v in twitDict:
        z = v - np.sum(np.dot(v, b)*b for b in basis )
        if (np.linalg.norm(z) > 1e-10):
            list_of_distance_from_space.append(np.linalg.norm(z))
        else:
            list_of_distance_from_space.append(0)
            count += 1
            print methods.printClosestVectorByCosSimilarity(v)

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


def svd_routine(twitDict):
    from numpy.linalg import svd
    import matplotlib.pyplot as plt
    movieRatings = [
        [2, 5, 3],
        [1, 2, 1],
        [4, 1, 1],
        [3, 5, 2],
        [5, 3, 1],
        [4, 5, 5],
        [2, 4, 2],
        [2, 2, 5],
    ]
    print(type(movieRatings))
    U, singularValues, V = svd(twitDict)
    print(len(singularValues))
    print()
    print(singularValues)
    plt.scatter(list(range(1, len(singularValues)+1 )),singularValues)
    plt.show()
    print(len(V))

    Sigma = np.vstack([
        np.diag(singularValues),
        np.zeros((373-50, 50)),
    ])

    print(len(U[1]))
    # print(np.dot(Sigma, V))
    # print(twitDict - np.round(np.dot(U, np.dot(Sigma, V)), decimals=10))
    exit()

def pertubation(twitterdict,ListOfEmotions):
    twitterdict = np.array(twitterdict)
    for v in ListOfEmotions:
        print v
        pre = twitterdict[methods.emotionNameToEmotionID(v)-1]
        x = methods.normalize_vec(np.random.normal(0,1,50),7.9)
        twitterdict[methods.emotionNameToEmotionID(v)-1] = methods.normalize_vec(pre + x)
        print methods.printClosestVectorByCosSimilarity(methods.normalize_vec(pre + x))
    return twitterdict

if __name__ == '__main__':
    main()

