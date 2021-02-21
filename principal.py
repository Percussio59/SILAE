import xlrd
import os, sys

import sorties

from Salarie import Salarie


if len(sys.argv) == 0 or len(sys.argv)>2:

    print("Usage : Ce script nécessite le nom d'un fichier Excel (au format 97-2003) en argument")
    sys.exit()
else:
    try:
        classeur = xlrd.open_workbook(sys.argv[1])
        os.system("cls")
        for elt in classeur:
            elt = Salarie(elt)
    
        
    except:
        
        print("Quelque chose n'a pas fonctionné")
        print("Merci de vérifier le nom de votre fichier")
        print("Utilisation : principal.py monfichier.xls")
sorties.imprime_tableau()
sorties.exporte_pdf()
sorties.exporte_json()

