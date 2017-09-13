#TODO: SABO: add the next line to your file so it'll know this file.
#from init import initRelationTable
from numpy import genfromtxt
import sqlite3
import os

def initRelationTable():
    DBName= "emotions.db"
    pathOfEmotionRealations = "files/emotionsAngelsToDB.csv"
    print("going to create the DB function")
    databaseexisted = os.path.isfile('emotions.db')
    if not databaseexisted:
        print("going to create the DB")
        dbcon = sqlite3.connect("emotions.db")
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""CREATE TABLE Relations(X INTEGER NOT NULL,
                                                      Y INTEGER NOT NULL,
                                                     Value REAL NOT NULL)""")
            print ("creating cartesian emotions table")
            relationArray = genfromtxt(pathOfEmotionRealations, delimiter=',')
            rows = len(relationArray)
            cols = len(relationArray)
            print relationArray
            for row in range(0, rows):
                for col in range(0, cols):
                    cursor.execute("INSERT  INTO Relations VALUES (?,?,?)", (row, col, relationArray[row][col]))
                    #print ("added value (%f) to the DB" % relationArray[row][col])
            dbcon.commit()



            print ("end of the prog")
            #basic_actions_on_db( cursor)
    print ("DB EXIST")
    return dbcon






def angels_between_two_emotions (emotion1, emotion2):
    print ("angel between two emotions function")
    #SELECT * FROM Relations WHERE X = 181  ORDER BY VALUE  DESC
    #SELECT VALUE FROM Relations WHERE X = 180 AND Y = 40