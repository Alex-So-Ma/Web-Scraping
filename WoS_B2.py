from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

import os
import gzip
import shutil

uname=os.getlogin()

query=input  ('Escribe las etiquetas de los artículos a consultar:')

carp1 = 'Record_y_referencias'
newpath1 = 'C:\\Users\\{}\\Downloads\\{}'.format(uname,carp1)
if not os.path.exists(newpath1):
    os.makedirs(newpath1)

opt=Options()

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opt
)

driver.get('https://www.webofscience.com/wos/woscc/advanced-search')

while True:
    try:
        WebDriverWait(driver, 60)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@class,'ot-close-icon')]")))\
            .click()
        break
    except Exception:
        sleep(1)

WebDriverWait(driver, 60)\
        .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@class,'_pendo-close-guide')]")))\
        .click()

WebDriverWait(driver, 60)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="advancedSearchInputArea"]')))\
        .click()

elab = driver.find_element(By.XPATH, '//*[@id="advancedSearchInputArea"]').send_keys(query)

driver.switch_to.active_element.send_keys(Keys.ENTER)

while True:
    try:
        al = driver.find_element(By.XPATH, "//*[@class='brand-blue']").text
        break
    except Exception:
        sleep(1)

h=int(al.replace(',',''))

m= h//500
r= h%500

if r!=0:
    p=m+1
else:
    p=m

d=p-1

for k in range(p):
    if k!=d:
        m=500*k
        n=500*k
    else:
        m=500*k
        n=500*(k-1)+r

    driver.refresh()
    sleep(10)

    while True:
        try:
            WebDriverWait(driver, 180)\
                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-base-summary-component/div/div[2]/app-page-controls[1]/div/app-export-option/div/app-export-menu/div/button")))\
                .click()
            break
        except Exception:
            try:
                WebDriverWait(driver, 60)\
                    .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@class,'ot-close-icon')]")))\
                    .click()
            except Exception:
                try:
                    WebDriverWait(driver, 60)\
                        .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@class,'_pendo-close-guide')]")))\
                        .click()
                except Exception:
                    sleep(1)

    while True:
        try:
            WebDriverWait(driver, 180)\
                .until(EC.element_to_be_clickable((By.XPATH,"//*[text()=' Plain text file ']")))\
                .click()
            break
        except Exception:
            sleep(1)
            
    WebDriverWait(driver, 60)\
            .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="radio3"]')))\
            .click()
    
    WebDriverWait(driver, 60)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@name,'markFrom')]")))\
            .clear()

    driver.find_element(By.XPATH, "//*[contains(@name,'markFrom')]").send_keys('{}'.format(str(1+m)))

    WebDriverWait(driver, 180)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@name,'markTo')]")))\
            .clear()

    driver.find_element(By.XPATH, "//*[contains(@name,'markTo')]").send_keys('{}'.format(str(500+n)))

    WebDriverWait(driver, 180)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@class,'dropdown')]")))\
            .click()

    WebDriverWait(driver, 180)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='Full Record and Cited References']")))\
            .click()

    WebDriverWait(driver, 180)\
            .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='Export']")))\
            .click()

    while True:
        try:
            os.rename("C:\\Users\\{}\\Downloads\\savedrecs.txt".format(uname),
                      "C:\\Users\\{}\\Downloads\\archivos_{}_{}.txt".format(uname, carp1, str(1+m), str(500+n)))
            shutil.move("C:\\Users\\{}\\Downloads\\archivos_{}_{}.txt".format(uname, carp1, str(1+m), str(500+n)),
                        "C:\\Users\\{}\\Downloads\\{}\\archivos_{}_{}.txt".format(uname, carp1, str(1+m), str(500+n)))
            break
        except Exception:
            sleep(1)

driver.quit()
