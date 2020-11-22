import os
import sys
import datetime 
import json
import requests
import re

cintIndent = 2
__location__ = ""

def getHassIOStates():
    #curl -X GET -H "Authorization: Bearer xxx
    x = {}

    url = "http://192.168.1.10:8123/api/states"
    header= {
        "Authorization": "Bearer xxx",
        "Content-Type": "application/json"
    }

    page = requests.get(url, headers =header)
    if page.status_code == 200:
        x= json.loads(page.content.decode("utf-8"))
    else:
        #raise Exception('Error API Hassio','issue cwith API call')
        x={}
    return x

def buildBagForJinja(todo, states):

    for task in todo:
        pattern = todo[task]
        p = re.compile(pattern)
        mylist = [x for x in states if p.match(x["entity_id"] + " ")]
        if len(mylist) > 0:
            todo[task] = mylist

    return todo


def processFile(location,filenamein, fileout, prefix = "", intblock = 0, intsublock = 0, j={},g={}, jinja = True):

    filein = open(os.path.join(location,filenamein) ,"r")
    text = filein.read()
    filein.close()

    if jinja:
        lines = replaceLogic(text,j,g).split("\n")
    else:
        lines = text.split("\n")

    if lines[-1]== "":
        lines = lines[:-1]

    #Check for END
    blnKeep = True
    sublines = []
    for line in lines:
        if line[0:3] == "END":
            blnKeep = False
        if blnKeep:
            sublines.append (line)
    lines = sublines

    #Cleaning to only keep one of the underlying block
    if intblock > 0:
        currentblock = 0
        sublines = []
        for line in lines:
            if len(line)==0:
                line = " "
            if line[0] == "-":
                currentblock +=1
            if currentblock == intblock and (line [0] == "-" or line [0] == " "):
                sublines.append(line)
        lines = sublines

    if intsublock > 0:
        currentblock = 0
        sublines = []
        for line in lines:
            line = line[cintIndent:]
            if len(line)==0:
                line = " "
            if line[0] == "-":
                currentblock +=1
            if currentblock == intsublock and (line [0] == "-" or line [0] == " "):
                sublines.append(line)
        lines = sublines

    output = ""
    for line in lines:
        if "#include" in line:
            #Flush before recursion
            fileout.write(output)
            output = ""

            remainingline,command = line.split("#include")
            recursionfile,nj = parseCommand(command.replace("\n",""))

            x = nj['#block'].split(",")
            intblock = int(x[0])
            intsublock = int(x[1])
            jinja4child = nj["#jinja"]

            if '#indent' in j:
                processFile(location, recursionfile.strip(),fileout, prefix[-2*j['#indent']:] + remainingline, intblock,intsublock,nj,g,jinja4child)            
            else:
                processFile(location, recursionfile.strip(),fileout, prefix + remainingline, intblock,intsublock,nj,g,jinja4child)            
        else:
            #if jinja:
            #    proceesedline = replaceLogic(line,j)
            #else:

            if not '#indent' in j:
                processedline = line
            else:
                processedline = line[-2*j['#indent']:]
                
            output += prefix + processedline
            #fileout.write(prefix + proceesedline)

            if len(line) == 0 :
                output += ('\n')
                #fileout.write('\n')
            else:
                if line[-1] != '\n':
                    output += ('\n')
                    #fileout.write('\n')

    fileout.write(output)
    output = ""

def replaceLogic(line,j,g):
    #for key in j:
    #    line = line.replace(key,j[key])
    #return line
    try:
        from jinja2 import Template
        tm = Template(line)
        newtm = tm.render(j=j, g=g) + '\n'
        return newtm
    except: 
        return line

def parseCommand(command):
    # xxxx.yaml,{'#block': '1,1', 'v1': 145, 'v2': 'abc'}
    mylist = command.split(",",1)
    file = mylist[0]
    if len(mylist) == 1:
        mylist.append('{"#block": "0,0"}')
    j = json.loads(mylist[1])
    if "#block" not in j:
        j["#block"] = "0"
    j["#block"] = j["#block"] + ",0,0\n"

    if not "#jinja" in j:
        j["#jinja"] = True
    else:
        j["#jinja"]= (j["#jinja"] == "True")
    
    if not "#indent" in j:
        j["#indent"] = 0
    return file,j

def main(location, inputfile, outputfull):
    
    print("-" * 80)
    print("location  : " + location)
    print("inputfile : " + inputfile)
    print("outputfull: " + outputfull)
    print("-"*80)

    mylocation = os.path.dirname(__file__)

    with open(os.path.join(mylocation,"g.json")) as f:
        todo = json.load(f)

    states = getHassIOStates()
    g = buildBagForJinja(todo,states)

    fileout = open(outputfull,"w")
    processFile(location,inputfile,fileout, g=g)
    fileout.close()

    filein = open(outputfull ,"r")
    lines = filein.readlines()
    filein.close()
    now = datetime.datetime.now()

    fulltext = "".join(lines)
    #pyperclip.copy(fulltext)
    print("lines     : " + str(len(lines)))
    print("Bytes     : " + str(len(fulltext)))
    print("Timestamp : " + now.strftime('%Y-%m-%d %H:%M:%S'))
    print("-"*80)

if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        location = os.path.dirname(__file__)
        inputfile ="input.yaml"
        outputfull = os.path.join(location,"output.yaml")
    else:
        location = os.path.dirname(sys.argv[1])
        inputfile =os.path.basename(sys.argv[1])
        outputfull = sys.argv[2]

    ##FOR DEBUGGING WHEN NEEDED
    if 1==2:
        location="y:\\development\\Hass.io\\config\\tools\\yamllovelace"
        inputfile= "main.yaml" 
        outputfull = "y:\\development\\Hass.io\\config\\auto_lovelace-production.yaml" #"d:\\test.yaml"

    main(location,inputfile , outputfull)