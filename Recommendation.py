import MySQLdb
import re
import csv
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
#On récupére la liste des relation
request="select IDService1,IDService2,dateObservation,typeRelation,poids from RELATION WHERE SUBSTR(dateObservation,7,4)>\'2007\'"
cursor.execute(request)
result=cursor.fetchall()
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\Recommendation.csv', mode='wb') as csv_file:
    fieldnames=['IDService1','IDService2','dateObservation','typeRelation','poids','differencePoids']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    #Pour chaque element de la liste
    for row in result:
        print row
        date=row[2]
        date=date[0:6]+str(int(date[6:10])-2)
        #On récupére le poids de l'interraction suivante
        request="select poids from RELATION WHERE IDService1='"+str(row[0])+"' AND IDService2='"+str(row[1])+"' AND dateObservation='"+date+"'"
        cursor.execute(request)
        result2=cursor.fetchall()
        row2=result2[0]
        diff=row[4]-row2[0]
        #On insére l'entrée dans le csv
        writer.writerow({'IDService1':str(row[0]),'IDService2':str(row[1]),'dateObservation':str(row[2]),'typeRelation':str(row[3]),'poids':str(row[4]),'differencePoids':str(diff)})