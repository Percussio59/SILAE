from fpdf import FPDF

from rich.console import Console
from rich.table import Table
from Salarie import Salarie

console = Console()



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


    

    

        



def exporte_pdf():
    for personne in Salarie.LISTE_SALARIES:
        print(personne)


    pdf = FPDF('L','mm','A4')
    pdf.add_page()
    pdf.set_font("Arial","B", 12)
    pdf.cell(190,10, "CONTROLE DES REDUCTIONS GENERALES DE COTISATIONS", 1,0,"C")


    titre = [("NOM",30), ("PRENOM",30), ("HEURES",25),("BRUT",25), ("BRUT ABAT.",25),("FRAIS",25), ("LOGICIEL",30),("CALCULEE",30), ("ECART",30)]
    pdf.set_font("Arial","B",10)
    pdf.ln(15)
    for tit in titre:
        pdf.cell(tit[1],10,tit[0],1,0,align="C")
    pdf.ln()

    for personne in Salarie.LISTE_SALARIES:
        print(personne)
        
        pdf.cell(30,10,personne.nom,1)
        pdf.cell(30,10,personne.prenom,1)
        donnees = personne.get_salarie()
        print(donnees)
        for num,elt in enumerate(donnees):
            if num > 1:
                pdf.cell(titre[num][1],10,"%.2f" %elt,1,0,align="R")
                
        pdf.ln()
            
    pdf.output("tuto.pdf","F")
    



    