import MySQLdb
import re
import csv
#Création du csv StatAPI qui permet de savoir le nombre d'interraction entre API ainsi que dans quelle Mashup l'interraction a eu lieu
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
liste = {}
value={}
maxRequest="SELECT ID FROM MASHUP WHERE Related_API_ LIKE '%,%,%,%,%' AND SUBSTR(Submitted,7,4)>'2007' AND SUBSTR(Submitted,7,4)<'2011'"
cursor.execute(maxRequest)
maxResult=cursor.fetchall()
#Récupération des API de chaque Mashup
for row in maxResult:
    request='SELECT Related_API_ FROM MASHUP WHERE ID=\''+row+'\''
    cursor.execute(request)
    result=cursor.fetchone()
    result=re.sub(" , ","_",result[0])
    result=re.sub(" ,","_",result)
    result=re.sub(", ","_",result)
    result=re.sub(",","_",result)
    result=re.split("_",result)
    #Pour chaque duo d'API on incrémente le nombre d'interraction et on garde l'ID de la Mashup
    for j in range(0,len(result)):
        try:
            value=liste[result[j]]
            for k in range(0,len(result)):
                if result[k]!=result[j]:
                    try:
                        value2=value[result[k]]
                        value2[0]=value2[0]+1
                        value2[1]=value2[1]+","+str(i)
                        value[result[k]]=value2
                    except:
                        value[result[k]]=[1,str(i)]
            liste[result[j]]=value
        except:
            value={}
            for l in range(0,len(result)):
                if result[l]!=result[j]:
                    value[result[l]]=[1,str(i)]
            liste[result[j]]=value
#On produit le csv
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\StatAPI2.csv', mode='wb') as csv_file:
    fieldnames=["API1","API2","Nombre d\'interractions","ID Mashup"]
    writer = csv.DictWriter(csv_file,fieldnames)
    for listeRow in liste:
        for cle,valeur in liste[listeRow].items():
            writer.writerow({'API1':listeRow,'API2':cle,'Nombre d\'interractions':valeur[0],'ID Mashup':valeur[1]})