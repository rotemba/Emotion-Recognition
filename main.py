import sqlite3
import os

from numpy import genfromtxt
import sqlite3
import os
import csv



path = os.getcwd()


def initTwitterDB(s):
    databaseexisted = os.path.isfile('Emotions.db')
    dbcon = sqlite3.connect("Emotions.db")
    if not databaseexisted:
        str = ("ID INTEGER NOT NULL REFERENCES  EmotionsID(ID), %s" % ','.join("X%d REAL" % i for i in range(50)))

        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("CREATE TABLE EmotionsID(ID INTEGER PRIMARY KEY NOT NULL ,Emotion_name TEXT NOT NULL )")
            cursor.execute("CREATE TABLE Twitter (%s)" % str )
            cursor.execute("""CREATE TABLE Relations(X INTEGER NOT NULL,
                                                               Y INTEGER NOT NULL,
                                                              Value REAL NOT NULL)""")
            print ("creating cartesian emotions table")



            print("DONE creating the DB")
            pathOfTwitter = "files/twitter_dict.csv"
            pathOfEmotionRealations = "files/emotions_angels.csv"

            fileObject = csv.reader(pathOfTwitter)

            relationArray = genfromtxt(pathOfEmotionRealations, delimiter=',')
            twitDict = genfromtxt(pathOfTwitter, delimiter=',', dtype=None)
            row_count = 374
            print ("Inserting data to table")

            str = '?'
            for x in range(0, 50):
                str = str + ',?'

            for row in range(1, row_count):
                cursor.execute('''INSERT INTO Twitter VALUES (%s)''' % str,(row, twitDict[row][1],twitDict[row][2],twitDict[row][3],twitDict[row][4],twitDict[row][5],twitDict[row][6],twitDict[row][7],twitDict[row][8],twitDict[row][9],twitDict[row][10],
                                      twitDict[row][11],twitDict[row][12],twitDict[row][13],twitDict[row][14],twitDict[row][15],twitDict[row][16],twitDict[row][17],twitDict[row][18],twitDict[row][19],twitDict[row][20],
                                      twitDict[row][21],twitDict[row][22],twitDict[row][23],twitDict[row][24],twitDict[row][25],twitDict[row][26],twitDict[row][27],twitDict[row][28],twitDict[row][29],twitDict[row][30],
                                      twitDict[row][31],twitDict[row][32],twitDict[row][33],twitDict[row][34],twitDict[row][35],twitDict[row][36],twitDict[row][37],twitDict[row][38],twitDict[row][39],twitDict[row][40],
                                      twitDict[row][41],twitDict[row][42],twitDict[row][43],twitDict[row][44],twitDict[row][45],twitDict[row][46],twitDict[row][47],twitDict[row][48],twitDict[row][49],twitDict[row][50]))
            print ("Twitter vectors are inside the DB")
            for row in range(1, row_count):
                cursor.execute('''INSERT INTO EmotionsID(ID, Emotion_name) VALUES (?,?)''' ,(row,twitDict[row][0]))
            dbcon.commit()
            print ("Twitter emotions names are inside the DB")


            #print relationArray[1][0]

            for row in range(1, row_count):
                for col in range(1, row_count):
                    cursor.execute('''INSERT INTO Relations VALUES (?,?,?)''', (row, col, relationArray[row][col]))
                    #print ("added value (%r) to the DB at index %d,%d" % (relationArray[row][col], row, col))

            dbcon.commit()
    return dbcon

def angels_between_two_emotions (dbcon,emotion1 = 'None', emotion2 = 'None'):
    print ("angel between two emotions function")
    cursor = dbcon.cursor()
    cursor.execute("SELECT ID FROM EmotionsID WHERE Emotion_name= 'thoughtfulness' ")
    id = cursor.fetchone()

    print(first(id))
    #SELECT ID FROM EmotionID WHERE Emotion_name = thoughtfulness  ORDER BY VALUE  DESC
    #SELECT VALUE FROM Relations WHERE X = 180 AND Y = 40

def main(s):
    print(2)
    dbcon = initTwitterDB(s)
    angels_between_two_emotions(dbcon)




if __name__ == '__main__':
    print(1)
    twiter_path = "files/twitter_dict.csv"
    main(twiter_path)



