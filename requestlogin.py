# coding:utf-8
from bs4 import BeautifulSoup
import requests,time

def login(usrcode,password):
    session = requests.Session()
    header={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'}  
    loginurl='http://hqhr.efoxconn.com:999/HR/LoginForm.aspx'
    loginreq = session.get('http://hqhr.efoxconn.com:999/HR/LoginForm.aspx')
    loginHtml= loginreq.text
    soup=BeautifulSoup(loginHtml, 'html.parser')
    __VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
    logindata={
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
    loginResponse = session.post(url=loginurl, headers=header, data=logindata)
    
    signurl='http://hqhr.efoxconn.com:999/HR/PCM/PCMNetSignInOutEditForm.aspx?WorkNo='+usrcode+'&ModuleCode=PCMSYS13'
    signreq=session.get(signurl)
    signHtml= signreq.text

    soup=BeautifulSoup(signHtml, 'html.parser')
    __VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
    '''
    cookie={
    'ASP.NET_SessionId':session.cookies['ASP.NET_SessionId'],
    'CultureResource':'zh-tw',
    'ServerName':'E-HRM',
    'UserCode':'XXXXX'
    }
    '''
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
    signResponse = session.post(url=signurl, headers=header, data=signdata)

if __name__ == '__main__':
    sTime=time.strftime("%H:%M:%S", time.localtime())
    sDay=time.strftime("%A", time.localtime()) 
    if ((sTime>'07:30:01'and sTime<'07:59:01') or sTime>'17:30:01') \
       and (sDay!='Sunday'):
        login('XXXX','XXXX')