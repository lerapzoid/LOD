import MySQLdb
import random
import re
import time
def evolution():
    c=1
    #On recupére les relations de substitution
    request="select IDService1,IDService2,poids from RELATION Where SUBSTR(dateObservation,7,4)>\'2013\' AND typeRelation='Substitution'"
    cursor.execute(request)
    list=cursor.fetchall()
    print len(list)
    for row in list:
        print c
        APIID1=row[0]
        APIID2=row[1]
        poids=row[2]
        dateObs="01.01.2017"
        #On génére un poids aleatoire
        w = random.random()
        #Insertion de la nouvelle relation
        request='INSERT INTO RELATION(IDService1,IDService2,dateObservation,typeRelation,poids) VALUES(\''+str(APIID1)+'\',\''+str(APIID2)+'\',\''+str(dateObs)+'\',\'Substitution\',\''+str(w)+'\')'
        cursor.execute(request)
        if w<poids:
            #Si le poids est inférieur au seuil on ajoute à la table evolution les services ainsi que la date de l'observation et la différences de poids constater
            if(poids-w>0.3):
                request='INSERT INTO EVOLUTION(IDService1,IDService2,dateObservation,differencePoids,token) VALUES(\''+str(APIID1)+'\',\''+str(APIID2)+'\',\''+str(dateObs)+'\',\''+str(poids-w)+'\',\'0\');'
                cursor.execute(request)
        else:
            if(w-poids>0.3):
                request='INSERT INTO EVOLUTION(IDService1,IDService2,dateObservation,differencePoids,token) VALUES(\''+str(APIID1)+'\',\''+str(APIID2)+'\',\''+str(dateObs)+'\',\''+str(w-poids)+'\',\'1\');'
                cursor.execute(request)
        c=c+1
    db.commit()
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
evolution()