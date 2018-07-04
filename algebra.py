import numpy as np
import methods
import init
import matplotlib.pyplot as plt
import csv

ListOfEmotions = ["neutral", "happiness", "sadness", "anger", "surprise", "scare", "disgust"]
sentiment_file = "files/NRC_emotion_setiment.csv"
LABEL_COLOR_MAP = {0: 'r',
                   1: 'k',
                   2: 'b',
                   3: 'g',
                   4: 'c',
                   5: 'm',
                   6: 'y'
}
LABEL_COLOR_SENTIMENT = {
    (u'Positive',): 'g',
    (u'Negative',): 'r',
    (u'Unknown',):  'b',
    (u'Neutral',):  'k'
}

def main():

    init.get_paths()
    print init.path_to_only_vecs
    emotion_vectors = np.genfromtxt(init.path_to_only_vecs, dtype=float, delimiter=',')

    listOfGeneralVecs= map(lambda x: methods.getVectorOfEmotion(methods.emotionNameToEmotionID(x)), ListOfEmotions)
    vectors = np.array(listOfGeneralVecs)
    #orthonormal_vectors = gram_schmidt(vectors)
    print emotion_vectors.shape
    print "%s"%str(emotion_vectors[-1])
    print "%s"%methods.emotionIDToName(len(emotion_vectors))
    print "check"
    print vectors.shape[1]
    if (vectors.shape[1]  != init.dimensions_of_vector):
        print ("!!rerun the program after deleting the DB")
        exit()
    create_similarity_matrix(emotion_vectors)
    #U, singularValues, V = svd_routine(emotion_vectors)
    #print_statistics(U, singularValues, V,emotion_vectors)
    #finding_nearest_emotion(V)
    #basis = V[:7]
    #basis = gram_schmidt(basis)
    #dict_after_pertubation = pertubation(twitDict,ListOfEmotions)
    #which_emotions_are_close(emotion_vectors,basis)
    #get_clustering_no_sentiment(emotion_vectors,basis)
    #get_clustering(emotion_vectors,basis)

    #basis = V[:7]

    #meta_emotion_combination(emotion_vectors, orthonormal_vectors)
    # high_dimnesion_clustring(emotion_vectors,basis)



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
       print ("%d : %0.4f   %0.4f" % (i, singularValues[i]/sum_singular*100, sum(singularValues[:i + 1]) / sum_singular*100))

    # print ("V matrix")
    # print V

    plt.scatter(list(range(1, len(singularValues) + 1)), singularValues)
    plt.show()


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
    for j in range(1,2):
        for i in range(1, len(space)+1):
            v = space[i-1]
            # print methods.emotionIDToName(i)
            x.append(np.sum(np.dot(v, basis[0])))
            y.append( np.sum(np.dot(v, basis[1])) )
            #print i
            #print methods.emotionIDToName(i)
            name.append(methods.emotionIDToName(i))

        col = generate_clutering_from_sentiment(name)
        col = [(LABEL_COLOR_SENTIMENT[l]) for l in col]
        data = zip(x,y,col,name)
        #print data
        data = [x for x in data if x[2]!= 'b']
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        meanx = np.mean(np.array(x))
        meany = np.mean(np.array(y))
        # x = map(lambda z: z-meanx,x)
        # y = map(lambda z: z-meany,y)
        col = [i[2] for i in data]
        name = [i[3] for i in data]
        data_to_split = zip(x, y, col, name)
        print "shown data is %s"%data

        pos = [l for l in data_to_split if l[2] == 'g']
        neg = [l for l in data_to_split if l[2] == 'r']
        unknown = [l for l in data_to_split if l[2] == 'k']

        fig, ax = plt.subplots()

        #


        #
        # Plot something
        x = [l[0] for l in pos]
        y = [l[1] for l in pos]

        p1 = plt.scatter(x, y, color='g')
        x = [l[0] for l in neg]
        y = [l[1] for l in neg]
        p2 = plt.scatter(x, y, color='r')

        x = [l[0] for l in unknown]
        y = [l[1] for l in unknown]
        p3 = plt.scatter(x, y, color='k')

        # Create legend from custom artist/label lists

        plt.legend((p1,p2,p3),
                   ('Positive', 'Negative', 'Neutral'),
                   scatterpoints=1,
                   #loc='lower left',
                   ncol=50,
                   fontsize=12)

        # import matplotlib.pyplot as plt
        # fig, ax = plt.subplots()
        # ax.legend(x, y ,color = col , s=50, linewidth=1, linewidths=5)

        plt.axvline(x=0)
        plt.axhline(y=0)

        #plt.legend((lo, ll, l, a, h, hh, ho),
           # ('Low Outlier', 'LoLo', 'Lo', 'Average', 'Hi', 'HiHi', 'High Outlier'),
           # scatterpoints=1,
           # loc='lower left',
           # ncol=3,
           # fontsize=8)
        z = []
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        s = [20  for n in range(len(x))]
        for i in range(0, len(x)):
            if (i % 10 == 0 and name[i]!='agreement' and name[i]!='blues' and name[i]!='unhappiness' and name[i]!='strength'):
                z.append(name[i])
                ax.annotate(name[i], (x[i], y[i]),size=16)

        # ax.set_xlim([min(x), max(x)])
        print "11111"
        print z
        print "11111"
        ax.grid(True)
        plt.show()


