# coding:utf-8
import urllib,cookielib
from bs4 import BeautifulSoup
import urllib2,time


def Main(usrcode,password):
    loginUrl="http://hqhr.efoxconn.com:999/HR/LoginForm.aspx" 
    headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'}
    Cookie = cookielib.CookieJar()    
    pageOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Cookie))
    loginPageRequest = urllib2.Request(loginUrl)
    loginPageHTML = pageOpener.open(loginPageRequest).read()
    soup=BeautifulSoup(loginPageHTML, 'html.parser')
    __VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
    formdata={
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__LASTFOCUS':'',
        '__VIEWSTATE':__VIEWSTATE,
        '__VIEWSTATEGENERATOR':'2AB8E0AD',
        'ddlLanguage':'zh-tw',
        'textBoxUserID':usrcode,
        'textBoxPassword':password,
        'ImageButtonLogin.x':'34',
        'ImageButtonLogin.y': '30',
        'DropDownListDB': 'E-HRM',  
        'txtValiCode': '123',
        'textBoxWorkNo':'' ,
        'textBoxIdentityNo':'' ,
    }
    loginData=urllib.urlencode(formdata)
    loginRequest = urllib2.Request(loginUrl , loginData , headers)
    loginResponse = pageOpener.open(loginRequest)
    '''
    for c in Cookie:
        if c.name=='UserCode':
            sUserCode=c.value
    '''                 
    #print {c.name:c.value for c in Cookie }
    
    signurl='http://hqhr.efoxconn.com:999/HR/PCM/PCMNetSignInOutEditForm.aspx?WorkNo='+usrcode+'&ModuleCode=PCMSYS13'
    mainPageRequest = urllib2.Request(signurl)
    mainPageHTML = pageOpener.open(mainPageRequest).read() 
    soup=BeautifulSoup(mainPageHTML, 'html.parser')
    __VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
    signdata={
        '__VIEWSTATE':__VIEWSTATE,
        '__VIEWSTATEGENERATOR':'C457B3BA',
        'HiddenSave':'' ,
        'textBoxEmployeeNo':usrcode,
        'textBoxName':'xxx',
        'textBoxDPcode':'xxx',
        'textBoxTime': 'xxx',
        'textBoxWeek': 'xxx',  
        'RadioButtonListkq':'Y' ,
        'ButtonSave':'存儲' 
    }
    
    Data=urllib.urlencode(signdata)
    signRequest=urllib2.Request(signurl , Data , headers) 
    signResponse=pageOpener.open(signRequest)
    #print signResponse.read()
    


if __name__ == '__main__':        
    sTime=time.strftime("%H:%M:%S", time.localtime())
    sDay=time.strftime("%A", time.localtime()) 
    if ((sTime>'07:30:01'and sTime<'07:59:01') or sTime>'17:30:01') \
       and (sDay!='Sunday'):     
       Main('XXXX','XXXX')               