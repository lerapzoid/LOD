import MySQLdb
import csv
import re
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS API")
#cursor.execute("DROP TABLE IF EXISTS MASHUP")
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\APIV2.csv')as csv_fileR:
#with open('E:\\Fac\\Informatique\\Python\\txtFiles\\Mashup.csv')as csv_fileR:
    reader=csv.reader(csv_fileR)
    firstRow=True
    fieldnames=""
    rownum=0
    #Pour chaque ligne du csv on insere une nouvelle entrée de base de donnée
    for row in reader:
        rownum=rownum+1
        firstElement=True
        #On récupére les champs à partir de la premiére ligne du csv
        if(firstRow):
            try:
                request='SELECT * FROM API'
                #request='SELECT * FROM MASHUP'
                cursor.execute(request)
            except:
                print "La table n'existe pas"
                request="CREATE TABLE API (ID INT AUTO_INCREMENT NOT NULL"
                #request="CREATE TABLE MASHUP (ID INT AUTO_INCREMENT NOT NULL"
                for attribut in row:
                    attribut=re.sub(" /","",attribut)
                    attribut=re.sub("-","_",attribut)
                    attribut=re.sub("/","_",attribut)
                    attribut=re.sub(" \?","",attribut)
                    attribut=re.sub("\?","",attribut)
                    attribut=re.sub("\'","_",attribut)
                    attribut=re.sub(" \(.*?\)","",attribut)
                    attribut=re.sub(" ","_",attribut)
                    if(attribut=="API_Description" or attribut=="Mashup_Description"or attribut=="Related_API_"or attribut=="How_is_this_API_different" or attribut=="Secondary_Categories"or attribut=="API_Portal_Home_Page"or attribut=="Docs_Home_Page_URL"):
                        request=request+","+attribut+" LONGTEXT"
                    else:
                        request=request+","+attribut+" CHAR(255)"
                request=request+",PRIMARY KEY (ID));"
                cursor.execute(request)
                db.commit()
            for attribut in row:
                attribut=re.sub(" /","",attribut)
                attribut=re.sub("-","_",attribut)
                attribut=re.sub("/","_",attribut)
                attribut=re.sub(" \?","",attribut)
                attribut=re.sub("\?","",attribut)
                attribut=re.sub("\'","_",attribut)
                attribut=re.sub(" \(.*?\)","",attribut)
                attribut=re.sub(" ","_",attribut)
                if fieldnames=="":
                    fieldnames=attribut
                else:
                    fieldnames=fieldnames+","+attribut
            firstRow=False
        #On crée la requete d'insertion dans la base de donnée
        else:
            if rownum<-1:
                rownum=rownum
            else:
                request='INSERT INTO API('+fieldnames+') VALUES('
                #request='INSERT INTO MASHUP('+fieldnames+') VALUES('
                for attribut in row:
                    if(firstElement):
                        firstElement=False
                        attribut=re.sub("\'"," ",attribut)
                        request=request+"\'"+attribut+"\'"
                    else:
                        attribut=re.sub("\'"," ",attribut)
                        request=request+",\'"+attribut+"\'"
                request=request+");"
                cursor.execute(request)
                db.commit()
        print rownum