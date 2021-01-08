# coding:utf-8
import requests,sys,os,json,time,cx_Oracle
from selenium import webdriver
from tkinter import *
from tkinter import messagebox
from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import


def main():
    driver_path="C:\chromedriver_win32\chromedriver.exe"
    msg=None       
    try:
        driver = webdriver.Chrome(driver_path)
        page_url='https://swapp.singlewindow.cn/sasserver/sw/ems/pub/bwlQueryList?sysId=Z7&ngBasePath=https%3A%2F%2Fswapp.singlewindow.cn%3A443%2Fsasserver%2F'
        driver.get(page_url)
        #20秒时间登录
        time.sleep(20) 
        session = requests.Session()        
        content=driver.page_source
        #获取法人编码
        tmp="var cus_reg_no='"
        corpCode=content[content.index(tmp)+16:content.index(tmp)+26]
        print('corpCode:'+corpCode)  
        #获取cookie
        cookies = driver.get_cookies()
        for cookie in cookies:
            session.cookies.set(cookie['name'],cookie['value'])        
        list=Query(corpCode)
        for item in list:
            driver.find_element_by_id("selTradeCode").send_keys(corpCode)
            driver.find_element_by_id("bwlNo").send_keys(item[1])
            driver.find_element_by_id("inputDateStart").clear()
            driver.find_element_by_id("inputDateEnd").clear()
            driver.find_element_by_id("btn-search").click()
            time.sleep(2)
            checkboxs = driver.find_elements_by_xpath("//input[@type='checkbox']")    
            checkboxs[0].click()
            driver.find_element_by_id("bwlQuertyDetailBtn").click()
            time.sleep(5)
            try:
                driver.find_element_by_xpath("//a[@href='#bwlBillInfo']").click()
            except Exception as e:
                messagebox.showinfo("提示","完毕!")
                break
            
            driver.find_element_by_id("querycopGNo").send_keys(item[2])    #料号
            print(item[2])
            if item[0]==None:
                backward(driver)    
                continue
            driver.find_element_by_id("queryinvtNo").send_keys(item[0])    #核注清单号 
            driver.find_element_by_id("queryinvtGNo").send_keys(item[3])   #归并项次
            driver.find_element_by_id("quickQueryBillBtn").click()
            driver.switch_to.default_content()
            time.sleep(3)
            try:
                gdsSeqNo=driver.find_element_by_xpath("//*[@id='bwlBillInfoTalbe']/tbody/tr/td[2]").text
            except Exception as e:
                backward(driver)
                continue  
            print(gdsSeqNo)
            driver.find_element_by_id("querycopGNo").clear()
            driver.find_element_by_id("queryinvtNo").clear()
            driver.find_element_by_id("queryinvtGNo").clear()
            msg=callWsdl(corpCode,item[4],item[1],gdsSeqNo,item[2],item[3])
            if msg!=None:
                messagebox.showerror("错误",msg)
                break
            else:
                backward(driver)             
               
    except Exception as e:
        messagebox.showerror("错误",str(e))
    finally:
        driver.close()
        driver.quit()

def Query(corpCode):
    ora = cx_Oracle.connect('webcus/Ecusweb200@10.134.7.84:1521/csedbslh')
    cursor = ora.cursor()    
    try:
        qSql="select wzo01,wzo09 from wzo_file where wzo08='"+corpCode+"'"
        cursor.execute(qSql)
        plants=cursor.fetchall()
        wx=plants[0][0]
        sb=plants[0][1]
        qSql="select UNIQUE INVT_NO,bsh02,BSI14,BSI25,bsh01 from "+sb+".bsh_file ,"+sb+".bsi_file \
        where bsh01=bsi01 and bsipno is null and invt_dcl_time between (sysdate-7) and sysdate \
        and is_invt='Y' AND BSH00='0' AND LIST_STAT between 9 and 43  \
        union \
        select UNIQUE INVT_NO,bsh02,BSI14,BSI25,bsh01 from "+wx+".bsh_file ,"+wx+".bsi_file \
        where bsh01=bsi01 and (bsi03 is null or bsi03=0) and invt_dcl_time between (sysdate-7) and sysdate \
        and is_invt='Y' AND BSH00='0' AND LIST_STAT between 9 and 43"
        cursor.execute(qSql)
        list=cursor.fetchall()
        print(list)
        return list
    except Exception as e:
        print(str(e))
    finally:
        cursor.close()
        ora.close()

def callWsdl(corpCode,preNo,emsNo,gdsSeqNo,bsi14,bsi25):
    try:
        url='http://xxx/EcusWebService.asmx?wsdl' 
        imp = Import('http://www.w3.org/2001/XMLSchema',location='http://www.w3.org/2001/XMLSchema.xsd')
        imp.filter.add('http://tempuri.org/')        
        client= Client(url,doctor = ImportDoctor(imp))
        msg=client.service.updateGold2bwl(corpCode,preNo,emsNo,gdsSeqNo,bsi14,bsi25)
        print (msg)         
    except Exception as e:
        msg=bsi14+' 回写失败:'+str(e)
    return msg

def backward(driver):    
    driver.execute_script("window.history.go(-1)")
    driver.find_element_by_id("selTradeCode").clear()
    driver.find_element_by_id("bwlNo").clear()     

if __name__ == '__main__':
        #main()
        Query('4101630001')
        #callWsdl('4101630001','7HJ-B10001','T4612D000006','5415','0808031-0041168','6')    




