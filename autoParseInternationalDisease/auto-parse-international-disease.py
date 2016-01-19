# coding: utf-8
# -*- coding: utf-8 -*-

# auto-parse-international-disease PYTHON v1.0.0 (2016/1/10)
# (c) 2016 Center for Disease Control, Taiwan
# EIC Jian-Kai Wang
# License: GNU GENERAL PUBLIC LICENSE

# ----------
import json
import urllib
import time
import os
import codecs
# ----------

# ----------
# get color of each disease (only used in summary)
diseaseDef = {\
            u'cls1':'cls1', \
            u'天花':'cls1', \
            u'嚴重急性呼吸道症候群':'cls1',\
            u'鼠疫':'cls1',\
            u'狂犬病':'cls1',\
            u'cls2':'cls2',\
            u'登革熱':'cls2',\
            u'德國麻疹':'cls2',\
            u'霍亂':'cls2',\
            u'流行性斑疹傷寒':'cls2',\
            u'白喉':'cls2',\
            u'流行性腦脊髓膜炎':'cls2',\
            u'西尼羅熱':'cls2',\
            u'傷寒':'cls2',\
            u'副傷寒':'cls2',\
            u'小兒麻痺症':'cls2',\
            u'急性無力肢體麻痺':'cls2',\
            u'桿菌性痢疾':'cls2',\
            u'阿米巴性痢疾':'cls2',\
            u'瘧疾':'cls2',\
            u'麻疹':'cls2',\
            u'急性病毒性Ａ型肝炎':'cls2',\
            u'Ａ型肝炎':'cls2',\
            u'腸道出血性大腸桿菌感染症':'cls2',\
            u'漢他病毒症候群':'cls2',\
            u'多重抗藥性結核病':'cls2',\
            u'屈公病':'cls2',\
            u'炭疽病':'cls2',\
            u'cls3':'cls3',\
            u'腸病毒感染併發重症':'cls3',\
            u'腸病毒':'cls3',\
            u'結核病':'cls3',\
            u'人類免疫缺乏病毒感染':'cls3',\
            u'漢生病':'cls3',\
            u'百日咳':'cls3',\
            u'新生兒破傷風':'cls3',\
            u'破傷風':'cls3',\
            u'急性病毒性B型肝炎':'cls3',\
            u'急性病毒性C型肝炎':'cls3',\
            u'急性病毒性D型肝炎':'cls3',\
            u'急性病毒性E型肝炎':'cls3',\
            u'流行性腮腺炎':'cls3',\
            u'腮腺炎':'cls3',\
            u'梅毒':'cls3',\
            u'淋病':'cls3',\
            u'侵襲性ｂ型嗜血桿菌感染症':'cls3',\
            u'退伍軍人病':'cls3',\
            u'先天性德國麻疹症候群':'cls3',\
            u'日本腦炎':'cls3',\
            u'cls4':'cls4',\
            u'流感併發重症':'cls4',\
            u'肉毒桿菌中毒':'cls4',\
            u'庫賈氏病':'cls4',\
            u'鉤端螺旋體病':'cls4',\
            u'萊姆病':'cls4',\
            u'類鼻疽':'cls4',\
            u'地方性斑疹傷寒':'cls4',\
            u'Ｑ熱':'cls4',\
            u'水痘併發症':'cls4',\
            u'恙蟲病':'cls4',\
            u'兔熱病':'cls4',\
            u'侵襲性肺炎鏈球菌感染症':'cls4',\
            u'疱疹B病毒感染症':'cls4',\
            u'弓形蟲感染症':'cls4',\
            u'布氏桿菌病':'cls4',\
            u'cls5':'cls5',\
            u'新型A型流感':'cls5',\
            u'中東呼吸症候群冠狀病毒感染症':'cls5',\
            u'黃熱病':'cls5',\
            u'伊波拉病毒感染':'cls5',\
            u'拉薩熱':'cls5',\
            u'馬堡病毒出血熱':'cls5',\
            u'裂谷熱':'cls5'}

classColor = {'single':'rgba(237,28,36,1)',\
            'other':'rgba(63,72,204,1)',\
            'cls1':'rgba(0,162,232,1)',\
            'cls2':'rgba(34,177,76,1)',\
            'cls3':'rgba(255,242,0,1)',\
            'cls4':'rgba(225,127,39,1)',\
            'cls5':'rgba(237,28,36,1)'}

