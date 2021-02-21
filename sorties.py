import json

from fpdf import FPDF
from datetime import date

from rich.console import Console
from rich.table import Table
from Salarie import Salarie

console = Console()

DOSSIER = "ALLo"

class PDF(FPDF):

    def __init__(self):
        super().__init__(orientation='L',unit='mm',format='A4')
    
    def footer(self):
        self.set_y(-5)
        #self.set_text_color(50)
        self.set_font('Arial', 'B', 12)
        self.cell(40,0,"Date : " + str(date.today().strftime("%d/%m/%Y")),0,0,align="L")
        self.cell(210,0,f"{DOSSIER}",0,0,align="C")
        
        self.cell(30,0,'Page %s' % self.page_no() + '/{nb}',0,0,align="R")



def imprime_tableau():
    """Fonction qui génère le tableau graphique récapitulatif des salariés
    """
    #ON CREE L'ENTETE ET LE TITRE DU TABLEAU
    print("")
    table = Table(show_header=True, title_justify="center",header_style="bold black on white")
    
    #CREATION DU TABLEAU ET DES COLONNES D'EN TETE
    tableau = [("NOM",14),("PRENOM",14),("HEURES",9,"right"),("BRUT",10,"right"),("BR. ABAT",10,"right"),("FRAIS",10,"right"),("FIL. LOG",12,"right"),("FIL. CALC",12,"right"),("ECARTS",9,"right")]
    for elt in tableau:
        try:
            table.add_column(elt[0], style="dim", width=elt[1], justify=elt[2])
        except:
            table.add_column(elt[0], style="dim", width=elt[1])
    #AJOUT DES DONNEES POUR CHAQUE SALARIE
    for personne in Salarie.LISTE_SALARIES:
            
        
             
        ecart = round(sum(personne.reductions_logiciel)+personne.reduction_calculee,2)
               
        table.add_row(
            str(personne.nom), str(personne.prenom), 
            "%.2f" %round(sum(personne.heures),2) if sum(personne.heures) !=0 else "",
            "%.2f" %round(sum(personne.brut),2) if sum(personne.brut) !=0 else "",
            "%.2f" %round(sum(personne.brutabattu),2) if sum(personne.brutabattu) !=0 else "",
            "%.2f" %round(sum(personne.frais),2) if sum(personne.frais) !=0 else "",
            "%.2f" %round(sum(personne.reductions_logiciel),2) if sum(personne.reductions_logiciel) !=0 else "",
            "%.2f" %personne.reduction_calculee if personne.reduction_calculee !=0 else"",

            "%.2f" %ecart if ecart !=0 else "",
        )
    #ET ON AJOUTE LES TOTAUX
    table.add_row("")
    table.add_row("TOTAUX","",
    
        "%.2f" %Salarie.total_dossier()[0],
        "%.2f" %Salarie.total_dossier()[1],
        "%.2f" %Salarie.total_dossier()[2],
        "%.2f" %Salarie.total_dossier()[3],
        "%.2f" %Salarie.total_dossier()[4],
        "%.2f" %Salarie.total_dossier()[5],
        "%.2f" %(Salarie.total_dossier()[4] + Salarie.total_dossier()[5]),
    style="black on white")


    console.print(table)


 
def exporte_pdf(dossier="Dossie"):
    global DOSSIER
    DOSSIER = dossier
    #ON CREE LE FICHIER PDF
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    #ON DEFINI LE TITRE DU DOCUMENT
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255)
    pdf.set_fill_color(120)
    pdf.cell(280,10, "CONTROLE DES REDUCTIONS GENERALES DE COTISATIONS : " + str(Salarie.ANNEE), 1,1,"C", True)

    
    #ON DEFINIT LE TITRE DES COLONNES
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0)
    titre = [("NOM",55), ("PRENOM",55), ("HEURES",25),("BRUT",25), ("BRUT ABAT.",25),("FRAIS",25), ("LOGICIEL",25),("CALCULEE",25), ("ECART",20)]
    pdf.ln(5)
    for tit in titre:
        pdf.set_fill_color(170)
        pdf.cell(tit[1],10,tit[0],1,0,align="C",fill=True)
    pdf.ln()
    
    #POUR CHAQUE SALARIE ON AJOUTE UNE LIGNE
    for num, personne in enumerate(Salarie.LISTE_SALARIES):

        #ON PREVOIT DE NE METTRE QUE 20 SALARIES PAR PAGE    
        if num % 20 ==0 and num!=0:
            pdf.add_page()
            pdf.ln(1)
            for tit in titre:
                pdf.cell(tit[1],10,tit[0],1,0,align="C",fill=True)
            pdf.ln()
        
        pdf.cell(55,7,personne.nom,1)
        pdf.cell(55,7,personne.prenom,1)
        donnees = personne.get_salarie()
        
        for num,elt in enumerate(donnees):
            if num > 1:
                
                pdf.cell(titre[num][1],7,"%.2f" %elt,1,0,align="R") if elt !=0 else pdf.cell(titre[num][1],7,"",1,0,align="R")
                
        pdf.ln()

    pdf.ln(5)
    

    #ON FINI PAS AJOUTER LES TOTAUX
    donnees = Salarie.total_dossier()
    
    pdf.cell(110,10,"TOTAUX",1,0,align="C",fill=True)
    for chiffres in donnees:
        pdf.cell(25,10, "%.2f" %chiffres,1,0, align="R", fill=True)
    pdf.cell(20,10,"%.2f" %(donnees[4]+donnees[5]),1,0,align="R",fill=True)
    pdf.output("tuto.pdf","F")
    


def exporte_dictionnaire():
    """FONCTION SIMPLE DE MISE EN FORME DU DICTIONNAIRE CONTENANT LES SALARIES

    Returns:
        [Dict]: [Dictionnaire contenant les données salariés avec un numéro pour chaque salarié]
    """
    dictionnaire = {}
    dictionnaire_interne = {}
    for num, personne in enumerate(Salarie.LISTE_SALARIES):
        for cle, valeurs in personne.__dict__.items():
            if cle !="feuille":
                
                dictionnaire[cle]=getattr(personne, cle)
        dictionnaire_interne[num] = dictionnaire
        dictionnaire ={}

    
    return dictionnaire_interne
 

def exporte_json(fichier="salaries_json.json"):
    """Fonction pour exporter les données de chaque salarié dans un dictionnaire
    dont la clé et un numéro entier.

    Args:
        fichier (str, optional): [Nom du fichier json de destination]. Defaults to "salaries_json.json".
    """
    dico = exporte_dictionnaire()
    with open(fichier, "w") as write_file:
        for num, personne in enumerate(Salarie.LISTE_SALARIES):
            json.dump(dico[num], write_file, indent=3)
    
        