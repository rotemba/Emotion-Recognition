#TODO: SABE: add the next line to your file so it'll know this file.
#from init import initRelationTable 
from numpy import genfromtxt
import sqlite3
import os

def initRelationTable():
    DBName= "emotions.db"
    pathOfEmotionRealations = "files/emotionsAngelsToDB.csv"
    print("going to create the DB function")
    databaseexisted = os.path.isfile('emotionsss.db')
    if not databaseexisted:
        print("going to create the DB")
        dbcon = sqlite3.connect("emotionsss.db")
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
                    print ("added value (%d) to the DB", relationArray[row][col])
            print ("end of the prog")

    print ("DB EXIST")
