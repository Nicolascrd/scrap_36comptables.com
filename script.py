"""Lancer le programme avec la command python3 script.py en mettant le département slug correspondant dans la variable DEPARTEMENT
   Tous les departements sont disponibles dans le fichier departement.csv dans le même répertoire."""

# os for file management
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
import re
import subprocess


#départment a extraire
DEPARTEMENT = "nord"

#fonction pour renvoyer l'adresse mail dans une phrase
def get_email(chaine):
    liste = chaine.split(' ')
    for mot in liste:
        if '@' in mot:
            return mot
    return None


#fonction pour renvoyer le nom dans une phrase (entre les mots 'de' et 'est')
def get_name(chaine):
    liste = chaine.split(' ')
    for indice, mot in enumerate(liste):
        if(mot == 'de'):
            start = indice + 1
        if(mot == "est"):
            end = indice - 1
    return liste[start:end+1]


#ajoute dans un fichier repertoire.csv un élément
def add2csv(liste):
    f = open("repertoire.csv", "a")
    f.write(liste[0])
    f.write(',')
    f.write(liste[1])
    f.write(',')
    f.write(liste[2])
    f.write(',')
    f.write(liste[3])
    f.write('\n')
    f.close()
    return None

driver = webdriver.Firefox()

for j in range(1,9):
    try:
        url = 'https://36comptables.com/annuaire/' + DEPARTEMENT + '/' + str(j)
        driver.get(url)
    except:
        pass
    else:
        
        liste_pages = driver.find_elements_by_class_name('professional-name')
        startpoint = 240 #pour pas prendre les premiers cabinets qui sont pas des bonnes adresses.
        print(len(liste_pages))
        for i in range(startpoint, len(liste_pages)):
            driver.get(url)
            print('get url', url)
            secondes = time.time()
            #on enleve la banière de cookie
            print("tour start")
            try:
                print("try")
                cookie = driver.find_element_by_class_name("cookies-eu-ok")
                cookie.click()
            except:
                pass
            try:
                liste = driver.find_elements_by_class_name('professional-name')#on refait la liste à chaque fois mais on itère toujours
                elt = liste[i]
                elt.click()
                
            except:
                pass
            try:

                #a partir d'ici, on est dans la page d'un expert comptable.
                
                titre = driver.find_element_by_css_selector("h1")
                titre_text = titre.text
                titre_liste = titre_text.split(' ')
                ville = titre_liste[-1]
                pro_info = driver.find_element_by_class_name("professional")
                paragraphes = pro_info.find_elements_by_css_selector('p')
                para = paragraphes[5].text
                email = get_email(para)[:-1]
                name = get_name(para)
                print(name,email,ville)
                
            except:
                print('except n°2')
                pass
            else:
                print('else')
                if (len(name) == 2):
                    ligne = [name[1], name[0], email, ville]
                    add2csv(ligne)
                pass
                #et jusque ici   
            print(time.time()-secondes)       

driver.close()






    