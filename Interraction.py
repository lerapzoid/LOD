import MySQLdb
import random
import re
def interract(idservice1,idservice2,datebegin,dateend,seuil_interaction_neg):
    nbInterract=0
    nbInterractNegative=0
    nbInterractTemp=0
    processing=True
    listResult=None
    resultRange=None
    #Récupération du nom et de la date de publication des API
    API1Request='SELECT API_Name,Submitted FROM API WHERE ID=\''+str(idservice1)+'\''
    API2Request='SELECT API_Name,Submitted FROM API WHERE ID=\''+str(idservice2)+'\''
    cursor.execute(API1Request)
    API1Result=cursor.fetchone()
    API1Name=API1Result[0]
    print API1Name
    cursor.execute(API2Request)
    API2Result=cursor.fetchone()
    API2Name=API2Result[0]
    print API2Name
    API1Date=API1Result[1]
    API2Date=API2Result[1]
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
    #Récupération des API
    request='SELECT Related_API_,Submitted FROM MASHUP WHERE Related_API_ LIKE \'%'+API1Name+'%\''
    cursor.execute(request)
    list=cursor.fetchall()
    request='SELECT Related_API_,Submitted FROM MASHUP WHERE Related_API_ LIKE \'%'+API2Name+'%\''
    cursor.execute(request)
    list=list+cursor.fetchall()
    listResult=set(list)
    #Création de la range nécessaire afin de pouvoir calculer le nombre d'interraction negative
    dayLowerRange=daybegin
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
                if dayUpperRange>int(dayend):
                    dayUpperRange=int(dayend)
                    processing=False;
        #Pour chaque element dans la liste des résultat on verifie dans un premier temps si la date n'est pas antérieur à la range
        #print listResult
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
    result=[nbInterract,nbInterractNegative]
    return result
#Permet de regarder si les dates des row ne depasse pas la range
def UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,row):
    nbInterract=0
    exactRow=exactName(row)
    if int(date[6:10])<yearUpperRange:
        nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name)
    elif int(date[6:10])==yearUpperRange:
        if int(date[0:2])<monthUpperRange:
            nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name)
        elif int(date[0:2])==monthUpperRange:
            if int(date[3:5])<=dayUpperRange:
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
        #print exactRow
        return 0
    else:
        #print exactRow
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
#Sélection de 2 API aléatoires différentes
maxRequest='SELECT COUNT(*) FROM API'
cursor.execute(maxRequest)
maxResult=cursor.fetchone()
max=maxResult[0]
APIID1=random.randint(0, max)
APIID2=random.randint(0, max)
while APIID1==APIID2:
    APIID2=random.randint(0, max)
datebegin="01.06.2005"
dateend="01.01.2020"
result=interract(1,2,datebegin,dateend,6)
#print result
print result[0]
print -result[1]
w = weight(0.35, result[0], result[0]+(-result[1]), 1, 2)
print("weight :" + str(w))