def getColor(getDisease):
    if getDisease in diseaseDef.keys():
        return classColor[diseaseDef[getDisease]]
    elif getDisease in classColor.keys():
        return classColor[getDisease]
    else:
        return classColor['other']
# ----------

# ----------
# global data
# for azure path
azurePath = 'D:/home/site/wwwroot/'
developPath = ''
usedPath = developPath

# save the file whose date peroid
datePeroid = []

# world health map-config-setting.json default information
# the only one and update the content on each fetching json data
whmConfigSettingPath = usedPath + 'configJson/whm-config-setting.json'
whmConfigSettingJson = [\
                            {\
                            "initial-disease":"summary",\
                            "initial-date":"20160107",\
                            "initial-source":"cdctw",\
                            "initial-color":"rgba(217,27,36,1)",\
                            "initial-disItem":"20160107"\
                            }\
                        ]
                        
# world health map-selection-item.json and default information
whmSelItemPath = usedPath + 'selJson/whm-sel-item.json'
whmSelitemJson = [\
                    {\
                   	"id":"search-select-source",\
                   	#"cdctw":"CDC Taiwan"\
                    },\
                    {\
                   	"id":"search-select-date",\
                   	#"20160107":"2015/12/14-2016/01/07"\
                    }\
                ]
                
# world health map-selection.json and default information
# update in each time
whmSelDisPath = usedPath + 'selJson/'
whmSelDisJson = [\
                    {\
                        "id":"search-select-disease",\
                        "summary":u"疫情總覽"\
                        #"dengue":"Dengue Fever"\
                    }\
                ]\

# save all json, including summary and each disease
jsonDataPath = usedPath + 'dataJson/'
# save all json object
jsonData = {}

# total alert counts
ttlAlerts = 0

# total country { isoName : object, isoName2 : object2, ... }
countryList = {}

# total disease {disName : [iosName1,iosName2,...], disName2 : [iosName1,iosName2, ...]
diseaseList = {}

# current date
currentDate = time.strftime("%Y%m%d")
# ----------

# ----------
# parse json from url (update every day)
# option 1: download first (location/format : originJson/dwn-{date}.json); 
#           including Utf-s decoding without BOM
# option 2: use Url
def parseJson(option,getUrl):    
    global jsonData, currentDate
    
    if option == 1:
        # method.1
        # due to Json file being downloaded as a file, must use urlretrieve() first
        # must notice the downloaded date, maybe is the previous day due to source updating time
        downloadJsonName = usedPath + "originJson/dwn-" + currentDate + ".json"
        decodeJsonData = ''
        
        # if the file exist, the json file would not be downloaded
        if(not os.path.isfile(downloadJsonName)):
            getJsonFromInternational = getUrl
            urllib.urlretrieve(getJsonFromInternational,downloadJsonName)
            
        # change Json file into the one without BOM
        fin = open(downloadJsonName,"r")
        fread = fin.read()
        fin.close()
        decodeJsonData = fread.decode("utf-8-sig")
        # decode string into json array
        jsonData = json.loads(decodeJsonData)

    elif option == 2:
        # method.2 directly download json from Url
        loadJson = urllib.urlopen(getUrl)
        preJsonData = loadJson.read()
        
        # decode string into json array
        jsonData = json.loads(preJsonData)
        
# use data must be (jsonData[0]["senderName"] == u"疾病管制署")
parseJson(1,'http://www.cdc.gov.tw/ExportOpenData.aspx?Type=json&FromWeb=1')
ttlAlerts = len(jsonData)
# ----------

# ----------
# start to fetch the date peroid
def dateFormat(option,getDate):
    dateList = getDate.split(u"T")
    combineDate = (dateList[0]).split(u"-")
    # format 20160110
    if option == 1:
        return combineDate[0] + combineDate[1] + combineDate[2]
    # format 2016/01/10
    elif option == 2:
        return combineDate[0] + "/" + combineDate[1] + "/" + combineDate[2]
    # format 2016-01-10
    elif option == 3:
        return combineDate[0] + "-" + combineDate[1] + "-" + combineDate[2]

# sort time to prevent sequential date error
allDateList = []
for i in range(0,ttlAlerts,1):
    if jsonData[i][u"effective"] not in allDateList:
        allDateList.append(jsonData[i][u"effective"])
sorted(allDateList)
fetchDate = [allDateList[0],allDateList[len(allDateList)-1]]
# ----------

