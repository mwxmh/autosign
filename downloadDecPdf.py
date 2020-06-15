# coding:utf-8
import requests,time,sys,datetime,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
reload(sys)
sys.setdefaultencoding('utf-8')

options = Options()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver_path="C:\chromedriver_win32\chromedriver.exe"
#driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver = webdriver.Chrome(driver_path)
page_url='https://swapp.singlewindow.cn/deskserver/sw/deskIndex?menu_id=dec001'
driver.get(page_url)
#20秒时间登录
time.sleep(20)
'''
with open('cookies.txt','w') as cookief:
    #将cookies保存为json格式
    cookief.write(json.dumps(driver.get_cookies()))
'''
#起始日期
begindate=(datetime.datetime.now() - datetime.timedelta(days = 6)).strftime("%Y-%m-%d")
#结束日期
enddate=time.strftime("%Y-%m-%d", time.localtime())
print begindate
print enddate
s = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
        s.cookies.set(cookie['name'],cookie['value'])
driver.close()
driver.quit()
#创建文件夹
pdf_path=begindate+'~'+enddate
if not os.path.exists(pdf_path):
    os.mkdir(pdf_path)
#登录后重新访问url        
resp = s.get(page_url)
for dclTrnRelFlag in ('2','0'):
    for ieFlag in ('I','E'):
        print ieFlag
        dec_url='https://swapp.singlewindow.cn/decserver/sw/dec/merge/cusQuery?limit=50&offset=0&stName=updateTime&stOrder=desc&decStatusInfo=%25257B%252522cusCiqNoHidden%252522%3A%252522%252522%2C%252522dclTrnRelFlagHidden%252522%3A%252522%252522%2C%252522transPreNoHidden%252522%3A%252522%252522%2C%252522cusOrgCode%252522%3A%252522%252522%2C%252522dclTrnRelFlag%252522%3A%252522'+dclTrnRelFlag+'%252522%2C%252522cusDecStatus%252522%3A%252522%252522%2C%252522etpsCategory%252522%3A%252522C%252522%2C%252522cusIEFlag%252522%3A%252522'+ieFlag+'%252522%2C%252522entryId%252522%3A%252522%252522%2C%252522cusCiqNo%252522%3A%252522%252522%2C%252522cnsnTradeCode%252522%3A%252522%252522%2C%252522billNo%252522%3A%252522%252522%2C%252522isBillNoExactQuery%252522%3A%2525220%252522%2C%252522customMaster%252522%3A%252522%252522%2C%252522tableFlag%252522%3A%2525221%252522%2C%252522updateTime%252522%3A%252522'+begindate+'%252522%2C%252522updateTimeEnd%252522%3A%252522'+enddate+'%252522%2C%252522operateDate%252522%3A%2525221%252522%2C%252522queryPage%252522%3A%252522cusBasicQuery%252522%2C%252522operType%252522%3A%2525220%252522%25257D&_=1591769129196'
        dec_Resp=s.get(dec_url)
        dec_Resp.encoding = 'utf-8'
        print dec_Resp.text
        json_str=dec_Resp.text
        jsonDecodestr=json.loads(json_str)
        total=jsonDecodestr.get('total')
        print ieFlag+'数量'+str(total)
        page_size=int(total)//50+1 #获取页码
        for page_num in range(0,page_size):
            dec_url_exten1='https://swapp.singlewindow.cn/decserver/sw/dec/merge/cusQuery?limit=50&offset='+str(page_num*50)+'&stName=updateTime&stOrder=desc&decStatusInfo=%25257B%252522cusCiqNoHidden%252522%3A%252522%252522%2C%252522dclTrnRelFlagHidden%252522%3A%252522%252522%2C%252522transPreNoHidden%252522%3A%252522%252522%2C%252522cusOrgCode%252522%3A%252522%252522%2C%252522dclTrnRelFlag%252522%3A%252522'+dclTrnRelFlag+'%252522%2C%252522cusDecStatus%252522%3A%252522%252522%2C%252522etpsCategory%252522%3A%252522C%252522%2C%252522cusIEFlag%252522%3A%252522'+ieFlag+'%252522%2C%252522entryId%252522%3A%252522%252522%2C%252522cusCiqNo%252522%3A%252522%252522%2C%252522cnsnTradeCode%252522%3A%252522%252522%2C%252522billNo%252522%3A%252522%252522%2C%252522isBillNoExactQuery%252522%3A%2525220%252522%2C%252522customMaster%252522%3A%252522%252522%2C%252522tableFlag%252522%3A%2525221%252522%2C%252522updateTime%252522%3A%252522'+begindate+'%252522%2C%252522updateTimeEnd%252522%3A%252522'+enddate+'%252522%2C%252522operateDate%252522%3A%2525221%252522%2C%252522queryPage%252522%3A%252522cusBasicQuery%252522%2C%252522operType%252522%3A%2525220%252522%25257D&_=1591769129196'
            dec_Resp_extend1=s.get(dec_url_exten1)
            dec_Resp_extend1.encoding = 'utf-8'
            json_str_extend1=dec_Resp_extend1.text
            analyz_str=json.loads(json_str_extend1)   
            list_row=analyz_str.get('rows')
            for i in range(len(list_row)):
                print list_row[i]["cusCiqNo"],list_row[i]["entryId"]
                if list_row[i]["entryId"]!=None:
                    download_addres='https://swapp.singlewindow.cn/decserver/entries/ftl/1/0/0/'+list_row[i]["cusCiqNo"]+'.pdf'
                    download_resp=s.get(download_addres)
                    with open(pdf_path+'\\'+list_row[i]["entryId"]+".pdf","wb") as f:
                        f.write(download_resp.content)




