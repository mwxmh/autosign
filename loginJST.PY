# coding:utf-8
from bs4 import BeautifulSoup
import requests,time,sys
import pytesseract
import cv2 as cv
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    session = requests.Session()    
    header={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'}  
    loginurl='http://xxxxx:8888/checkLogin'
    logindata={
        'userId': 'xxxx',
        'password': '1',
        'code': 'XYQ1'       
    } 
    while True:
        codeUrl='http://xxxx:8888/code/getCode'##验证码
        valcode = session.get(codeUrl)
        temp = open("C:\\valcode.png","wb") ##保存验证码图片
        temp.write(valcode.content)
        temp.close()
        #valc = input("输入验证码：")    
        image=Image.open("C:\\valcode.png")
        valc = pytesseract.image_to_string(image)    
        logindata["code"]=str(valc) 
        loginResponse = session.post(url=loginurl, headers=header, data=logindata)
        loginHtml=loginResponse.text
        if("导航" in loginHtml ):
            #print loginResponse.text 
            break
    queryUrl='http://xxxxxx:8888/logined/base/getCorpCodeList'
    queryRes=session.get(queryUrl)
    print queryRes.text        
                

if __name__ == '__main__':
    main()