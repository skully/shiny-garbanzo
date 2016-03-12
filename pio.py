import json, requests, os


def config():
    
    confDict = dict()
    try:
        print "Config file found!"
        with open(".config", "r") as confFile:
            for confLine in confFile:
                listOfConf = confLine.replace(" ", "").split(":",1)
                confDict.update({listOfConf[0]:listOfConf[1]})

    except IOError:
        print "No .config file! Let's make one!"
        confFile = open(".config", "w")

        oAuthToken = raw_input("OAuthToken: ")
        confFile.write("oauth: "+oAuthToken)
        confDict.update({"oauth":oAuthToken})

    confFile.close()
    
    return confDict

def correctConfig(key = "", *val):
    #key: value
    confDict = dict()
    
    confFile = open(".config", "w")
    confFile.write( key+": "+val[0])
    
    confDict.update({key:val[0]})

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

def uploadFile(oauth, filename):
    #Problem w/ the solution: loads the complete file into the memory, no feedback for the user
    #Look for other solution!
    payload = {'oauth_token':oauth}
    try:
        files = {'file':open(filename,'rb')}
        url = 'https://upload.put.io/v2/files/upload'
        
        result = requests.post(url, params=payload, files= files )

        parsed = json.loads(result.text)
        files['file'].close;
        return parsed
    except NameError:
        return None    


def getInfos(oauth,id):
    payload = {'oauth_token':oauth}
    result = requests.get("https://api.put.io/v2/files/"+ str(id) , params=payload)
    parsed = json.loads(result.text)
    if parsed['status'] ==  'OK':
        return parsed['file']
    else:
        return "ERR"

#return must be -1 or size of file
def downloadFile(oauth, id, path=".", feedbackfunc = None, *feedbackargs):
    payload = {'oauth_token':oauth}
    url = "https://api.put.io/v2/files/" + str(id) + "/download"

    try:
        local_file= getInfos(oauth, id)
    except requests.exceptions.ConnectionError:
        return -1
    #ha van mar ilyen nevu fajl, append id!

    
    if os.path.exists((path+"/"+local_file['name'])):
        local_filename = local_file['name'] +"_"+ str(id)
    else:
        local_filename = local_file['name'] 


    r= requests.get(url, params = payload,stream = True)
    with open((path+"/"+local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)
                f.flush()
                if feedbackfunc != None:
                    feedbackfunc(*feedbackargs)
                    print local_file
    return getInfos(oauth,id)['size']


def downloadFolder(oauth, id, path, folderfeedback = None, feedbackfunc = None, *feedbackargs):
    payload = {'oauth_token':oauth}
    fileList = getFileList(oauth, id)
    if not os.path.exists(path):
        os.mkdir(path)

    for item in fileList["files"]:         
       
        print item
        if item['content_type'] == 'application/x-directory': 
            print "folder"
            if not os.path.exists(path + '/' + item['name']):
                os.mkdir(path + '/' + item['name'])
            downloadFolder(oauth, item["id"], path + '/' + item['name'])
        else:
            print "file"
            b =  downloadFile(oauth, item['id'], path, feedbackfunc, feedbackargs)
            print b


    