# ----------
# edit whm-config-setting.json
whmConfigSettingJson[0][u'initial-disease'] = 'summary'
whmConfigSettingJson[0][u'initial-source'] = 'cdctw'
#whmConfigSettingJson[0][u'initial-date'] = dateFormat(1,fetchDate[1])
whmConfigSettingJson[0][u'initial-date'] = currentDate
whmConfigSettingJson[0][u'initial-color'] = getColor('single')
#whmConfigSettingJson[0][u'initial-disItem'] = dateFormat(1,fetchDate[1])
whmConfigSettingJson[0][u'initial-disItem'] = currentDate

# write out json file
with codecs.open(whmConfigSettingPath,"w","utf-8") as fout:
    # ensure_ascii == True, then output as ascii code
    fout.write(json.dumps(whmConfigSettingJson, ensure_ascii=False))
# ----------

# ----------
# define a piece of news
class singleAlert:
    __effective = ''
    __expire = ''
    __disease = ''
    __description = ''
    __web = ''
    __security_level = ''
    
    def __init__(self):
        self.__effective = ''
        self.__expire = ''
        self.__disease = ''
        self.__description = ''
        self.__web = ''
        self.__securityLevel = ''
        
    def setAlert(self, getEffDate, getExpDate, getDis, getDes, getWeb, getSL):
        self.__effective = getEffDate
        self.__expire = getExpDate
        self.__disease = getDis
        self.__description = getDes
        self.__web = getWeb
        self.__securityLevel = getSL
        
    
    def getEffDate(self):
        return self.__effective
    
    def getExpDate(self):
        return self.__expire
        
    def getDis(self):
        return self.__disease
    
    def getDes(self):
        return self.__description
    
    def getWeb(self):
        return self.__web
    
    def getSL(self):
        return self.__securityLevel
# ----------

# ----------                
# define a country
getDisIndex = []   # return alert indexes of the same disease names

class singleCountry():
    global singleAlert, getDisIndex
    
    __countryCode = ''
    __countryChineseName = ''
    __countryEnglishName = ''
    __alertCount = 0
    __alertList = []
    
    def __init__(self):
        self.__countryCode = ''
        self.__countryChineseName = ''
        self.__countryEnglishName = ''
        self.__alertCount = 0
        self.__alertList = []    
    
    def setCountry(self, getCode, getChName, getEnName):
        self.__countryCode = getCode
        self.__countryChineseName = getChName
        self.__countryEnglishName = getEnName
    
    def addAlert(self, getSingleAlert):
        self.__alertList.append(getSingleAlert)
        self.__alertCount += 1
    
    def getCountryCode(self):
        return self.__countryCode
    
    def getCountryChName(self):
        return self.__countryChineseName
        
    def getCountryEnName(self):
        return self.__countryEnglishName
    
    def getAlertCount(self):
        return self.__alertCount
    
    def getAlertList(self):
        return self.__alertList

    def getDisArray(self, getDisName):
        global getDisIndex
        
        # initialization
        getDisIndex = []
        
        for i in range(0,self.__alertCount,1):
            if (self.__alertList[i]).getDis() == getDisName:
                getDisIndex.append(i)

        return getDisIndex
# ----------

# ----------
# start to parse each alert
effDate = ''
expDate = ''
disName = ''
disDes = ''
webUrl = ''
secLevel = ''
# maybe more than 1 country
conChName = []
conEnName = []
isoNameCode = []
# check data integrity list
dataIntegrityList = [u'effective',u'expires',u'headline',\
                u'areaDesc',u'areaDesc_EN',u'ISO3166',\
                u'description',u'web',u'severity_level']

# disease must be only 1
def sepHeadLine(getName):
    sepCnDis = getName.split(u'\u2500')   # '─'
    return sepCnDis[1]
    
# make sure data is not "None" type    
def checkNonetype(getData):
    if getData == None:
        return True
    return False

