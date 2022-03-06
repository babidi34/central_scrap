import config
import fonctions
import sys

# fonction dynamically
name_fonction = "scrap_"+config.nom_site.replace("-","_")
function_current = getattr(fonctions,name_fonction)

data_list = function_current()
print(data_list)