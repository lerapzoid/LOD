import MySQLdb
import csv
import re
def interract(idservice1,idservice2,datebegin,dateend,seuil_interaction_neg):
    nbInterract=0
    nbInterractNegative=0
    nbInterractTemp=0
    processing=True
    listResult=None
    resultRange=None
    result=[]
    #Récupération du nom et de la date de publication des API
    API1Request='SELECT API_Name,Submitted FROM API WHERE ID=\''+str(idservice1)+'\''
    API2Request='SELECT API_Name,Submitted FROM API WHERE ID=\''+str(idservice2)+'\''
    cursor.execute(API1Request)
    API1Result=cursor.fetchone()
    API1Name=API1Result[0]
    cursor.execute(API2Request)
    API2Result=cursor.fetchone()
    API2Name=API2Result[0]
    API1Date=API1Result[1]
    API2Date=API2Result[1]
    #Récupération des API
    request='SELECT Related_API_,Submitted FROM MASHUP WHERE Related_API_ LIKE \'%'+API1Name+'%\'AND Related_API_ LIKE \'%,%\''
    cursor.execute(request)
    list=cursor.fetchall()
    request='SELECT Related_API_,Submitted FROM MASHUP WHERE Related_API_ LIKE \'%'+API2Name+'%\'AND Related_API_ LIKE \'%,%\''
    cursor.execute(request)
    list=list+cursor.fetchall()
    listResult=set(list)
    nbInterract=0
    nbInterractNegative=0
    processing=True
    #Vérification des dates de publication(ne depasse pas dateend)
    yearbegin=datebegin[6:10]
    monthbegin=datebegin[3:5]
    daybegin=datebegin[0:2]
    yearend=dateend[6:10]
    monthend=dateend[3:5]
    dayend=dateend[0:2]
    if(API1Date=="null"):
        API1Date="00.00.0000"
    if(API2Date=="null"):
        API2Date="00.00.0000"
    dayLowerRange=int(daybegin)
    monthLowerRange=int(monthbegin)
    yearLowerRange=int(yearbegin)
    dayUpperRange=dayLowerRange
    if (int(monthLowerRange)+seuil_interaction_neg)%12==0:
        monthUpperRange=12
        yearUpperRange=yearLowerRange
    else:
        monthUpperRange=(int(monthLowerRange)+seuil_interaction_neg)%12
        yearUpperRange=int(yearLowerRange)+((int(monthLowerRange)+seuil_interaction_neg)//12)
    #Boucle sur la durée datebegin dateend
    while processing:
        nbInterractTemp=nbInterract
        resultRange=()
        #Si la borne haute de la selection depasse on rabaisse la range a dateend
        if yearUpperRange>int(yearend):
            yearUpperRange=int(yearend)
            monthUpperRange=int(monthend)
            dayUpperRange=int(dayend)
            processing=False;
        elif yearUpperRange==int(yearend):
            if monthUpperRange>int(monthend):
                monthUpperRange=int(monthend)
                dayUpperRange=int(dayend)
                processing=False;
            elif monthUpperRange==int(monthend):
                if dayUpperRange>=int(dayend):
                    dayUpperRange=int(dayend)
                    processing=False;
        #Pour chaque element dans la liste des résultat on verifie dans un premier temps si la date n'est pas antérieur à la range
        for row in listResult:
            date=row[1]
            if int(date[6:10])>yearLowerRange:
                nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,row)
            elif int(date[6:10])==yearLowerRange:
                if int(date[0:2])>monthLowerRange:
                    nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,row)
                elif int(date[0:2])==monthLowerRange:
                    if int(date[3:5])>=dayLowerRange:
                        nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,row)
            #Si le nombre d'interraction n'as pas changer aprés l'étude des api dans la range on incrémente le nombre d'interraction negative
        if(nbInterractTemp==nbInterract):
            nbInterractNegative=nbInterractNegative-1
            #On incrémente la range
        dayLowerRange=dayUpperRange
        monthLowerRange=monthUpperRange
        yearLowerRange=yearUpperRange
        dayUpperRange=dayLowerRange
        if (int(monthLowerRange)+seuil_interaction_neg)%12==0:
            monthUpperRange=12
        else:
            monthUpperRange=(int(monthLowerRange)+seuil_interaction_neg)%12
            yearUpperRange=int(yearLowerRange)+((int(monthLowerRange)+seuil_interaction_neg)//12)
    result=[nbInterract,nbInterractNegative,API1Name,API2Name]
    print result
    return result
#Permet de regarder si les dates des row ne depasse pas la range
def UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,row):
    nbInterract=0
    exactRow=exactName(row)
    if int(date[6:10])<int(yearUpperRange):
        nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name)
    elif int(date[6:10])==int(yearUpperRange):
        if int(date[0:2])<int(monthUpperRange):
            nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name)
        elif int(date[0:2])==int(monthUpperRange):
            if int(date[3:5])<=int(dayUpperRange):
                nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name)
    return nbInterract
#Permet de ne pas compter des éléments non conforme ex:(Facebook, Facebook Graph)
def exactName(row):
    exactRow=row[0]
    exactRow=re.sub(" , ","_",exactRow)
    exactRow=re.sub(" ,","_",exactRow)
    exactRow=re.sub(", ","_",exactRow)
    exactRow=re.sub(",","_",exactRow)
    exactRow=re.split("_",exactRow)
    return exactRow
