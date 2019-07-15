import MySQLdb
import random
import re
import time
def evolution():
    c=1
    #On recupére les relations de la table(le code actuel ne fait pas le tri entre les différentes itération
    request="select IDService1,IDService2,poids from RELATION Where SUBSTR(dateObservation,7,4)>\'2009\' AND typeRelation='Composition'"
    cursor.execute(request)
    list=cursor.fetchall()
    print len(list)
    for row in list:
        print c
        APIID1=row[0]
        APIID2=row[1]
        poids=row[2]
        datebegin="01.01.2011"
        dateend="01.01.2013"
        seuil_interaction_neg=6
        #On execute la fonction d'interaction pour chaque duo de service
        result=interract(APIID1,APIID2,datebegin,dateend,seuil_interaction_neg)
        if(result!=None):
            nbInterract=result[0]
            nbInterractNegative=result[1]
        dateObs="01.01.2013"
        #On calcule le nouveau poids
        w = weight(poids, nbInterract, nbInterract+(-nbInterractNegative), 1, 2)
        #Insertion de la nouvelle relation
        request='INSERT INTO RELATION(IDService1,IDService2,dateObservation,typeRelation,poids) VALUES(\''+str(APIID1)+'\',\''+str(APIID2)+'\',\''+str(dateObs)+'\',\'Composition\',\''+str(w)+'\')'
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
def interract(idservice1,idservice2,datebegin,dateend,seuil_interaction_neg):
    nbInterract=0
    nbInterractNegative=0
    nbInterractTemp=0
    processing=True
    listResult=None
    resultRange=None
    #Récupération des attribut des API
    #API1Request='SELECT API_Name,Primary_Category,Secondary_Categories,API_Description,Supported_Request_Formats,Supported_Response_Formats,Submitted FROM API WHERE ID=\''+str(idservice1)+'\''
    API1Request='SELECT API_Name,Primary_Category,Submitted FROM API WHERE ID=\''+str(idservice1)+'\''
    #API2Request='SELECT API_Name,Primary_Category,Secondary_Categories,API_Description,Supported_Request_Formats,Supported_Response_Formats,Submitted FROM API WHERE ID=\''+str(idservice2)+'\''
    API2Request='SELECT API_Name,Primary_Category,Submitted FROM API WHERE ID=\''+str(idservice2)+'\''
    cursor.execute(API1Request)
    API1Result=cursor.fetchone()
    API1Name=API1Result[0]
    #print API1Name
    cursor.execute(API2Request)
    API2Result=cursor.fetchone()
    API2Name=API2Result[0]
    #print API2Name
    #API1Date=API1Result[6]
    #API2Date=API2Result[6]
    API1Date=API1Result[2]
    API2Date=API2Result[2]
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
        for row in listResult:
            date=row[1]
            if int(date[6:10])>yearLowerRange:
                nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,API1Result,API2Result,row)
            elif int(date[6:10])==yearLowerRange:
                if int(date[0:2])>monthLowerRange:
                    nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,API1Result,API2Result,row)
                elif int(date[0:2])==monthLowerRange:
                    if int(date[3:5])>=dayLowerRange:
                        nbInterract=nbInterract+UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,API1Result,API2Result,row)
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
def UpperRange(date,yearUpperRange,monthUpperRange,dayUpperRange,API1Name,API2Name,API1Result,API2Result,row):
    nbInterract=0
    exactRow=exactName(row)
    if int(date[6:10])<yearUpperRange:
        nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name,API1Result,API2Result)
    elif int(date[6:10])==yearUpperRange:
        if int(date[0:2])<monthUpperRange:
            nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name,API1Result,API2Result)
        elif int(date[0:2])==monthUpperRange:
            if int(date[3:5])<=dayUpperRange:
                nbInterract=nbInterract=isInMashup(exactRow,API1Name,API2Name,API1Result,API2Result)
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
def isInMashup(exactRow,API1Name,API2Name,API1Result,API2Result):
    API1In=False
    API2In=False
    #On récupére les attribut de toute les API lié à la Mashup
    #request='SELECT API_Name,Primary_Category,Secondary_Categories,API_Description,Supported_Request_Formats,Supported_Response_Formats FROM API WHERE API_Name IN ('
    request='SELECT API_Name,Primary_Category FROM API WHERE API_Name IN ('
    #On crée la requete de recupération
    for j in range (0,len(exactRow)):
        request=request+'\''+exactRow[j]+'\''
        if(j!=len(exactRow)):
            request=request+","
    request=request[0:len(request)-1]+")"
    cursor.execute(request)
    listAPIM=cursor.fetchall()
    #On vérifie si les API de la relation sont lie à la mashup
    for i in range (0,len(exactRow)):
        #print i
        if(API1Name==exactRow[i]):
            API1In=True
        elif(API2Name==exactRow[i]):
            API2In=True
    #On vérifie si des API similaire à celle de la relation sont liée à la Mashup
    for k in range (0,len(listAPIM)):
        if(listAPIM[k]!=None):
            if compareAttribut(listAPIM[k],API1Result):
                API1In=True
            elif compareAttribut(listAPIM[k],API2Result):
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
def compareAttribut(API1,API2):
    #On crée un compteur qui nous permettera de vérifié si un certains pourcentage d'attribut voulue corresponde entre les deux API
    similarity=0
    similarity=similarity+comparePrimary(API1[1],API2[1])
    #similarity=similarity+compareSecondary(API1[2],API2[2])
    #similarity=similarity+compareDescription(API1[3],API2[3])
    #similarity=similarity+compareRequest(API1[4],API2[4])
    #similarity=similarity+compareResponse(API1[5],API2[5])
    if(similarity==1):
        return True
    else:
        return False
