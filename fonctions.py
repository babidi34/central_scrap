import os
import config
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def createDirectory(secteur_activites):
    path = f"data/{secteur_activites}"
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print(f"Directory {path} is created")
    return path

def createCsv(strinlist):
    path = createDirectory(config.secteur_activites)
    path_csv = f"{path}/{config.nom_site}.csv"
    new_csv = open(path_csv,"w")
    for ligne in strinlist:
        new_csv.write(f"{ligne}\n")
    print(f"File {path_csv} is created")

def scrap_offre_alimentaire_paca():
    headers = { 'User-Agent': UserAgent().random }
    liste_data = list()
    for i in range(1,3):
        url = "http://www.offre-alimentaire-paca.fr/1-35253-Annuaire-Fournisseurs.php?showall=1&page=" 
        url = url + str(i)
        response = requests.get(url,headers=headers)
        parser = BeautifulSoup(response.content, 'html.parser') 
        body = parser.body
        fiches = body.find_all("div",{"class":"fond-annuaire"})
        for i in fiches:
            nom_entreprise = i.h3.text
            adresse_full = i.find("div",{"class":"adresse"}).text
            adresse = adresse_full.split('Tél')[0]
            tel = ""
            if "Tél" in adresse_full:
                tel = adresse_full.split('Tél')[1]
                tel = tel.split(':')[1].replace("Fax","")
            responsable = i.find("div",{"class":"contact_commercial"}).text.split(":")[1]
            mail = i.find("div",{"class":"contact_mail"}).a['href'].split(":")[1]
            contact_web = i.find("div",{"class":"contact_web"})
            site = ""
            if hasattr(contact_web,'a'):
                site = contact_web.a['href']
            type_entreprise = i.find("div",{"class":"type_entreprise"}).text.split(":")[1]
            activites = i.find("div",{"class":"activites"}).text.split(":")[1]
            liste_data.append(f"{nom_entreprise};{adresse};{tel};\
                {responsable};{mail};{site};{type_entreprise};{activites}")
    return liste_data

def scrap_rungisinternational():
    liste_data = ["nom entreprise;adresse;tel;mail;site web"]
    html = open("html_dir/rungisinternational.html","r")
    content = html.read()
    parser = BeautifulSoup(content, 'html.parser')
    body = parser.body
    grid = body.find_all("section",{"class":"grid-3 item"})
    for entreprise in grid:
        nom = entreprise.section.h1.text.strip()
        adresse = entreprise.find("section",{"class":"address"}).text.strip()
        tel = ""
        try:
            tel = entreprise.find("section",{"class":"tel"}).find("span",{"class":"tel"}).text.strip()
        except:
            pass
        mail_full = entreprise.find("span",{"class":"mail"})
        mail = ""
        if hasattr(mail_full,'a'):
            mail = mail_full.a['href']
            mail = mail.split(":")[1].strip()
        site_full = entreprise.find("span",{"class":"www"})
        site_web = ""
        if hasattr(site_full,'a'):
            site_web = site_full.a['href'].strip()
        liste_data.append(f"{nom};{adresse};{tel};{mail};{site_web}")
    return liste_data
