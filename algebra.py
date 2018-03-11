import numpy as np
import methods
import matplotlib.pyplot as plt
#def getMixedVec1(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):

def main():

    #emotion = raw_input("put emotion name please to replace with neutral")
    emotion = "neutral"
    pathOfTwitter = "files/Twitter_only_vecs.csv"
    #twitDict = np.genfromtxt(pathOfTwitter, delimiter=',', dtype=None)
    twitDict = np.genfromtxt(pathOfTwitter, dtype=float, delimiter=',')
    ListOfEmotions = [emotion, "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    #vectors = np.array(listOfGeneralVecs)
    print twitDict.shape
    U, singularValues, V = svd_routine(twitDict)
    print U.shape
    print V.shape
    print_statistics(U, singularValues, V,twitDict)
    finding_nearest_emotion(V)
    basis = gram_schmidt(V[0:7])
    #basis = gram_schmidt(vectors)
    #dict_after_pertubation = pertubation(twitDict,ListOfEmotions)
    #which_emotions_are_close(twitDict,basis)



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

    # movieRatings = [
    #     [2, 5, 3],
    #     [1, 2, 1],
    #     [4, 1, 1],
    #     [3, 5, 2],
    #     [5, 3, 1],
    #     [4, 5, 5],
    #     [2, 4, 2],
    #     [2, 2, 5],
    # ]
    movieRatings = twitDict
    print movieRatings
    U, singularValues, V = svd(movieRatings)
    print U.shape
    return [U, singularValues, V]

def pertubation(twitterdict,ListOfEmotions):
    twitterdict = np.array(twitterdict)
    for v in ListOfEmotions:
        print v
        pre = twitterdict[methods.emotionNameToEmotionID(v)-1]
        x = methods.normalize_vec(np.random.normal(0,1,50),0.9)
        twitterdict[methods.emotionNameToEmotionID(v)-1] = methods.normalize_vec(pre + x)
        print methods.printClosestVectorByCosSimilarity(methods.normalize_vec(pre + x))
    return twitterdict

def finding_nearest_emotion(V):
    i=0
    for v in V:
        emo = (methods.find_shortest_dist(v,1))
        print "emotion : %s is closest to V[%0d] distance %0.6f"%(methods.emotionIDToName(emo[1]),i, emo[0])
        i = i + 1


def print_statistics(U, singularValues, V,twitDict):
    print ("U matrix")
    print (U)
    print ("singular")
    sum_singular = sum(singularValues)
    #print sum_singular
    #for i in range(0, len(singularValues)):
    #    print ("%d : %0.4f   %0.4f" % (i, singularValues[i], sum(singularValues[:i + 1]) / sum_singular))

    print ("V matrix")
    print V

    #plt.scatter(list(range(1, len(singularValues) + 1)), singularValues)
    #plt.show()
    #print(len(V))


def print_histogram(space, basis):
    list_of_distance_from_space = list()
    count = 0
    for i in range(1,len( space)):
        v = space[i]
        print methods.emotionIDToName(i)
        z = v - np.sum(np.dot(v, b) * b for b in basis)
        if (np.linalg.norm(z) > 1e-10):
            list_of_distance_from_space.append( (np.linalg.norm(z) ))
        else:
            list_of_distance_from_space.append( 0 )
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

def which_emotions_are_close(space,basis):
    list_of_distance_from_space = list()
    count = 0
    for i in range(1, len(space)):
        v = space[i]
        print methods.emotionIDToName(i)
        z = v - np.sum(np.dot(v, b) * b for b in basis)
        if (np.linalg.norm(z) > 1e-10):
            list_of_distance_from_space.append((np.linalg.norm(z), methods.emotionIDToName(i)))
        else:
            list_of_distance_from_space.append((0, methods.emotionIDToName(i)))
            count += 1
            print methods.printClosestVectorByCosSimilarity(v)

    from operator import itemgetter
    sorted_distance_list = sorted(list_of_distance_from_space, key=itemgetter(0))
    for i in range(0,int(len(sorted_distance_list)*0.3)):
        print "[%0d] emotion %s distance to space is %0.6f" %(i,sorted_distance_list[i][1],sorted_distance_list[i][0])


if __name__ == '__main__':
    main()

