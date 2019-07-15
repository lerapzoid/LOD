import random
import MySQLdb
import csv

mydb = MySQLdb.connect(
        host='localhost',
        db='network',
        user='root',
        passwd='root')

mycursor = mydb.cursor()


def newrelationsSup(serviceid, iteration_i, iteration_j, typerelation):
    # sql = "SELECT COUNT(servicej) AS nbpeers FROM relations WHERE servicei = 1 AND iteration = 3 AND weight > 0.5 AND relation='composition' AND servicej NOT IN (SELECT servicej FROM relations where servicei = 1 and iteration = 1 AND weight > 0.5 AND relation= 'composition')"
    sql = "SELECT COUNT(IDService2) AS nbpeers FROM RELATION WHERE IDService1 = %s AND dateObservation = %s AND poids < 0.5 AND typeRelation = %s AND IDService2 NOT IN (SELECT IDService2 FROM RELATION where IDService1 = %s and dateObservation = %s AND poids < 0.5 AND typeRelation= %s)"
    val = (serviceid, iteration_j, typerelation, serviceid, iteration_i, typerelation)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for x in myresult:
        nb_newpeers = x[0]
        #print(nb_newpeers)

    return nb_newpeers

def newrelations1Inf(serviceid, iteration_i, iteration_j, typerelation):
    # sql = "SELECT COUNT(servicej) AS nbpeers FROM relations WHERE servicei = 1 AND iteration = 3 AND weight > 0.5 AND relation='composition' AND servicej NOT IN (SELECT servicej FROM relations where servicei = 1 and iteration = 1 AND weight > 0.5 AND relation= 'composition')"
    sql = "SELECT COUNT(IDService2) AS nbpeers FROM RELATION WHERE IDService1 = %s AND dateObservation = %s AND poids > 0.5 AND typeRelation = %s AND IDService2 NOT IN (SELECT IDService2 FROM RELATION where IDService1 = %s and dateObservation = %s AND poids > 0.5 AND typeRelation= %s)"
    val = (serviceid, iteration_j, 'Composition', serviceid, iteration_i, 'Composition')
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for x in myresult:
        nb_newpeers = x[0]
        #print(nb_newpeers)

    return nb_newpeers

def savedata(i, j, typerelation, poids, iteration, mycursor):
    sql = "INSERT INTO relations (servicei, servicej, relation, weight, iteration) VALUES (%s, %s, %s, %s, %s)"
    val = (i, j, typerelation, poids, iteration)
    mycursor.execute(sql, val)
    mydb.commit()

# sql = "DELETE FROM relations WHERE id >= 1"
# mycursor.execute(sql)
# mydb.commit()
# print(mycursor.rowcount, "record(s) deleted")

# for o in range(0, 5):
#     for i in range(0, 100):
#         for j in range(0, 100):
#             if (i == j):
#                 print(str(i) + ", " + str(j) + ", " + str(0) + ", relation, observation:"+ str(o))
#             else:
#                 print(str(i) + ", " + str(j) + ", " + str(random.random()) + ", composition, observation:"+ str(o))
#                 savedata(i, j, "composition", random.random(), o, mycursor)
#                 print(str(i) + ", " + str(j) + ", " + str(random.random()) + ", substitution, observation:"+ str(o))
#                 savedata(i, j, "substitution", random.random(), o, mycursor)
#                 print(str(i) + ", " + str(j) + ", " + str(random.random()) + ", interest, observation:"+ str(o))
#                 savedata(i, j, "interest", random.random(), o, mycursor)
nouv=0
nouv1=0
nouv2=0
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\NewRelation.csv', mode='wb') as csv_file:
    fieldnames=['DateObservation','Relation','Pourcentage']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for k in range(0,2):
        if k==0:
            relation="Composition"
        if k==1:
            relation="Substitution"
        for i in range(0,5):
            for j in range(1,600):
                if i==0:
                    nouv1=nouv1+newrelations(j, "01.01.2007", "01.01.2009", relation)
                    nouv2=nouv2+newrelations1(j, "01.01.2007", "01.01.2009", relation)
                    nouv=nouv1+nouv2
                elif i==1:
                    nouv1=nouv1+newrelations(j, "01.01.2009", "01.01.2011", relation)
                    nouv2=nouv2+newrelations1(j, "01.01.2009", "01.01.2011", relation)
                    nouv=nouv1+nouv2
                elif i==2:
                    nouv1=nouv1+newrelations(j, "01.01.2011", "01.01.2013", relation)
                    nouv2=nouv2+newrelations1(j, "01.01.2011", "01.01.2013", relation)
                    nouv=nouv1+nouv2
                elif i==3:
                    nouv1=nouv1+newrelations(j, "01.01.2013", "01.01.2015", relation)
                    nouv2=nouv2+newrelations1(j, "01.01.2013", "01.01.2015", relation)
                    nouv=nouv1+nouv2
                elif i==4:
                    nouv1=nouv1+newrelations(j, "01.01.2015", "01.01.2017", relation)
                    nouv2=nouv2+newrelations1(j, "01.01.2015", "01.01.2017", relation)
                    nouv=nouv1+nouv2
            print nouv1
            print nouv2
            print nouv
            if i==0:
                writer.writerow({'DateObservation':"01.01.2007/01.01.2009",'Relation':relation,'Pourcentage':nouv*2})
            elif i==1:
                writer.writerow({'DateObservation':"01.01.2009/01.01.2011",'Relation':relation,'Pourcentage':nouv*2})
            elif i==2:
                writer.writerow({'DateObservation':"01.01.2011/01.01.2013",'Relation':relation,'Pourcentage':nouv*2})
            elif i==3:
                writer.writerow({'DateObservation':"01.01.2013/01.01.2015",'Relation':relation,'Pourcentage':nouv*2})
            elif i==4:
                writer.writerow({'DateObservation':"01.01.2015/01.01.2017",'Relation':relation,'Pourcentage':nouv*2})
            print"================="
            nouv=0
            nouv1=0
            nouv2=0
#newrelations(161, "01.01.2010", "01.01.2014", "Composition")