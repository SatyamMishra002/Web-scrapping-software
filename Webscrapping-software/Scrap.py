# from concurrent.futures import ThreadPoolExecutor
import html
import time
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import requests
import wx
app1 = wx.App()
from insert_on_database import *
import database
import global_var
from selenium import webdriver
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wx.adv
import re
import sys
from insert_on_database import *
import requests
import os
from bs4 import BeautifulSoup

app=wx.App()

def print_exception_details(e):  
    exc_type, exc_obj, tb = sys.exc_info()
    lineno = tb.tb_lineno
    print(f'EXCEPTION: {e}\nLINE NO: {lineno}\nException Type: {exc_type}\n')
    time.sleep(5)


def make_html_doc(htmldoc3,domain):
    htmldoc3 = htmldoc3.get_attribute("outerHTML")
    htmldoc3 = htmldoc3.replace("&amp;", "&").replace("&nbsp;", " ").strip()
    htmldoc3 = htmldoc3.replace('\r','').replace('\n','').replace('\t','').strip()
    htmldoc3 = re.sub(r'\s+', ' ', htmldoc3)
    htmldoc3 = htmldoc3.replace('href="/','href="'+domain+'')
    htmldoc3 = htmldoc3.replace('src="/','src="'+domain+'')
    htmldoc3 = htmldoc3.replace(' </','</')
    htmldoc3 = htmldoc3.replace('> ','>')
    while 'data-href=' in htmldoc3:
        htmldoc3 = re.sub(r'data-href=', 'href=', htmldoc3)
    while "<form" in htmldoc3:
        remove = htmldoc3.partition('<form')[2].partition('</form>')[0]
        htmldoc3 = htmldoc3.replace('<form'+ remove +'</form>', '')
    while '<img' in htmldoc3:
        remove = htmldoc3.partition('<img')[2].partition('>')[0]
        htmldoc3 = htmldoc3.replace('<img'+ remove +'>','')   

    # soup = BeautifulSoup(htmldoc3, 'html.parser')
    # for input in soup.find_all('input'):
    #     input.decompose()
    # htmldoc3 = str(soup)

    return htmldoc3

    