def comparePrimary(primary1,primary2):
    if(primary1=="null" and primary2=="null"):
        return 0
    elif(primary1==primary2):
        return 1
    else:
        return 0
def compareSecondary(secondary1,secondary2):
    allInclude=True
    #On sépare tou les éléments
    secondary1=re.sub(" , ","_",secondary1)
    secondary1=re.sub(" ,","_",secondary1)
    secondary1=re.sub(", ","_",secondary1)
    secondary1=re.sub(",","_",secondary1)
    secondary1=re.split("_",secondary1)
    secondary2=re.sub(" , ","_",secondary2)
    secondary2=re.sub(" ,","_",secondary2)
    secondary2=re.sub(", ","_",secondary2)
    secondary2=re.sub(",","_",secondary2)
    secondary2=re.split("_",secondary2)
    #On vérifie que l' attribut de l'API est inclue dans la deuxiéme si c'eest le cas on considére qu'elles sont similaire du faite que l'une est une version plus générale de l'autre
    if(len(secondary1)>len(secondary2)):
        for i in range(0,len(secondary2)):
            if secondary2[i] not in secondary1:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(len(secondary2)>len(secondary1)):
        for i in range(0,len(secondary1)):
            if secondary1[i] not in secondary2:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(secondary1[0]=="null" and secondary2[0]=="null"):
        return 0
    #Si les attribut sont les même
    elif(secondary1==secondary2):
        return 1
    else:
        return 0
def compareDescription(description1,description2):
    #En attente de la fonction
    return 1
def compareRequest(format1,format2):
    allInclude=True
    format1=re.sub(" , ","_",format1)
    format1=re.sub(" ,","_",format1)
    format1=re.sub(", ","_",format1)
    format1=re.sub(",","_",format1)
    format1=re.split("_",format1)
    format2=re.sub(" , ","_",format2)
    format2=re.sub(" ,","_",format2)
    format2=re.sub(", ","_",format2)
    format2=re.sub(",","_",format2)
    format2=re.split("_",format2)
    #On vérifie que l' attribut de l'API est inclue dans la deuxiéme si c'eest le cas on considére qu'elles sont similaire du faite que l'une est une version plus générale de l'autre
    if(len(format1)>len(format2)):
        for i in range(0,len(format2)):
            if format2[i] not in format1:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(len(format2)>len(format1)):
        for i in range(0,len(format1)):
            if format1[i] not in format2:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(format1[0]=="null" and format2[0]=="null")or(format1[0]=="None Specified" and format2[0]=="None Specified")or(format1[0]=="Unspecified" and format2[0]=="Unspecified"):
        return 0
    #Si les attribut sont les même
    elif(format1==format2):
        return 1
    else:
        return 0
def compareResponse(format1,format2):
    allInclude=True
    format1=re.sub(" , ","_",format1)
    format1=re.sub(" ,","_",format1)
    format1=re.sub(", ","_",format1)
    format1=re.sub(",","_",format1)
    format1=re.split("_",format1)
    format2=re.sub(" , ","_",format2)
    format2=re.sub(" ,","_",format2)
    format2=re.sub(", ","_",format2)
    format2=re.sub(",","_",format2)
    format2=re.split("_",format2)
    #On vérifie que l' attribut de l'API est inclue dans la deuxiéme si c'eest le cas on considére qu'elles sont similaire du faite que l'une est une version plus générale de l'autre
    if(len(format1)>len(format2)):
        for i in range(0,len(format2)):
            if format2[i] not in format1:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(len(format2)>len(format1)):
        for i in range(0,len(format1)):
            if format1[i] not in format2:
                allInclude=False
        if(allInclude):
            return 1
        else:
            return 0
    elif(format1[0]=="null" and format2[0]=="null")or(format1[0]=="None Specified" and format2[0]=="None Specified")or(format1[0]=="Unspecified" and format2[0]=="Unspecified"):
        return 0
    #Si les attribut sont les même
    elif(format1==format2):
        return 1
    else:
        return 0
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
cursor = db.cursor()
evolution()