#Verifie si les deux API sont présentes dans la Mashup
def isInMashup(exactRow,API1Name,API2Name):
    API1In=False
    API2In=False
    for i in range (0,len(exactRow)):
        if(API1Name==exactRow[i]):
            API1In=True
        if(API2Name==exactRow[i]):
            API2In=True
    if(API1In and API2In):
        return 1
    elif(API1In or API2In):
        return 0
    else:
        return 0
def weight(current_weight, nb_positive_interaction, nb_total_interaction, coeff_current_weight, coeff_interaction):
    nb_positive_interaction=float(nb_positive_interaction)
    nb_total_interaction=float(nb_total_interaction)
    coeff_current_weight=float(coeff_current_weight)
    coeff_interaction=float(coeff_interaction)
    new_weight = (coeff_current_weight * current_weight + coeff_interaction * (nb_positive_interaction / nb_total_interaction))/(coeff_current_weight + coeff_interaction)
    return new_weight

db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
listID=[]
#On récupére la liste des interraction de notre cluster
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\ClusterAPI.csv')as csv_fileR:
    reader=csv.reader(csv_fileR)
    for row in reader:
        ID=[row[2],row[3]]
        listID.append(ID)
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\PrecisionV2.csv', mode='wb') as csv_file:
    fieldnames=['API1','API2','2007/2009','2009/2011','2011/2013','2013/2015','2015/2017']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    #Pour chaque interraction
    for i in range(0,len(listID)):
        ID=listID[i]
        result=interract(ID[0],ID[1],'01.01.2005','01.01.2007',6)
        poidsInit=weight(0.35, result[0], result[0]+(-result[1]), 1, 2)
        API1Name=result[2]
        API2Name=result[3]
        p2007=0
        p2009=0
        p2011=0
        p2013=0
        p2015=0
        #Pour chaque Periode
        for j in range(0,5):
            if j==0:
                #On crée la range
                datebegin='01.01.2007'
                dateend='01.01.2009'
                result=interract(ID[0],ID[1],datebegin,dateend,6)
                Newpoids=weight(poidsInit, result[0], result[0]+(-result[1]), 1, 2)
                #On regarde si la différence de poids est inférieur à 0.2 et on insére le pourccentage correspondant à la différence entre les poids
                if Newpoids-poidsInit<0.2 and poidsInit-Newpoids<0.2:
                    if Newpoids-poidsInit>0:
                        v=float(Newpoids-poidsInit)
                        p2007=float(100-((v*100)/0.2))
                        print p2007
                    elif poidsInit-Newpoids>0:
                        v=float(poidsInit-Newpoids)
                        p2007=float(100-((v*100)/0.2))
                        print p2007
                poidsInit=Newpoids
            if j==1:
                datebegin='01.01.2009'
                dateend='01.01.2011'
                result=interract(ID[0],ID[1],datebegin,dateend,6)
                Newpoids=weight(poidsInit, result[0], result[0]+(-result[1]), 1, 2)
                if Newpoids-poidsInit<0.2 and poidsInit-Newpoids<0.2:
                    if Newpoids-poidsInit>0:
                        v=float(Newpoids-poidsInit)
                        p2009=float(100-((v*100)/0.2))
                        print p2009
                    elif poidsInit-Newpoids>0:
                        v=float(poidsInit-Newpoids)
                        p2009=float(100-((v*100)/0.2))
                        print p2009
                poidsInit=Newpoids
            if j==2:
                datebegin='01.01.2011'
                dateend='01.01.2013'
                result=interract(ID[0],ID[1],datebegin,dateend,6)
                Newpoids=weight(poidsInit, result[0], result[0]+(-result[1]), 1, 2)
                if Newpoids-poidsInit<0.2 and poidsInit-Newpoids<0.2:
                    if Newpoids-poidsInit>0:
                        v=float(Newpoids-poidsInit)
                        p2011=float(100-((v*100)/0.2))
                        print p2011
                    elif poidsInit-Newpoids>0:
                        v=float(poidsInit-Newpoids)
                        p2011=float(100-((v*100)/0.2))
                        print p2011
                poidsInit=Newpoids
            if j==3:
                datebegin='01.01.2013'
                dateend='01.01.2015'
                result=interract(ID[0],ID[1],datebegin,dateend,6)
                Newpoids=weight(poidsInit, result[0], result[0]+(-result[1]), 1, 2)
                if Newpoids-poidsInit<0.2 and poidsInit-Newpoids<0.2:
                    if Newpoids-poidsInit>0:
                        v=float(Newpoids-poidsInit)
                        p2013=float(100-((v*100)/0.2))
                        print p2013
                    elif poidsInit-Newpoids>0:
                        v=float(poidsInit-Newpoids)
                        p2013=float(100-((v*100)/0.2))
                        print p2013
                poidsInit=Newpoids
            if j==4:
                datebegin='01.01.2015'
                dateend='01.01.2017'
                result=interract(ID[0],ID[1],datebegin,dateend,6)
                Newpoids=weight(poidsInit, result[0], result[0]+(-result[1]), 1, 2)
                if Newpoids-poidsInit<0.2 and poidsInit-Newpoids<0.2:
                    if Newpoids-poidsInit>0:
                        v=float(Newpoids-poidsInit)
                        p2015=float(100-((v*100)/0.2))
                        print p2015
                    elif poidsInit-Newpoids>0:
                        v=float(poidsInit-Newpoids)
                        p2015=float(100-((v*100)/0.2))
                        print p2015
                poidsInit=Newpoids
        writer.writerow({'API1':API1Name,'API2':API2Name,'2007/2009':p2007,'2009/2011':p2009,'2011/2013':p2011,'2013/2015':p2013,'2015/2017':p2015})