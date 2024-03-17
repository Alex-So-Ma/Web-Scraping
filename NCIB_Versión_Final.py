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

#Obtiene el nombre del usuario del sistema
uname=os.getlogin()

#Crea una carpeta en la carpeta de descargas donde va poner los archivos con los genómas
carp1 = 'genoma'
newpath1 = 'C:\\Users\\{}\\Downloads\\{}'.format(uname,carp1)
if not os.path.exists(newpath1):
    os.makedirs(newpath1)

#Crea una carpeta en la carpeta de descargas donde va poner los archivos con la información de las proteínas
carp2 = 'proteina'
newpath2 = 'C:\\Users\\{}\\Downloads\\{}'.format(uname,carp2)
if not os.path.exists(newpath2):
    os.makedirs(newpath2)

#Activa el modo headless
opt=Options()
opt.add_argument("--headless")
prefs = {
    "profile.default_content_settings.popups": 0,
    "download.prompt_for_download": False,
    "download.directory_upgrade ": True,
    'download.default_directory': 'C:\\Users\\{}\\Downloads'.format(uname),
}
opt.add_experimental_option('prefs', prefs)

#Selecciona Google Chrome como el navegador a utilizar y obtiene el driver de la librería webdriver_manager
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opt
)

#Le pide al usuario la url de la página del ncib de donde se va a sacar los datos 
url=input  ('Seleccionana en la página del ncib (https://www.ncbi.nlm.nih.gov/datasets/genome/) \n\
            los taxones y filtros que requieras, copia y pega completa la url resultante aquí:')
driver.get(url)

sleep(5)

#Obtiene de la página la cantidad de cepas h
try:
    al = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div[3]/div/div[1]/section[3]/div/div[3]/div").get_attribute("aria-label")
except Exception:
    WebDriverWait(driver, 3600)\
        .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
        .click()
    al = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/section[3]/div[2]/div[1]/section[3]/div/div[3]/div').get_attribute("aria-label")
h=int(al.replace('Showing 1 to 20 of ','').replace(',',''))

m= h//20 #En la página aparecen de 20 en 20 cepas, m es el número de veces que se tiene que cambiar las cepas que se muestran
r= h%20 #r nos dice si el número de cepas es multiplo de 20, caso contrario debe haber un último cambio en las cepas que se muestran

#Este if hace el cambio mencionado en el comentario de r
if r!=0:
    p=m+1
else:
    p=m

d=p-1 #d sirve para saber donde dejar de hacer cambios para que no haya un error

j=0 #j es el número de cepas sin los archivod requeridos

for k in range(p): #Va cambiando las cepa que se muestran
    if k!=d:
        n=20
    else:
        n=r
    for i in range(n): #De las cepas que se muestran, revisar y descargar los archivos que se encuentren
        while True: #Si la página tarda mucho en cargar va a actualizar la página
            try:
                try:#Evita un error debido a una ventana emergente de una encuesta
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/main/div/div/div[3]/div/div[2]/div/div[2]/div/table/tbody/tr[{}]/td[12]/button'.format(str(i+1)))))\
                        .click()
                except Exception:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
                        .click()
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/main/div/section[3]/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr[{}]/td[12]/button'.format(str(i+1)))))\
                        .click()

                try:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH, "//*[text()='View details']")))\
                        .click()
                except Exception:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
                        .click()
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH, "//*[text()='View details']")))\
                        .click()
                WebDriverWait(driver, 180).until(EC.number_of_windows_to_be(2))
                break
            except Exception:
                driver.refresh()
                
        driver.switch_to.window(driver.window_handles[-1])#Cambia a la pestaña que abre lo anterior

        while True: #Este while True tiene la misma función que el anterior, pero busca algo diferente en la pestaña que se abrió
            try:
                try:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="show-link-menu-button"]')))\
                        .click()
                except Exception:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
                        .click()
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="show-link-menu-button"]')))\
                        .click()

                try:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.LINK_TEXT, "See more files on FTP")))\
                        .click()
                except Exception:
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
                        .click()
                    WebDriverWait(driver, 180)\
                        .until(EC.element_to_be_clickable((By.LINK_TEXT, "See more files on FTP")))\
                        .click()
                break
            except Exception:
                driver.refresh()
        
        try:#Busca los archivos deseados 

            st=0

            WebDriverWait(driver, 30)\
                .until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "_cds_from_genomic.fna.gz")))\
                .click()
            file_1 = driver.find_element(By.PARTIAL_LINK_TEXT, "_cds_from_genomic.fna.gz")
            
            st+=1

            WebDriverWait(driver, 30)\
                .until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "_protein.faa.gz")))\
                .click()
            file_2 = driver.find_element(By.PARTIAL_LINK_TEXT, "_protein.faa.gz")

            st+=1

        except Exception: #Si no los encuentra aumenta j e imprime la cepa que no los tiene
            j+=1
            print('Falta un archivo. No se descarga en'+ driver.title)

        while True:#Este while True esta hecho para que no salte un error si los archivos tardan mucho en descargarse
            try:#Si encontró los archivos, los descomprime y los llevas a la carpeta correspondiente
                if st!=0:
                    with gzip.open("C:\\Users\\{}\\Downloads\\{}".format(uname, file_1.text), 'rt') as f_in:
                        with open("C:\\Users\\{}\\Downloads\\{}\\{}".format(uname, carp1, file_1.text.replace('.gz','')), 'wt') as f_out:
                            shutil.copyfileobj(f_in, f_out)

                    if st==2:
                        with gzip.open("C:\\Users\\{}\\Downloads\\{}".format(uname, file_2.text), 'rt') as f_in:
                            with open("C:\\Users\\{}\\Downloads\\{}\\{}".format(uname, carp2, file_2.text.replace('.gz','')), 'wt') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                break
            except Exception:
                sleep(1)

        driver.close()#Cierra la pestaña con los archivos de la cepa actual
        driver.switch_to.window(driver.window_handles[0])#Cambia el driver a la pestaña con la lista de cepas
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)#Cierra cualquier menú que haya quedado abierto
    if k!=d:#Si no es la última lista de cepas cambia a las siguientes
        try:
            WebDriverWait(driver, 120)\
                .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/main/div/div/div[3]/div/div[1]/section[3]/div/div[4]/button[2]')))\
                .click()
        except Exception:
            WebDriverWait(driver, 120)\
                .until(EC.element_to_be_clickable((By.XPATH,"//*[text()='No Thanks']")))\
                .click()
            WebDriverWait(driver, 120)\
                .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/main/div/div/div[3]/div/div[1]/section[3]/div/div[4]/button[2]')))\
                .click()
    sleep(5)
driver.quit()
print(j,'cepas que no tienen los archivos deseados')
