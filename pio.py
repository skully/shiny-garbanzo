import json, requests


def config():
    
    confDict = dict()
    try:
        print "Config file found!"
        with open(".config", "r") as confFile:
            for confLine in confFile:
                listOfConf = confLine.replace(" ", "").split(":",1)
                confDict.update({listOfConf[0]:listOfConf[1:]})

    except IOError:
        print "No .config file! Let's make one!"
        confFile = open(".config", "w")

        oAuthToken = raw_input("OAuthToken: ")
        confFile.write("oauth: "+oAuthToken)
        confDict.update({"oauth":oAuthToken})

    confFile.close()
    
    return confDict

def correctConfig():
        
    confDict = dict()
    #correct dict refresh

    #reparse

    return confDict;


def getFileList(oauth,id):
    payload = {'oauth_token':oauth}
    if id == 0:
        result = requests.get("https://api.put.io/v2/files/list", params=payload)
    else:
        payload.update({'parent_id': id})
        result = requests.get("https://api.put.io/v2/files/list", params=payload)
    parsed = json.loads(result.text)
    return parsed


def getTransferList(oauth):
    payload = {'oauth_token':oauth}
    result = requests.get("https://api.put.io/v2/transfers/list", params=payload)
    parsed = json.loads(result.text)
    return parsed





confDict = config()
print confDict



try:

    #answ = raw_input("mi kone ha vona: ")
    
    #parsed = getFileList(confDict["oauth"],0)   
    #print str(parsed['files']).replace(" u'"," \n'") 

    #attr = raw_input("id: ")
    #parsed = getFileList(attr)
    #print '\n'

    #print len(parsed['files'])
    print "wtf"

    parsed = getTransferList(confDict["oauth"])

    print str(parsed['transfers']).replace(" u'"," \n'") 
except KeyError:
    confDict = correctConfig()








