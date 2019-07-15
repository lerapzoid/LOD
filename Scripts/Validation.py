import MySQLdb
import csv
import re
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)<'2007'"
cursor.execute(request)
result=cursor.fetchall()
newList=[]
#On récupére les API liée au Mashup crée avant 2007
for row in result:
    #On transforme l'attribut Related_API_ de la Mashup en une liste d'API
    APIBrut=row[0]
    APIBrut=re.sub(" , ","_",APIBrut)
    APIBrut=re.sub(" ,","_",APIBrut)
    APIBrut=re.sub(", ","_",APIBrut)
    APIBrut=re.sub(",","_",APIBrut)
    listAPI=re.split("_",APIBrut)
    #On prend les API 2 par 2
    for i in range(0,len(listAPI)-1):
        for j in range(i+1,len(listAPI)):
            APIOrder1=False
            APIOrder2=False
            API1=listAPI[i]+"/"+listAPI[j]
            API2=listAPI[j]+"/"+listAPI[i]
            #On regarde si les 2 ordre sont dans la liste
            try:
                newList.index(API1)
            except:
                APIOrder1=True
            try:
                newList.index(API2)
            except:
                APIOrder2=True
            if APIOrder1 and APIOrder2:
                newList.append(API1)
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\Validation.csv', mode='wb') as csv_file:
    fieldnames=['Periode','Pourcentage']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    periode=""
    #Pour chaque Periode
    for k in range (0,5):
        #On récupére les API liée au Mashup
        if k==0:
            request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2006' AND SUBSTR(Submitted,7,4)<2010"
            periode="2007/2009"
        if k==1:
            request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2008' AND SUBSTR(Submitted,7,4)<2012"
            periode="2009/2011"
        if k==2:
            request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2010' AND SUBSTR(Submitted,7,4)<2014"
            periode="2011/2013"
        if k==3:
            request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2012' AND SUBSTR(Submitted,7,4)<2016"
            periode="2013/2015"
        if k==4:
            request="SELECT Related_API_,Submitted FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2014' AND SUBSTR(Submitted,7,4)<2018"
            periode="2015/2017"
        cursor.execute(request)
        result=cursor.fetchall()
        newList2=[]
        inNewList=[]
        nbRelation=0
        for row in result:
            #On transforme l'attribut Related_API_ de la Mashup en une liste d'API
            APIBrut=row[0]
            APIBrut=re.sub(" , ","_",APIBrut)
            APIBrut=re.sub(" ,","_",APIBrut)
            APIBrut=re.sub(", ","_",APIBrut)
            APIBrut=re.sub(",","_",APIBrut)
            listAPI=re.split("_",APIBrut)
            #On prend les API 2 par 2
            for i in range(0,len(listAPI)-1):
                for j in range(i+1,len(listAPI)):
                    nbRelation=nbRelation+1
                    APIOrder1=False
                    APIOrder2=False
                    APINewOrder1=False
                    APINewOrder2=False
                    API1=listAPI[i]+"/"+listAPI[j]
                    API2=listAPI[j]+"/"+listAPI[i]
                    try:
                        newList.index(API1)
                    except:
                        APIOrder1=True
                    try:
                        newList.index(API2)
                    except:
                        APIOrder2=True
                    try:
                        newList2.index(API1)
                    except:
                        APINewOrder1=True
                    try:
                        newList2.index(API2)
                    except:
                        APINewOrder2=True
                    #Si l'interraction existe deja dans newList on ajoute la relation a inNewList
                    if APIOrder1==False or APIOrder2==False:
                        inNewList.append(API1)
                    #Si l'interraction n'existe pas dans newList et newList2 on l'ajoute a newList2
                    if APIOrder1 and APIOrder2 and APINewOrder1 and APINewOrder2:
                        newList2.append(API1)
        newList=newList+newList2
        nb=float(len(inNewList))
        total=float(nbRelation)
        #On insére l'entrée dans le csv
        writer.writerow({'Periode':periode,'Pourcentage':float((nb*100)/total)})
        print float((nb*100)/total)