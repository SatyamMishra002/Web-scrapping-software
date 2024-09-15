# from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import global_var
import sys, os
import ctypes
import wx 
import gzip
import json
import database
from datetime import date, datetime, timedelta
import global_var
from selenium import webdriver
from insert_on_database import *
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wx.adv
import re
from Scrap import *


app = wx.App()
def print_exception_details(e):
    exc_type, exc_obj, tb = sys.exc_info()
    lineno = tb.tb_lineno
    print(f'EXCEPTION: {e}\nLINE NO: {lineno}\nException Type: {exc_type}\n')
    time.sleep(5)  # Sleep for 5 seconds before retrying

            
def Chromedriver():
    chrome_service = ChromeService('C:\\Translation EXE\\chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    browser.maximize_window()
    browser.get("https://bllcompras.com/Process/ProcessSearchPublic?param1=1")

    time.sleep(3)
    
    navigatinglink(browser)

def navigatinglink(browser):
    Collection = []
    count = 1
    a = True
    while a:
        try:
            rows = browser.find_elements(By.XPATH, '//*[@id="tableProcessDataBody"]/tr')
            for _ in range(1, len(rows)):
                if count > len(rows):
                    break
                time.sleep(1)
                tender_link = browser.find_element(By.XPATH,'//*[@id="tableProcessDataBody"]/tr['+str(count)+']/td[1]/a')
                tender_link1 = tender_link.get_attribute("href").strip()

                publish_Date = browser.find_element(By.XPATH,'//*[@id="tableProcessDataBody"]/tr['+str(count)+']/td[7]')
                publish_Date = publish_Date.get_attribute("innerText")
                date_obj = None
                for date_format in ('%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M'):
                    try:
                        date_obj = datetime.strptime(publish_Date, date_format)
                        break
                    except ValueError:
                        continue
                if date_obj:
                    publish_Date = date_obj.strftime('%m/%d/%Y')
                    publish_Date = datetime.strptime(publish_Date, '%m/%d/%Y')     

                try:
                    if publish_Date != '':
                        date = publish_Date
                        selected_date = datetime.strptime(global_var.fromdate, '%d/%m/%Y') # from date from main calendar
                        timedelta = date - selected_date # how many days remaining 
                        day = timedelta.days
                        if day >= 0:
                            Collection.append({"tender_link" : tender_link1, "publish_Date" : publish_Date}) 
                            print(f" {len(Collection)} link Inserted ")
                            count += 1
                                            
                            # if len(Collection) == 1:
                            #     data_scraping(browser,Collection)
                            #     a=False
                            #     break
                        else:
                            a = False
                            break
                except Exception as e :
                    print_exception_details(e)      
        except Exception as e:
            print("problem in collecting link", print_exception_details(e))   

        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except NoSuchElementException:
            print_exception_details(e)  
    data_scraping(browser,Collection)        
    
    wx.MessageBox(f'Total: {global_var.Total}\nDeadline Not given: {global_var.deadline_Not_given}\nSkipped: {global_var.skipped}\nduplicate: {global_var.duplicate}\ninserted: {global_var.inserted}\nexpired: {global_var.expired}\nQC Tenders: {global_var.QC_Tender}',global_var.source_name, wx.OK | wx.ICON_INFORMATION)
    browser.close()
    sys.exit()

Chromedriver()