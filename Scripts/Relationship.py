import MySQLdb
import random
#On crée 100 relation entre API
for x in range(0,50):
    dayObs=0
    monthObs=0
    yearObs=0
    #On crée un poids aléatoire
    r=random.random()
    idRelation=2
    #On crée un type de relation aléatoire
    #idRelation=random.randint(1, 3)
    if idRelation==1:
        relation="Composition"
    elif idRelation==2:
        relation="Substitution"
    elif idRelation==3:
        relation="Interet"
    db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
    cursor = db.cursor()
    #On choisi deux API parmi les 500 premiére API de la base de donnée
    APIID1=random.randint(1,100)
    APIID2=random.randint(1,100)
    while APIID1==APIID2:
        APIID2=random.randint(0, 100)
    cursor.execute("SELECT * FROM RELATION WHERE IDService1=\'"+str(APIID1)+"\' AND IDService2=\'"+str(APIID2)+"\'")
    result=cursor.fetchall()
    #Si la relation existe déja on prend des nouvelles API
    while(len(result)!=0):
        APIID1=random.randint(1, 100)
        APIID2=random.randint(1, 100)
        while APIID1==APIID2:
            APIID2=random.randint(0, 100)
        cursor.execute("SELECT * FROM RELATION WHERE IDService1=\'"+str(APIID1)+"\' AND IDService2=\'"+str(APIID2)+"\'")
        result=cursor.fetchall()
    API1DateRequest='SELECT Submitted FROM API WHERE ID=\''+str(APIID1)+'\''
    API2DateRequest='SELECT Submitted FROM API WHERE ID=\''+str(APIID2)+'\''
    cursor.execute(API1DateRequest)
    API1DateResult=cursor.fetchone()
    cursor.execute(API2DateRequest)
    API2DateResult=cursor.fetchone()
    API1Date=API1DateResult[0]
    API2Date=API2DateResult[0]
    date="01:01:2007"
    request='INSERT INTO RELATION(IDService1,IDService2,dateObservation,typeRelation,poids) VALUES(\''+str(APIID1)+'\',\''+str(APIID2)+'\',\''+str(date)+'\',\''+str(relation)+'\',\''+str(r)+'\');'
    cursor.execute(request)
    db.commit()