def data_scraping(browser,Collection):  
    
    for data in Collection:
        browser.get(data["tender_link"])
        # browser.get('https://zakupki.rosatom.ru/2405231627181')
        a = True
        time.sleep(3)      
        
        while a == True:
            try:
                segField = []
                for i in range(50):
                    segField.append('')

                try:
                    html_source = browser.find_element(By.XPATH,'//*[@id="ProcessViewInfo"]')               
                    gethtmlsource  = make_html_doc(html_source,global_var.domain)
                except NoSuchElementException:
                    print("Skipping this data.")
                    break

                Maz_Org = 	gethtmlsource.partition('PROMOTOR')[2].partition('">')[0].partition('value="')[2].strip()
                Maz_Org = removeHTMLTags(Maz_Org).strip()

                Title = gethtmlsource.partition('OBJETO')[2].partition('</textarea>')[0].partition('">')[2].strip()
                Title = removeHTMLTags(Title).strip()

                email =  gethtmlsource.partition('E-MAIL PROMOTOR')[2].partition('">')[0].partition('value="')[2].strip()
                email = removeHTMLTags(email).strip()

                # location = gethtmlsource.partition('Место нахождения')[2].partition('</tr>')[0]
                # location = removeHTMLTags(location).strip()
                # mailing_add = gethtmlsource.partition('Почтовый адрес')[2].partition('</tr>')[0]
                # mailing_add = removeHTMLTags(mailing_add).strip()
                telephone =  gethtmlsource.partition('FONE PROMOTOR')[2].partition('">')[0].partition('value="')[2].strip()
                telephone = removeHTMLTags(telephone).strip()
                # fax = gethtmlsource.partition('Факс')[2].partition('</tr>')[0]
                # fax = removeHTMLTags(fax).strip()
                # contact_person = gethtmlsource.partition('Контактное лицо')[2].partition('</tr>')[0]
                # contact_person = removeHTMLTags(contact_person).strip()

                deadline_raw =  gethtmlsource.partition('FIM REC. PROPOSTA')[2].partition('">')[0].partition('value="')[2].strip()
                deadline_raw = removeHTMLTags(deadline_raw).strip()
                for date_format in ('%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M'):
                    try:
                        date_obj = datetime.strptime(deadline_raw, date_format)
                        break
                    except ValueError:
                        continue
                if date_obj:
                    # deadline_raw = date_obj.strftime('%m/%d/%Y')
                    deadline = date_obj.strftime('%Y-%m-%d')
                # deadline_raw = datetime.strptime(deadline_raw,'%m/%d/%Y %H:%M')
                # deadline = deadline_raw.strftime('%Y-%m-%d')

                Add = f'Brazil \n<br>[Disclaimer: For Exact Organization/Tendering Authority details, please refer the tender notice.], Phone: {telephone} '

                # purchaser = gethtmlsource.partition('Номер закупк')[2].partition('<tr>')[0]
                Amount =   gethtmlsource.partition('VALOR TOTAL DO PROCESSO')[2].partition('">')[0].partition('value="')[2].strip()
                Amount = removeHTMLTags(Amount).replace('.', '').replace(',','.').strip()
                Amount = re.sub(r"[^0-9.]", "", Amount).strip()

                tender_notice_no =   gethtmlsource.partition('Nº EDITAL')[2].partition('">')[0].partition('value="')[2].strip()
                tender_notice_no = removeHTMLTags(tender_notice_no).strip()     

                segField[1] = email
                segField[2] = Add
                segField[7] = global_var.country_code
                segField[12] =  Maz_Org
                segField[13] = tender_notice_no
                segField[18] = Title
                segField[19] = segField[18]
                segField[20] = Amount
                if str(segField[20]) != '':
                        segField[21] = 'BRL'
                segField[24] = deadline
                segField[27] = "0"
                segField[28] = browser.current_url
                segField[31] = global_var.source_name                
                segField[42] = segField[7]

                         
                # Doc_list = []
                # for Doc_details in browser.find_elements(By.XPATH,'//*[@id="table_04"]/table/tbody/tr'):
                #     second_a_element = Doc_details.find_elements(By.TAG_NAME, 'a')[1]
                #     Doc_link = second_a_element.get_attribute('href').strip()
                #     filename_extension = get_filename_from_url(Doc_link,segField)
                #     Doc_text = second_a_element.get_attribute('innerText').strip()
                #     Doc_text = str(Doc_text) + str(filename_extension)
                #     # Doc_link = Doc_link.partition('(')[2].partition(')')[0].strip()
                #     # Doc_links = Doc_link.replace(',','&tipo=').replace("'", '')
                #     full_link =  Doc_link
                #     Doc_list.append({'link_text' : Doc_text ,'link_href' : full_link})   
                
                # full_links = ''
                # # for lists in Doc_list:
                # #     if lists['link_href'] != '':
                # #         full_link = lists['link_text']+'~'+lists['link_href']+','
                # #         full_links += full_link
                # #         segField[44] = full_links.rstrip(',')


                # for lists in Doc_list:
                #     if lists['link_href'] != '':
                #         link_text = lists['link_text']  # Default assignment outside of the conditional block
                #         if '~' in link_text:
                #             link_text = link_text.replace('~', '')  # Remove '~' character from link text
                #         full_link = link_text + '~' + lists['link_href'] + ','
                #         full_links += full_link
                # segField[44] = full_links.rstrip(',')

                segField = validate_segfeild(segField)
  
                # check_date(segField,gethtmlsource)
                
                deadline = (segField[24])
                curdate = datetime.now()
                curdate_str = curdate.strftime("%Y-%m-%d")
                if deadline != '':
                    datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
                    datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
                    timedelta_obj = datetime_object_deadline - datetime_object_curdate
                    day = timedelta_obj.days
                    is_new = False
                    if day > 0:
                        is_new = check_Duplication(segField)
                        if is_new :
                            Fileid,Filename = create_html_file(segField,gethtmlsource)
                            
                            if segField[44] != '':
                                adddoc_Filename = AdditionalDocs(segField,Fileid)
                                # if adddoc_Filename != '':
                                segField[44] = adddoc_Filename
                                
                            insert_in_local(segField,Fileid)
                            insert_l2l_tbl(segField,Fileid,Filename)
                        else:
                            print('Duplicate Tender')
                            global_var.duplicate += 1    
                    else:
                        print("Expired Tender")
                        global_var.expired += 1
                else:
                    print("Deadline Not Given")
                    global_var.deadline_Not_given += 1
                
                a = False
                global_var.Total += 1
                print(" Total: " + str(global_var.Total) + " Duplicate: " + str(global_var.duplicate) + " Expired: " + str(global_var.expired) + " Skipped: " + str(global_var.skipped) + " Inserted: " + str(global_var.inserted) + " Deadline Not given: " + str(global_var.deadline_Not_given) + " QC Tenders: "+ str(global_var.QC_Tender),"\n")    
            
            except Exception as e:
                log_exception_details(e,str(segField[28])) 
                print_exception_details(e)
                a = True             
    
