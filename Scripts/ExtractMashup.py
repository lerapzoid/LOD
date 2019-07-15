import urllib
import re
import csv
APIDone=0
fieldnames=[]
description=""
dict={}
date=""
#On récupére la liste des paramétres des Mashup a partir de programmableweb
def specNameLister ():
    listName=[]
    last=0
    urlCount=0
    url=urllib.urlopen("https://www.programmableweb.com/add/mashup")
    page=url.read().decode('utf-8')
    listSpec = re.findall(r""+"<label"+".+"+"</label>", page)
    for i in range (0,len(listSpec)-1):
        nameSpec=re.sub("<.*?>","",listSpec[i])
        nameSpec=re.sub("&#039;","\'",nameSpec)
        nameSpec=re.sub(" \*","",nameSpec)
        #On supprime les éléments qui ne sont pas des champs
        if (nameSpec=="Web" or nameSpec=="Mobile" or nameSpec=="Desktop" or nameSpec=="Other"or nameSpec=="Weight for row 1"):
            last=i
        elif(nameSpec=="Leave this field blank"):
            break
        elif(nameSpec=="URL" and urlCount==0):
            listName.append(nameSpec)
            urlCount=1
        elif(nameSpec=="URL" and urlCount==1):
            last=i
        else:
            listName.append(nameSpec)
    listName.append("Submitted")
    return listName
#On parcours les page qui liste les Mashup et on écrit les données dans le csv
def PageLister():
    global fieldnames
    global dict
    page=urllib.urlopen('https://www.programmableweb.com/category/all/mashups')
    strpage=page.read().decode('utf-8')
    pagerLast=re.findall("<li class=\"pager-next\">"+".+"+"?</li>",strpage,re.DOTALL)
    countPage=re.sub("<.*?>","",pagerLast[0])
    countPage=int(countPage)
    with open('E:\\Fac\\Informatique\\Python\\txtFiles\\Mashup.csv', mode='ab') as csv_file:
        fieldnames=specNameLister()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #MashupLister('https://www.programmableweb.com/category/all/mashups')
        for x in range(159,countPage-1):
            path="https://www.programmableweb.com/category/all/mashups?page="+str(x)
            MashupLister(path)
            if(len(dict)>=100):
                print "Saving"
                compt=0
                for k, v in dict.items():
                    writer.writerow(v)
                    compt=compt+1
                    percent=(compt*100)/len(dict)
                    print percent," % done"
                dict={}
                print "Save done"
#On accéde a la page qui liste les information de chaque Mashup
def MashupLister(path):
    global date
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
        print splitHref[2]
        dict2[fieldnames[0]]=splitHref[2]
        date=re.sub("<.*?>","",listAttributeAPI[3])
        date=re.sub(" ","",date)
        date=re.sub("\n","",date)
        dict[APIDone]=dict2
        path="https://www.programmableweb.com"+splitHref[1]
        specLister(path)
#On récupére la liste des attribut de chaque Mashup
def specLister (path):
    global description
    global dict
    listNameSpec=[]
    listValues=[]
    last=0
    url=urllib.urlopen(path)
    page=url.read().decode('utf-8')
    listSpec = re.findall(r""+"<label>"+".+"+"</label>", page)
    """"name = re.findall("<div class=\"node-header\">"+".+"+"?</div>", page,re.DOTALL)
    if(name==[]):
        name="null"
    else:
        name = re.findall("<h1>"+".+"+"?</h1>", name[0])
        name=re.sub("<.*?>","",name[0])
        name=name.encode('ascii','ignore')
    dict2={}
    dict2[fieldnames[0]]=name
    dict[APIDone]=dict2"""
    description=re.findall("<div class=\"field-item even\""+".+"+"?</div>",page,re.DOTALL)
    if(description==[]):
        description="null"
    else:
        description=re.sub("<.*?>","",description[1])
        description=description.encode('ascii','ignore')
    #On accéde aux données a partir de la page
    for i in range (0,len(listSpec)-1):
        nameSpec = re.sub("<label>", "", listSpec[i])
        nameSpec = re.sub("</label>", "", nameSpec)
        nameSpec= nameSpec.encode('ascii','ignore')
        if(nameSpec=="Related APIs"):
            nameSpec="Related API "
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
        elif(nameSpec=="Categories"):
            secondary=""
            hasSecondary=False
            listNameSpec.append("Primary Category")
            listNameSpec.append("Secondary Category")
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
            value=re.split(",",value)
            for j in range(0,len(value)):
                if j==0:
                    listValues.append(value[j])
                elif(secondary==""):
                    secondary=value[j]
                    hasSecondary=True
                else:
                    secondary=secondary+","+value[j]
            if(hasSecondary):
                listValues.append(secondary)
            else:
                listValues.append("null")
        else:
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
    global date
    dict2=dict[APIDone]
    for x in range(1,len(fieldnames)-1):
        defined=False
        for y in range(0,len(listNameSpec)):
            if(fieldnames[x]==listNameSpec[y]):
                dict2[fieldnames[x]]= listValues[y]
                defined=True
            elif(fieldnames[x]=="Mashup Description"):
                description=str(description)
                dict2[fieldnames[x]]= description
                defined=True
        if not defined:
            dict2[fieldnames[x]]='null'
    dict2[fieldnames[len(fieldnames)-1]]=date
    APIDone=APIDone+1
    print APIDone
PageLister()