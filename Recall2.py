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
    result=[nbInterract,nbInterractNegative]
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
#On récupére la liste des API publiée avant 2007
request="SELECT API_Name FROM API WHERE SUBSTR(Submitted,7,4)<'2007'"
cursor.execute(request)
result=cursor.fetchall()
listAPIM=[]
listAPI=[]
for row in result:
    listAPI.append(row[0])
with open('E:\\Fac\\Informatique\\Python\\txtFiles\\Recall2.csv', mode='ab') as csv_file:
    fieldnames=['Mashup','Periode','Precision','API']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #writer.writeheader()
    #Pour chaque Periode
    for i in range(0,5):
        #On récupére les API liée au Mashup
        if i==0:
            request="SELECT Related_API_,Mashup_Name FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2006' AND SUBSTR(Submitted,7,4)<2009 AND Related_API_ LIKE '%,%,%,%,%'"
            periode="2007/2009"
        if i==1:
            request="SELECT Related_API_,Mashup_Name FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2008' AND SUBSTR(Submitted,7,4)<2011 AND Related_API_ LIKE '%,%,%,%,%'"
            periode="2009/2011"
        if i==2:
            request="SELECT Related_API_,Mashup_Name FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2010' AND SUBSTR(Submitted,7,4)<2013 AND Related_API_ LIKE '%,%,%,%,%'"
            periode="2011/2013"
        if i==3:
            request="SELECT Related_API_,Mashup_Name FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2012' AND SUBSTR(Submitted,7,4)<2015 AND Related_API_ LIKE '%,%,%,%,%'"
            periode="2013/2015"
        if i==4:
            request="SELECT Related_API_,Mashup_Name FROM MASHUP WHERE SUBSTR(Submitted,7,4)>'2014' AND SUBSTR(Submitted,7,4)<2018 AND Related_API_ LIKE '%,%,%,%,%'"
            periode="2015/2017"
        cursor.execute(request)
        result=cursor.fetchall()
        for row in result:
            #On transforme l'attribut Related_API_ de la Mashup en une liste d'API
            print row[1]
            APIBrut=row[0]
            APIBrut=re.sub(" , ","_",APIBrut)
            APIBrut=re.sub(" ,","_",APIBrut)
            APIBrut=re.sub(", ","_",APIBrut)
            APIBrut=re.sub(",","_",APIBrut)
            listAPIM=re.split("_",APIBrut)
            nbInterract=0
            nbPositif=0
            tabInterraction=""
            #On prend les API 2 par 2
            for k in range(0,len(listAPIM)-1):
                for j in range(k+1,len(listAPIM)):
                    API1=listAPIM[k]
                    API2=listAPIM[j]
                    NotNewAPI1=True
                    NotNewAPI2=True
                    #On regarde si les 2 API sont dans la liste
                    try:
                        listAPI.index(API1)
                    except:
                        NotNewAPI1=False
                    try:
                        listAPI.index(API2)
                    except:
                        NotNewAPI2=False
                    #Si les deux API existait deja on les compare
                    if NotNewAPI1 and NotNewAPI2:
                        #On récupére les ID des API
                        nbInterract=nbInterract+1
                        request1="SELECT ID FROM API WHERE API_Name=\'"+API1+"\'"
                        cursor.execute(request1)
                        API1ID=cursor.fetchone()
                        request2="SELECT ID FROM API WHERE API_Name=\'"+API2+"\'"
                        cursor.execute(request2)
                        API2ID=cursor.fetchone()
                        resultI=[]
                        try:
                            datebegin="01.01."+periode[0:4]
                            dateend="01.01."+periode[5:9]
                            print API1
                            print API2
                            #On regarde l'interraction des 2 API
                            resultI=interract(API1ID[0],API2ID[0],datebegin,dateend,6)
                            w = weight(0.35, resultI[0], resultI[0]+(-resultI[1]), 1, 2)
                            #Si le poids est supérieur au seuil on compte une interraction supplémentaire pour la Mashup et on ajoute les 2 API a la liste des interraction
                            if w>0.5:
                                nbPositif=nbPositif+1
                                if tabInterraction=="":
                                    tabInterraction=API1+"/"+API2
                                else:
                                    tabInterraction=tabInterraction+";"+API1+"/"+API2
                        except:
                            resultT=[0,0]
            #On calcule le pourcentage de l'API que on a valider
            nbInterract=float(nbInterract)
            nbPositif=float(nbPositif)
            if nbInterract==0:
                p=0
            else:
                p=float((nbPositif*100)/nbInterract)
            #On insére l'entrée dans le csv
            writer.writerow({'Mashup':row[1],'Periode':periode,'Precision':p,'API':tabInterraction})
        request="SELECT API_Name FROM API WHERE SUBSTR(Submitted,7,4)<'"+periode[5:9]+"' AND SUBSTR(Submitted,7,4)>'"+str(int(periode[0:4])-1)+"'"
        cursor.execute(request)
        result=cursor.fetchall()
        #On ajoute à la liste des API les API nouvellement crée
        for row in result:
            try:
                listAPI.index(row[0])
            except:
                listAPI.append(row[0])