for i in range(0,ttlAlerts,1):
    # confirm data integrity
    dataIntegrity = 1
    
    for checkListIndex in dataIntegrityList:
        if checkNonetype(jsonData[i][checkListIndex]):
            dataIntegrity = 0        

    # data integrity is not well due to missing value or NA
    if dataIntegrity == 0:
        continue       

    effDate = dateFormat(3,jsonData[i][u'effective'])
    expDate = dateFormat(3,jsonData[i][u'expires']) 
    disName = sepHeadLine(jsonData[i][u'headline'])
    disDes = jsonData[i][u'description']
    webUrl = jsonData[i][u'web']
    secLevel = jsonData[i][u'severity_level']
    # initialization
    conChName = (jsonData[i][u'areaDesc']).split(u',')
    conEnName = (jsonData[i][u'areaDesc_EN']).split(u',')
    isoNameCode = (jsonData[i][u'ISO3166']).split(u',')
    
    #if i == 11:
    #    with codecs.open("text.txt","w","utf-8") as fout:
    #        # ensure_ascii == True, then output as ascii code
    #        fout.write(effDate + "\t" + disDes + "\n")
    #        fout.write(conChName[0] + "\t" + conEnName[0] + "\t" + isoNameCode[0])
    
    # create a alert object
    newAlert = singleAlert()
    newAlert.setAlert(effDate,expDate,disName,disDes,webUrl,secLevel)

    # use iso code to save country information
    # may be more than 1 country
    for isoCodeIndex in range(0,len(isoNameCode),1):
        if isoNameCode[isoCodeIndex] not in countryList.keys():
            # create a country object and add into the countryList
            newCountry = singleCountry()
            newCountry.setCountry(isoNameCode[isoCodeIndex],conChName[isoCodeIndex],conEnName[isoCodeIndex])
            countryList.setdefault(isoNameCode[isoCodeIndex],newCountry)
        # each country has the same alert
        countryList[isoNameCode[isoCodeIndex]].addAlert(newAlert)
    
    # add disease objects, countries are unique in the list
    if disName not in diseaseList.keys():
        # create a new disease object
        diseaseList.setdefault(disName,[])
        
    # add all countries into the diease list
    for isoCodeIndex in range(0,len(isoNameCode),1):
        if isoNameCode[isoCodeIndex] not in diseaseList[disName]:
            diseaseList[disName].append(isoNameCode[isoCodeIndex])
# ----------

# ----------
# write out disease selection json file
#whmSelDisPath = whmSelDisPath + 'cdctw_' + dateFormat(1,fetchDate[1]) + '_selection.json'
whmSelDisPath = whmSelDisPath + 'cdctw_' + currentDate + '_selection.json'
for disItem in diseaseList.keys():
    if disItem not in whmSelDisJson[0]:
        whmSelDisJson[0].setdefault(disItem,disItem)

# write out json file
with codecs.open(whmSelDisPath,"w","utf-8") as fout:
    # ensure_ascii == True, then output as ascii code
    fout.write(json.dumps(whmSelDisJson, ensure_ascii=False))        
# ----------

# ----------
# start to append the selection list
decodePreviousSelectionJsonData = ''
previousSelectionJsonData = ''

# check whether the first time to create the file
if(not os.path.isfile(whmSelItemPath)):
    previousSelectionJsonData = whmSelitemJson
    previousSelectionJsonData[0].setdefault("cdctw","CDC Taiwan")
    #previousSelectionJsonData[1].setdefault(dateFormat(1,fetchDate[0]),dateFormat(2,fetchDate[0]) + "-" + dateFormat(2,fetchDate[1]))
    previousSelectionJsonData[1].setdefault(currentDate,dateFormat(2,fetchDate[0]) + "-" + dateFormat(2,fetchDate[1]))
else:        
    fin = open(whmSelItemPath,"r")
    fread = fin.read()
    fin.close()
    decodePreviousSelectionJsonData = fread.decode("utf-8-sig")
    # decode string into json array
    previousSelectionJsonData = json.loads(decodePreviousSelectionJsonData)
    # update in every day
    #if dateFormat(1,fetchDate[1]) not in (previousSelectionJsonData[1]).keys():
        #previousSelectionJsonData[1].setdefault(dateFormat(1,fetchDate[1]),dateFormat(2,fetchDate[0]) + "-" + dateFormat(2,fetchDate[1]))
    if currentDate not in (previousSelectionJsonData[1]).keys():
        previousSelectionJsonData[1].setdefault(currentDate,dateFormat(2,fetchDate[0]) + "-" + dateFormat(2,fetchDate[1]))

# write out json file
with codecs.open(whmSelItemPath,"w","utf-8") as fout:
    # ensure_ascii == True, then output as ascii code
    fout.write(json.dumps(previousSelectionJsonData, ensure_ascii=False))  
# ----------

# ----------
# define security level with its color
def securityColor(getLevel):
    if getLevel == u'第一級:注意(Watch)':
        return 'rgba(237,28,36,1)'
    elif getLevel == u'第二級:警示(Alert)':
        return 'rgba(136,0,21,1)'
    elif getLevel == u'第三級:警告(Warning)':
        return 'rgba(130,57,130,1)'
    else:
        return 'rgba(255,127,39,1)'

