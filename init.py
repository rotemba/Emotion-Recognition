#TODO: SABO: add the next line to your file so it'll know this file.
#from init import initRelationTable
from numpy import genfromtxt
import sqlite3
import os

def initRelationTable(dbcon):
    DBName= "emotions.db"
    pathOfEmotionRealations = "files/emotions_angels.xlsx"
    #print("going to create the DB function")
    databaseexisted = os.path.isfile('Emotions.db')
    if not databaseexisted:
        print ('DB doesnt exist')
    else:
        print("going to create the DB")
        #dbcon = sqlite3.connect("Emotions.db")
        with dbcon:
            cursor1 = dbcon.cursor()
            cursor1.execute("""CREATE TABLE Relations(X INTEGER NOT NULL,
                                                      Y INTEGER NOT NULL,
                                                     Value REAL NOT NULL)""")
            print ("creating cartesian emotions table")
            relationArray = genfromtxt(pathOfEmotionRealations, delimiter=',',dtype=None)
            rows = len(relationArray)
            cols = len(relationArray)
            #print relationArray
            print cols
            for row in range(1, rows):
                for col in range(1, cols):
                    cursor1.execute('''INSERT INTO Relations VALUES (?,?,?)''', (row, col, relationArray[row][col]))
                    print ("added value (%f) to the DB at index %d,%d" % (relationArray[row][col], row, col))
            dbcon.commit()



            print ("end of the prog")
            #basic_actions_on_db( cursor)
    print ("DB EXIST")







def angels_between_two_emotions (emotion1, emotion2):
    print ("angel between two emotions function")
    SELECT * FROM Relations WHERE X = 181  ORDER BY VALUE  DESC
    #SELECT VALUE FROM Relations WHERE X = 180 AND Y = 40