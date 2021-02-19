import xlrd
import os
import sorties

from Salarie import Salarie


classeur = xlrd.open_workbook("DRAPIER2021.xls")
os.system("cls")
for elt in classeur:
    elt = Salarie(elt)
    
sorties.imprime_tableau()


