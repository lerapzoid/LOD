import urllib
import re
import csv
APIDone=0
fieldnames=[]
description=""
dict={}
#On récupére la liste des paramétres des API a partir de programmableweb
def specNameLister ():
    listName=[]
    last=0
    url=urllib.urlopen("https://www.programmableweb.com/add/api")
    page=url.read().decode('utf-8')
    listSpec = re.findall(r""+"<label"+".+"+"</label>", page)
    for i in range (0,len(listSpec)-1):
        nameSpec=re.sub("<.*?>","",listSpec[i])
        nameSpec=re.sub("&#039;","\'",nameSpec)
        nameSpec=re.sub(" \*","",nameSpec)
        #On supprime les éléments qui ne sont pas des champs
        if (nameSpec=="Yes" or nameSpec=="No" or nameSpec=="URL" or nameSpec=="Other(not listed)" or nameSpec=="Other Response Format"or nameSpec=="Type of License if Non-Proprietary"):
            last=i
        #A partir de cet élément on a plus de nouveau champs d'API
        elif(nameSpec=="Leave this field blank"):
            break
        else:
            listName.append(nameSpec)
    return listName
#On parcours les page qui liste les API et on écrit les données dans le csv
def PageLister():
    global fieldnames
    global dict
    page=urllib.urlopen('https://www.programmableweb.com/category/all/apis')
    #page=urllib.urlopen('https://www.programmableweb.com/category/all/mashup')
    strpage=page.read().decode('utf-8')
    pagerLast=re.findall("<li class=\"pager-next\">"+".+"+"?</li>",strpage,re.DOTALL)
    countPage=re.sub("<.*?>","",pagerLast[0])
    countPage=int(countPage)
    #with open('E:\\Fac\\Informatique\\Python\\txtFiles\\API.csv', mode='ab') as csv_file:
    with open('E:\\Fac\\Informatique\\Python\\txtFiles\\APIMashup.csv', mode='ab') as csv_file:
        fieldnames=specNameLister()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
        APILister('https://www.programmableweb.com/category/all/apis')
        #APILister('https://www.programmableweb.com/category/all/mashups')
        for x in range(1,countPage-1):
            path="https://www.programmableweb.com/category/all/apis?page="+str(x)
            #path="https://www.programmableweb.com/category/all/mashups?page="+str(x)
            APILister(path)
            #Toute les 100 API on enregistre dans le csv
            if(len(dict)%100==0 or len(dict)>100):
                print "Saving"
                compt=0
                for k, v in dict.items():
                    writer.writerow(v)
                    compt=compt+1
                    percent=(compt*100)/len(dict)
                    print percent," % done"
                dict={}
                print "Save done"
#On accéde a la page qui liste les information de chaque API ou Mashup
def APILister(path):
    page=urllib.urlopen(path)
    strpage=page.read().decode('utf-8')
    listAPIPage=re.findall("<table class="+".+"+"?</table>",strpage ,re.DOTALL)
    listAPI=re.findall("<tr"+".+"+"?</tr>",listAPIPage[2] ,re.DOTALL)
    for j in range(1,len(listAPI)):
        listAttributeAPI=re.findall("<td"+".+"+"?</td>",listAPI[j] ,re.DOTALL)
        href=re.findall("<a href="+".+"+"?</a>",listAttributeAPI[0])
        splitHref=re.split("\"", href[0])
        splitHref[2]=re.sub("</a>","",splitHref[2])
        splitHref[2]=re.sub(">","",splitHref[2])
        splitHref[2]=re.sub("&#039","\'",splitHref[2])
        splitHref[2]=splitHref[2].encode('ascii','ignore')
        dict2={}
        dict2[fieldnames[0]]=splitHref[2]
        dict[APIDone]=dict2
        path="https://www.programmableweb.com"+splitHref[1]
        print splitHref[1]
        specLister(path)
        #APIByMashup(path)