# def check_date(segField,gethtmlsource):     
#         deadline = (segField[24])
#         curdate = datetime.now()
#         curdate_str = curdate.strftime("%Y-%m-%d")
#         try:
#             if deadline != '':
#                 datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
#                 datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
#                 timedelta_obj = datetime_object_deadline - datetime_object_curdate
#                 day = timedelta_obj.days
#                 is_new = False
#                 if day > 0:
#                     is_new = check_Duplication(segField)
#                     if is_new :
#                         Fileid,Filename = create_html_file(segField,gethtmlsource)
                        
#                         if segField[44] != '':
#                             adddoc_Filename = AdditionalDocs(segField,Fileid)
#                             if adddoc_Filename != '':
#                                 segField[44] = adddoc_Filename
                            
#                         insert_in_local(segField,Fileid)
#                         insert_l2l_tbl(segField,Fileid,Filename,segField[31])
#                     else:
#                         print('Duplicate Tender')
#                         global_var.duplicate += 1    
#                 else:
#                     print("Expired Tender")
#                     global_var.expired += 1
#             else:
#                 print("Deadline Not Given")
#                 global_var.deadline_Not_given += 1
#         except Exception as e:
#             log_exception_details(e,str(segField[28])) 

# ChromeDriver()

def removeHTMLTags(text):
    pattern = re.compile(r'(<.*?>|<!--(.*?)-->)', re.DOTALL)
    text = re.sub(pattern, '', text)
    text = text.replace('\r','').replace('\n','').replace('\t','').strip()
    return text

def validate_segfeild(segField):
    for index, value in enumerate(segField):
         segField[index] = html.unescape(str(value)).strip()
        # segField[i] = segField[i].replace("'", "''")
    
    for index, value in enumerate(segField):
        if index == 44:
            continue 
        if len(value) > 1500:
            segField[index] = value[:1500] + "..."
        if value == "":
            segField[index] = ""
            
    if segField[18] == '':
        segField[18] = segField[19]
        
    if len(segField[19]) > 200:
        if segField[18] != segField[19]:
            segField[18] = segField[19]+'<br>\n'+segField[18]
        segField[19] = segField[19][:200].strip() + "..."
   
    if len(segField[2]) > 500:
        segField[2] = segField[2][:500].strip() + "..."

    return segField

def get_filename_from_url(url,segfield):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.head(url, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                # Extract filename from the Content-Disposition header
                filename = content_disposition.split('filename=')[-1].strip(' "')
                file_extension = os.path.splitext(filename)[1]
                return file_extension
                
            else:
                # If there's no Content-Disposition header, try to get the filename from the URL
                file_extension = os.path.splitext(url)[1]
                return file_extension
        else:
            return None
    except Exception as e:
        log_exception_details(e,str(segfield[28])) 
        print_exception_details(e)
        return None

            
# wx.MessageBox("All work done successfully...!!\n\nTotal: " + str(global_var.Total) + "\n""Inserted: " + str(global_var.inserted) + "\n""Duplicate: " + str(global_var.duplicate) + "\n""Expired: " + str(global_var.expired) + "\n""Skipped: " + str(global_var.skipped) + "\n""Deadline Not given: " + str(global_var.deadline_Not_given) + "\n""QC Tenders: "+ str(global_var.QC_Tender) + "",str(global_var.source_name), wx.OK | wx.ICON_INFORMATION)

            