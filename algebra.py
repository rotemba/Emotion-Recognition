import numpy as np
import methods
import init
import matplotlib.pyplot as plt
import csv
#def getMixedVec1(NeutralScalar,HappyScalar,SadScalar,AngryScalar,SurprisedScalar,ScaredScalar,DisgustedScalar, listOfTheVecs):

pathOfTwitter = "files/Twitter_only_vecs.csv"
human_space = "files/human_space_algebra.csv"
sentiment_file = "files/NRC_emotion_setiment.csv"
LABEL_COLOR_MAP = {0: 'r',
                   1: 'k',
                   2: 'b',
                   3: 'g',
                   4: 'c',
                   5: 'm',
                   6: 'y'
}

def main():

    #emotion = raw_input("put emotion name please to replace with neutral")
    emotion = "neutral"

    if (init.working_with_twiter_space == 1):
        path_to_only_vecs = pathOfTwitter
    else:
        path_to_only_vecs = human_space

    emotion_vectors = np.genfromtxt(path_to_only_vecs, dtype=float, delimiter=',')
    ListOfEmotions = [emotion, "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    vectors = np.array(listOfGeneralVecs)
    print emotion_vectors.shape
    print "check"
    print vectors.shape[1]
    if (vectors.shape[1]  != init.dimensions_of_vector):
        print ("!!rerun the program after deleting the DB")
        exit()

    U, singularValues, V = svd_routine(emotion_vectors)
    print_statistics(U, singularValues, V,emotion_vectors)
    finding_nearest_emotion(V)
    basis = V[:7]
    basis = gram_schmidt(basis)
    #dict_after_pertubation = pertubation(twitDict,ListOfEmotions)
    which_emotions_are_close(emotion_vectors,basis)
    get_clustering(emotion_vectors,basis)

    basis = V[:7]
    high_dimnesion_clustring(emotion_vectors,basis)



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
        if (w - v > 1e-10).any():
            print "change in basis"
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
    U, singularValues, V = svd(movieRatings)
    return [U, singularValues, V]

def pertubation(twitterdict,ListOfEmotions):
    twitterdict = np.array(twitterdict)
    for v in ListOfEmotions:
        print v
        pre = twitterdict[methods.emotionNameToEmotionID(v)-1]
        x = methods.normalize_vec_l2(np.random.normal(0,1,50),0.9)
        twitterdict[methods.emotionNameToEmotionID(v)-1] = methods.normalize_vec_l2(pre + x)
        print methods.getClosestVectorNamesCosine(methods.normalize_vec_l2(pre + x))
    return twitterdict

def finding_nearest_emotion(V):
    i=0
    for v in V:
        dist = methods.getSortedListDistanceEmotionName(v)
        desc = '\n'
        for j in range(0,6):
            emo = dist[j]
            desc = desc + str(j)+ ".\t" + methods.emotionIDToName(emo[1]) + " " + "{:.4f}".format(emo[0]) +"\n"
        print "meta emotion V[%0d]: these are the closest emotions to it: %0s"%(i,desc)
        i = i + 1


def print_statistics(U, singularValues, V,twitDict):
    print ("U matrix")
    print (U)
    print ("singular")
    sum_singular = sum(singularValues)
    print sum_singular
    for i in range(0, len(singularValues)):
       print ("%d : %0.4f   %0.4f" % (i, singularValues[i], sum(singularValues[:i + 1]) / sum_singular))

    print ("V matrix")
    print V

    plt.scatter(list(range(1, len(singularValues) + 1)), singularValues)
    plt.show()
    print(len(V))


def create_histogram_from_space(space, basis):
    list_of_distance_from_space = list()
    count = 0
    for i in range(1,len(space)):
        v = space[i-1]
        print methods.emotionIDToName(i)
        z = v - np.sum(np.dot(v, b) * b for b in basis)
        if (np.linalg.norm(z) > 1e-10):
            list_of_distance_from_space.append( (np.linalg.norm(z) ))
        else:
            list_of_distance_from_space.append( 0 )
            count += 1

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
    for i in range(1, len(space)+1):
        v = space[i-1]
        z = v - np.sum(np.dot(v, b) * b for b in basis)
        if (np.linalg.norm(z) > 1e-10):
            list_of_distance_from_space.append((np.linalg.norm(z), methods.emotionIDToName(i)))
        else:
            list_of_distance_from_space.append((0, methods.emotionIDToName(i)))
            count += 1

    from operator import itemgetter
    sorted_distance_list = sorted(list_of_distance_from_space, key=itemgetter(0))
    for i in range(0,int(len(sorted_distance_list)*0.3)):
        print "[%0d] emotion %s distance to space is %0.6f" %(i,sorted_distance_list[i][1],sorted_distance_list[i][0])
        #print methods.getVectorOfEmotion(methods.emotionNameToEmotionID(sorted_distance_list[i][1]))#to verify
    dist_list = [ item[0] for item in list_of_distance_from_space]
    print_histogram(dist_list)


def get_clustering(space, basis):
    x = list()
    y = []
    name = []
    count = 0
    for i in range(1, len(space)+1):
        v = space[i-1]
        # print methods.emotionIDToName(i)
        x.append(np.sum(np.dot(v, basis[0])))
        y.append( np.sum(np.dot(v, basis[1])) )
        name.append(methods.emotionIDToName(i))

    data = np.array(list(zip(x, y)))
    col = generate_clutering(data)
    col = [LABEL_COLOR_MAP[l] for l in col]

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.scatter(x, y,color = col , s=50, linewidth=1)


    for i in range(0, len(space)):
        ax.annotate(name[i], (x[i], y[i]))


    plt.show()


def generate_clutering(data, num_clustring = 2 ):
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=num_clustring).fit_predict(data)
    return kmeans

def sentiment_per_emotion():
    sentimet = csv.reader(sentiment_file)



def print_histogram(dist_list):
    plt.hist(dist_list, align= 'mid', bins= 20)
    plt.title('Histogram')
    plt.ylabel('Frequency')
    plt.xlabel('Distance')
    plt.show()

def high_dimnesion_clustring(space, basis):
    x0 = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    x6 = []
    name =list()
    for i in range(1, len(space) + 1):
        v = space[i - 1]
        # print methods.emotionIDToName(i)
        x0.append(np.sum(np.dot(v, basis[0])))
        x1.append(np.sum(np.dot(v, basis[1])))
        x2.append(np.sum(np.dot(v, basis[2])))
        x3.append(np.sum(np.dot(v, basis[3])))
        x4.append(np.sum(np.dot(v, basis[4])))
        x5.append(np.sum(np.dot(v, basis[5])))
        x6.append(np.sum(np.dot(v, basis[6])))
        name.append(methods.emotionIDToName(i))
    num_of_clusters = 2
    data = np.array(list(zip(x0, x1 , x2 , x3, x4 , x5 , x6)))
    col = generate_clutering(data,num_of_clusters)
    c = [[] for x in xrange(num_of_clusters)]
    vector_cluster = [[] for x in xrange(num_of_clusters)]
    for i in range(0,len(space)):
        c[col[i]].append(methods.emotionIDToName(i+1))
        vector_cluster[col[i]].append(data[i])

    for item in c:
        print "number of emotion in cluster = %0d, emotions %s"%(len(item),item)


if __name__ == '__main__':
    main()