# return security level according to the information
def securityLevel(getSecLevel):
    if getSecLevel == u'第一級:注意(Watch)':
        return 1
    elif getSecLevel == u'第二級:警示(Alert)':
        return 2
    elif getSecLevel == u'第三級:警告(Warning)':
        return 3
    else:
        return -1

# return security information according to the level                
def getSecurityLevel(getSecLevel):
    if getSecLevel == 1:
        return u'第一級:注意(Watch)'
    elif getSecLevel == 2:
        return u'第二級:警示(Alert)'
    elif getSecLevel == 3:
        return u'第三級:警告(Warning)'
    else:
        return 'None'
# ----------

# ----------
# start to write out single disease and its information
singleDisCountry = []
singleDisInformation = {}
getSingleDisAlertList = []
necessaryInformation = ''
curSecLevel = -2
# new line by counting words
wordCount = 50
for disNameIndex in diseaseList.keys():
    # initialization
    singleDisCountry = []
    for cunIndex in diseaseList[disNameIndex]:
        # initialization
        singleDisInformation = {}
        getSingleDisAlertList = []
        necessaryInformation = ''
        curSecLevel = -2
        # set country code
        singleDisInformation.setdefault(u"code",cunIndex)
        # set z value (not used in single disease)
        singleDisInformation.setdefault(u"z",1)
        # set country name
        singleDisInformation.setdefault(u'Country', (countryList[cunIndex]).getCountryEnName() + u'(' + (countryList[cunIndex]).getCountryChName() + u')')
        # get alert index of each disease, the same disease but different information
        # e.g. cities, date, security levels, etc.
        getSingleDisAlertList = (countryList[cunIndex]).getDisArray(disNameIndex)
        # start to fetch detail information
        for alertIndex in range(0,len(getSingleDisAlertList),1):
            if alertIndex != 0:
                necessaryInformation = necessaryInformation + u'<br>----------<br>'
            # get alert object
            getCurrentAlert = (((countryList[cunIndex]).getAlertList())[getSingleDisAlertList[alertIndex]])
            # save disease effective date and expires date
            necessaryInformation = necessaryInformation + dateFormat(2,getCurrentAlert.getEffDate()) + u'-' + dateFormat(2,getCurrentAlert.getExpDate()) + u'<br>'
            necessaryInformation = necessaryInformation + u'<br>'
            for i in range(0,len(getCurrentAlert.getDes())/wordCount,1):
                necessaryInformation = necessaryInformation + getCurrentAlert.getDes()[i*wordCount: i*wordCount+wordCount] + u'<br>'
            necessaryInformation = necessaryInformation + getCurrentAlert.getDes()[(len(getCurrentAlert.getDes())/wordCount)*wordCount:len(getCurrentAlert.getDes())] + u'<br>'
                
            #necessaryInformation = necessaryInformation + u'Disease Description : ' + getCurrentAlert.getDes() + u'<br>'
            #necessaryInformation = necessaryInformation + u'Web information : ' + getCurrentAlert.getWeb() + u'<br>'
            if getCurrentAlert.getSL() != None:
                necessaryInformation = necessaryInformation + getCurrentAlert.getSL() + u'<br><br>'
            else:
                necessaryInformation = necessaryInformation + u'<br><br>'
            if securityLevel(getCurrentAlert.getSL()) > curSecLevel:
                curSecLevel = securityLevel(getCurrentAlert.getSL()) 
        # set the description
        singleDisInformation.setdefault("description",necessaryInformation)        
        # set color for the country
        singleDisInformation.setdefault("color",securityColor(getSecurityLevel(curSecLevel)))
        # save into butter for further output as json data
        singleDisCountry.append(singleDisInformation)
    
    # check the directory (folder) existing
    #if not os.path.exists('dataJson/' + dateFormat(1,fetchDate[1])):
        #os.makedirs('dataJson/' + dateFormat(1,fetchDate[1]))
    if not os.path.exists(jsonDataPath + currentDate):        
        os.makedirs(jsonDataPath + currentDate)
    
    # write out the json data for each disease
    #jsonDataFile = 'dataJson/' + dateFormat(1,fetchDate[1]) + '/' + 'cdctw_' + dateFormat(1,fetchDate[1]) + '_' + disNameIndex + '.json'
    jsonDataFile = jsonDataPath + currentDate + '/' + 'cdctw_' + currentDate + '_' + disNameIndex + '.json'
    # write out json file
    with codecs.open(jsonDataFile,"w","utf-8") as fout:
        # ensure_ascii == True, then output as ascii code
        fout.write(json.dumps(singleDisCountry, ensure_ascii=False)) 
