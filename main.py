import config
import fonctions

data_paca = fonctions.scrap_offre_alimentaire_paca()
fonctions.createCsv(data_paca)