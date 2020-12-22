# coding:utf-8
import requests,sys,os,json,time
from selenium import webdriver
from tkinter import *
from tkinter import messagebox


def main():
    Tk().geometry('0x0+999999+0')
    driver_path="C:\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    page_url='https://swapp.singlewindow.cn/sasserver/sw/ems/pub/applyQueryList?sysId=Z7&ngBasePath=https%3A%2F%2Fswapp.singlewindow.cn%3A443%2Fsasserver%2F'
    driver.get(page_url)
    #20秒时间登录
    time.sleep(20)    
    try:
        session = requests.Session()        
        content=driver.page_source
        #获取当前IC卡号
        tmp="var cards='"        
        iCardNo=content[content.index(tmp)+11:content.index(tmp)+24]
        print(iCardNo)
        #获取法人编码
        tmp="var cus_reg_no='"
        corpCode=content[content.index(tmp)+16:content.index(tmp)+26]
        print(corpCode)       
        if  is_number(iCardNo):            
            #获取cookie
            cookies = driver.get_cookies()
            #print(driver.find_element_by_xpath("//div[@id='fw']/div[@id='fwdiv']/div[@class='xwd']/div/div/p[0]").text)
            for cookie in cookies:
                session.cookies.set(cookie['name'],cookie['value'])
                
            list=os.listdir("D:/uplsas")
            if list!=None and len(list)!=0:
                for item in list:
                    preNo=item.split('.')[0]
                    time.sleep(2)
                    seqNo=getSeqNo(preNo,driver,corpCode)
                    uploadData(session,preNo,seqNo,iCardNo)
                    #os.remove("D:/uplsas/"+item)   
                messagebox.showinfo("提示","上传成功")
            else:
               messagebox.showerror("错误","未放置对应的pdf")     
        else:
            messagebox.showerror("错误","IC卡号获取失败")        
               
    except Exception as e:
        messagebox.showerror("错误","上传失败"+str(e))
    finally:
        driver.close()
        driver.quit()

#获取统一编号# 
def getSeqNo(preNo,driver,corpCode):
    try:
        driver.find_element_by_id("selTradeCode").send_keys(corpCode)
        driver.find_element_by_id("etpsInnerInvtNo").send_keys(preNo)
        driver.find_element_by_id("btn-search").click()
        driver.find_element_by_id("etpsInnerInvtNo").clear()
        driver.switch_to.default_content()
        table=driver.find_element_by_id("queryTalbe")
        tbody=table.find_element_by_tag_name("tbody")
        seqNo=tbody.find_elements_by_tag_name("tr")[0].find_elements_by_tag_name("td")[1].text
        print(seqNo)            
    except Exception as e:
        seqNo=None           
    return seqNo
#判断是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass 
    return False    

#上传
def uploadData(session,preNo,seqNo,iCardNo):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    # 代理
    proxy = "10.206.22.155:808"
    proxies = {
    "http": proxy,
    "https": proxy,
    }

    uploadUrl='https://swapp.singlewindow.cn/sasserver/sw/ems/pub/acmp/sasAcmpRLSaveService'
    uplpayLoad='{"blsNo":\"'+seqNo+'\","blsType":"6","chgTmsCnt":"0","sasAcmpRLList":[{"acmpFormSeqNo":"1","acmpFormFileNm":\"'+preNo+'.pdf","acmpBlsStatus":"8","acmpBlsStatusname":"待上传","modfMarkCd":"3","blsType":"6","blsTypename":"业务申报表","blsNo":\"'+seqNo+'\","icCardNo":\"'+iCardNo+'\","chgTmsCnt":"0","acmpFormFmt":"2","acmpFormFmtname":"非结构化","rmk":"D:\\uplsas\\'+preNo+'.pdf"}]}'
    print(uplpayLoad)
    uplpayLoad=uplpayLoad.replace('\\','\\\\')
    json_uplpayload=json.loads(uplpayLoad)
    print(type(json_uplpayload))
    response=session.post(url=uploadUrl,json=json_uplpayload,headers=headers)

if __name__ == '__main__':
        main()    