#On accéde a la page qui liste les information de chaque API dans une Mashup
def APIByMashup (path):
    url=urllib.urlopen(path)
    page=url.read().decode('utf-8')
    listSpec = re.findall(r""+"<label>"+".+"+"</label>", page)
    if(listSpec==[]):
        listSpec=None
    else:
        listSpec[0]=re.escape(listSpec[0])
        spec=re.split(listSpec[0],page)
        spec=re.split(listSpec[1],spec[1])
        attribute=re.split("<span>",spec[0])
        attribute=re.split("</span>",attribute[1])
        value=re.findall("<a href="+".+"+"?</a>",attribute[0])
        for x in range (0,len(value)):
            url=re.split("\"",value[x])
            specLister("https://www.programmableweb.com"+url[1])
#On récupére la liste des attribut de chaque API
def specLister (path):
    global description
    global dict
    listNameSpec=[]
    listValues=[]
    last=0
    url=urllib.urlopen(path)
    page=url.read().decode('utf-8')
    listSpec = re.findall(r""+"<label>"+".+"+"</label>", page)
    name = re.findall("<div class=\"node-header\">"+".+"+"?</div>", page,re.DOTALL)
    if(name==[]):
        name="null"
    else:
        name = re.findall("<h1>"+".+"+"?</h1>", name[0])
        name=re.sub("<.*?>","",name[0])
        name=name.encode('ascii','ignore')
    dict2={}
    dict2[fieldnames[0]]=name
    dict[APIDone]=dict2
    description=re.findall("<div class=\"api_description tabs-header_description\""+".+"+"?</div>",page,re.DOTALL)
    if(description==[]):
        description="null"
    else:
        description=re.sub("<.*?>","",description[0])
        description=description.encode('ascii','ignore')
    #On accéde aux données a partir de la page
    for i in range (0,len(listSpec)-1):
        nameSpec = re.sub("<label>", "", listSpec[i])
        nameSpec = re.sub("</label>", "", nameSpec)
        nameSpec= nameSpec.encode('ascii','ignore')
        listNameSpec.append(nameSpec)
        listSpec[i]=re.escape(listSpec[i])
        spec=re.split(listSpec[i],page)
        spec=re.split(listSpec[i+1],spec[1])
        attribute=re.split("<span>",spec[0])
        attribute=re.split("</span>",attribute[1])
        value=re.sub("<.*?>","",attribute[0])
        value=re.sub("amp;","",value)
        value=re.sub("&lt;","<",value)
        value=re.sub("&gt;",">",value)
        value=value.encode('ascii','ignore')
        listValues.append(value)
        last=i
    if(last>0):
        nameSpec = re.sub("<label>", "", listSpec[last+1])
        nameSpec = re.sub("</label>", "", nameSpec)
        listNameSpec.append(nameSpec)
        listSpec[last+1]=re.escape(listSpec[last+1])
        spec=re.split(listSpec[last+1],page)
        spec=re.split("</div>",spec[1])
        attribute=re.findall(r""+"<span>"+".+"+"</span>",spec[0])
        value=re.sub("<.*?>","",attribute[0])
        value=str(value)
        listValues.append(value)
    csvWriter(listNameSpec,listValues)
#On crée les ligne du csv
def csvWriter(listNameSpec,listValues):
    global fieldnames
    global dict
    global description
    global APIDone
    dict2=dict[APIDone]
    for x in range(1,len(fieldnames)):
        defined=False
        for y in range(0,len(listNameSpec)):
            if(fieldnames[x]==listNameSpec[y]):
                dict2[fieldnames[x]]= listValues[y]
                defined=True
            elif(fieldnames[x]=="API Description"):
                description=str(description)
                dict2[fieldnames[x]]= description
                defined=True
        if not defined:
            dict2[fieldnames[x]]='null'
    APIDone=APIDone+1
    print APIDone
PageLister()
