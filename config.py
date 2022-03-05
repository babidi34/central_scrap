secteur_activites = "fournisseur_restaurant"
url = "http://www.offre-alimentaire-paca.fr/1-35253-Annuaire-Fournisseurs.php?showall=1&page="
nom_site = url.split('//')[1].replace("www.","").split('.')[0]
print(nom_site)