# ----------

# ----------
# start to write out summary json for all countries
summaryCunList = []
countryInformation = {}
countryDescription = ''
highSecLevel = -2
allalertList = []
for cunIndex in countryList.keys():
    # initialization
    countryInformation = {}
    countryDescription = ''
    highSecLevel = -2
    allalertList = []
    # save country code
    countryInformation.setdefault(u"code",cunIndex)
    # save country name
    countryInformation.setdefault(u"Country",(countryList[cunIndex]).getCountryEnName() + u'(' + (countryList[cunIndex]).getCountryChName() + u')')
    # save z value
    countryInformation.setdefault(u"z",(countryList[cunIndex]).getAlertCount())
    # get all alerts
    countryDescription = u'疫情描述 : <br>'
    # temporarily count total alerts
    tempCountAlerts = 0
    # temporarily save the disease and its highest security level, {dis1 : dis1 highest security level, ...}
    tempSaveDisAlerts = {}
    allalertList = (countryList[cunIndex]).getAlertList()
    for alertIndex in range(0,len(allalertList),1):
        # format.1 (Complete) : effective date-expire date, disease, security level
        #countryDescription = countryDescription + u'Peroid : ' + dateFormat(2,(allalertList[alertIndex]).getEffDate()) + u'-' + dateFormat(2,(allalertList[alertIndex]).getExpDate())
        #countryDescription = countryDescription + u', ' + (allalertList[alertIndex]).getDis()
        #if (allalertList[alertIndex]).getSL() == None:
            #countryDescription = countryDescription + u'<br>'
        #else:
            #countryDescription = countryDescription + u' ,' + (allalertList[alertIndex]).getSL() + u'<br>'
            
        # format.2 (Simplied)
        if (allalertList[alertIndex]).getDis() in tempSaveDisAlerts.keys():
            if securityLevel((allalertList[alertIndex]).getSL()) > tempSaveDisAlerts[(allalertList[alertIndex]).getDis()]:
                tempSaveDisAlerts[(allalertList[alertIndex]).getDis()] = securityLevel((allalertList[alertIndex]).getSL())
        else:
            tempSaveDisAlerts.setdefault((allalertList[alertIndex]).getDis(),securityLevel((allalertList[alertIndex]).getSL()))
   
        # check the color of each disease            
        if securityLevel((allalertList[alertIndex]).getSL()) > highSecLevel:
            highSecLevel = securityLevel((allalertList[alertIndex]).getSL())

    # format.2 continue to save description
    tempGetAlerts = tempSaveDisAlerts.keys()
    for allAlertKey in tempGetAlerts:
        if tempCountAlerts == 0:
            tempCountAlerts = tempCountAlerts + 1
        else:
            countryDescription = countryDescription + u',<br>'
        countryDescription = countryDescription + allAlertKey
        
        # if the alert is None, skip it
        if tempSaveDisAlerts[allAlertKey] != -1:
            countryDescription = countryDescription + u'(' + getSecurityLevel(tempSaveDisAlerts[allAlertKey]) + u') ' 

    # save description
    countryInformation.setdefault(u"description",countryDescription)
    # save color
    countryInformation.setdefault(u"color",securityColor(getSecurityLevel(highSecLevel)))
    # save into json data
    summaryCunList.append(countryInformation)
    
    # check the directory (folder) existing
    #if not os.path.exists('dataJson/' + dateFormat(1,fetchDate[1])):
        #os.makedirs('dataJson/' + dateFormat(1,fetchDate[1]))
    if not os.path.exists(jsonDataPath + currentDate):
        os.makedirs(jsonDataPath + currentDate)        
    
    # write out the json data for each disease
    #jsonSummaryFile = 'dataJson/' + dateFormat(1,fetchDate[1]) + '/' + 'cdctw_' + dateFormat(1,fetchDate[1]) + '_summary.json'
    jsonSummaryFile = jsonDataPath + currentDate + '/' + 'cdctw_' + currentDate + '_summary.json'
    # write out json file
    with codecs.open(jsonSummaryFile,"w","utf-8") as fout:
        # ensure_ascii == True, then output as ascii code
        fout.write(json.dumps(summaryCunList, ensure_ascii=False)) 
# ----------