def generate_clutering(data, num_clustring = 2 ):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    for k in range(2,10):
        kmeans = KMeans(n_clusters=k).fit(data)
        label = kmeans.labels_
        sil_coeff = silhouette_score(data, label, metric='euclidean')
        print("For n_clusters={}, The Silhouette Coefficient is {}".format(k, sil_coeff))
    kmeans = KMeans(n_clusters=num_clustring).fit_predict(data)
    return kmeans

def generate_clutering_from_sentiment(names):
    label = []
    with init.dbcon:
        cursor = init.dbcon.cursor()
        for ii in range(0,init.num_of_vectors-1):
            if (names[ii]=="worry"): break
            #print names[ii]
            cursor.execute("SELECT Sentiment FROM EmotionsSentiment WHERE Emotion_name = (?)",  (names[ii],))
            sentiment = cursor.fetchall()
            if (len(sentiment) == 0):
                continue
            #print sentiment
            label.append((sentiment[0]))

    data = zip (names,label)
    #print data
    return label

def sentiment_per_emotion(emotion_name):
    with init.dbcon:
        cursor = init.dbcon.cursor()
        cursor.execute("SELECT Sentiment FROM EmotionsSentiment WHERE Emotion_name = (?)", (emotion_name,))
        sentiment = cursor.fetchall()
    return sentiment

def print_histogram(dist_list):
    plt.hist(dist_list, align= 'mid', bins= 20 , range= (0,1))
    plt.title('Histogram Human Dissimilarity Space')
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
    #col = generate_clutering_from_sentiment(name)

    c = [[] for x in xrange(num_of_clusters)]
    vector_cluster = [[] for x in xrange(num_of_clusters)]
    for i in range(0,len(space)):
        c[col[i]].append(methods.emotionIDToName(i+1))
        vector_cluster[col[i]].append(data[i])

    for item in c:
        disterbution_of_emotion_for_cluster(item)
        #print "number of emotion in cluster = %0d, emotions %s"%(len(item),item)


def meta_emotion_combination(V,basis):
    x0 = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    x6 = []
    dist= []
    for v in V:
        # print methods.emotionIDToName(i)
        x0.append(np.sum(np.dot(v, basis[0])))
        x1.append(np.sum(np.dot(v, basis[1])))
        x2.append(np.sum(np.dot(v, basis[2])))
        x3.append(np.sum(np.dot(v, basis[3])))
        x4.append(np.sum(np.dot(v, basis[4])))
        x5.append(np.sum(np.dot(v, basis[5])))
        x6.append(np.sum(np.dot(v, basis[6])))
        dist.append(np.linalg.norm(v - np.sum(np.dot(v, b) * b for b in basis)))
    data = np.array(list(zip(x0, x1, x2, x3, x4, x5, x6)))
    i=0
    for item in data:
        print "emotion %s is combination of this values data: " %(methods.emotionIDToName(i+1))
        print ListOfEmotions
        print ["{0:0.5f}".format(a) for a in item]
        print "dist from space is %0.5f"%dist[i]
        i = i + 1
        print


def disterbution_of_emotion_for_cluster(cluster):
    label_per_cluster = []
    for emo in cluster:
        if (len(sentiment_per_emotion(emo)) == 0):
            continue
        labeled = str(sentiment_per_emotion(emo)[0][0])
        label_per_cluster.append( labeled )

    from collections import Counter
    print Counter(label_per_cluster)


def get_clustering_no_sentiment(space, basis):
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

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='r')


    for i in range(0, len(space)):
        if (name[i] in ['abhorrence', 'anxious', 'aversion', 'change', 'completion', 'coolness', 'deflation', 'disappointment', 'disinterest', 'dizziness', 'empathy', 'expectation', 'furious', 'grim', 'hope', 'indifference', 'joyfulness', 'mediocrity', 'neutral', 'perplexity', 'push', 'repulsion', 'satisfaction', 'skepticism', 'terror', 'tranquility']):
            ax.annotate(name[i], (x[i], y[i]),size =16)

    plt.axvline(x=0)
    plt.axhline(y=0)
    ax.grid(True)
    plt.show()


def create_similarity_matrix(space):
    list_of_rows = []
    print "len_space %0d"%len(space)
    exit()
    for i in range(1,len(space)+1):
        row_list =[]
        row_emotion = methods.getVectorOfEmotion(i)
        for j in range(1, len(space) + 1):
            print "(%d,%d)"%(i,j)
            checked_emotion = methods.getVectorOfEmotion(j)
            row_list.append(methods.angleBetweenTwoVecs(row_emotion, checked_emotion ))
        list_of_rows.append(row_list)

    print "done"
    import csv
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_rows)

    exit()



    download_dir = "exampleCsv.csv"  # where you want the file to be downloaded to

    csv = open(download_dir, "w")
    # "w" indicates that you're writing strings to the file

    firstrow = methods.emotionIDToName(1) + ','
    for i in range(2,len(space)+1):
        firstrow = firstrow +',' + methods.emotionIDToName(i)

    firstrow = firstrow + '\n'
    csv.write(firstrow)
    for i in range(1,len(space)+1):
        row_to_write = ''
        row_emotion = methods.getVectorOfEmotion(i)
        for j in range(1, len(space) + 1):
            checked_emotion = methods.getVectorOfEmotion(j)



    for key in dic.keys():
        name = key
        email = dic[key]
        row = name + "," + email + "\n"
        csv.write(row)

    # for i in range(len(space)):
    #     for j in range(len(space)):


if __name__ == '__main__':
    main()

