import requests
import MySQLdb
#Permet d'annoter le texte en parametre a partir de DBPedia Spotlight
def annotate(text):
    headers = {'accept': 'application/json',}
    params = (
    ('text',text),
)
    response = requests.get('https://api.dbpedia-spotlight.org/en/annotate', headers=headers, params=params)
    return response
#Récupére la description d'une API à partir de la base de donnée
def getAPIDescription(API):
    db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
    cursor = db.cursor()
    request='SELECT API_Description FROM API WHERE API_Name = \''+API+'\''
    cursor.execute(request)
    result=cursor.fetchone()
    return result
#Récupére la description d'une Mashup à partir de la base de donnée
def getMashupDescription(Mashup):
    db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="network")
    cursor = db.cursor()
    request='SELECT Mashup_Description FROM MASHUP WHERE Mashup_Name = \''+Mashup+'\''
    cursor.execute(request)
    result=cursor.fetchone()
    return result
#On retourne les annotation séparé
def semanticparse(data):
    semantictags = [];
    for k, v in data.items():
        if (k=="Resources"):
            #print(v)
            for elt in v:
                #print(elt)
                for k, vl in elt.items():
                    if k == "@URI":
                        semantictags.append(vl);

    return semantictags
textA=getAPIDescription('MetaLocator')
textM=getMashupDescription('Honeygain')
#print textA
JSONA=annotate(textA)
#print textM
JSONM=annotate(textM)
JSONA=JSONA.json()
JSONM=JSONM.json()
dA = set(semanticparse(JSONA))
dM = set(semanticparse(JSONM))
print(dA)
print(dM)