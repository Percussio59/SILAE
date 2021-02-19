import xlrd, sys, os
import winsound
from Formule import fillon


base = slice(0,23,2)
resultat = slice(1,24,2)


#ATTENTION A BIEN RESPECTER LE FORMAT DES TUPLES (Penser à développer un gestionnaire de fichier de conf)
#FICHIER MODIFIE
PARAMETRES ={
    "brut":("","Brut","R"),
    "brutabattu":("","Brut AL avec RS","R"),
    "frais":("F11", "Indemnité de repas","R"),
    "heures":("","Heures travaillées","R"),
    "absences":(("","Sous-total Absences","R"),("C","Congés payés","R")),
    "heuressup":(("","Heures supplémentaires 25%","B"),("","Heures supplémentaires 50%","B")),
    "reductions_logiciel":(("SS011.4","Réduction générale des cotisations patronales","R"),("AA311.4","Réduct. générale des cotisat. pat. retraite","R")),
    "assedic":(("CH001","Assurance chômage TrA+TrB","R")),
    "salaire_de_base":("","Salaire de base"),
    "CP":(("CP001","Congés payés","R"),("CP003","OPP BTP","R")),
}





class Salarie:
    """La classe Salarie permet d'extraire d'un classeur excel, contenant les fiches individuelles détaillées du logiciel SILAE, 
    les informations nécessaires aux calculs de la réduction générale de cotisation.

    Returns:
        [Salaire]: [Un salarié]"""
    
    
    LISTE_SALARIES = []
    ANNEE = 0
    

    def __init__(self, feuil):
        """Initialisation de la classe Salarié

        Args:
            feuil (xlrd.sheet): Feuill Excel ouvert à l'aide de la librairie xlrd et d'une boucle sur les éléments du xlrd.workbook
        """
        #CHARGEMENT DES DONNEES CHIFFREES
        #On vérifie également le format de chaque feuille
        self.vérifie_feuille(feuil)
        self.feuille = feuil
        per = self.definir_annee(feuil)
        self.definir_nom(feuil)
        self.charger_dictionnaire()


        #ON AFFECTE LES LISTES A NOS ATTRIBUTS (les listes ont toutes la meme taille de 12 éléments au départ)
        self.brut = self.chercher_valeurs(PARAMETRES["brut"])[per:]
        self.frais = self.chercher_valeurs(PARAMETRES["frais"])[per:]
        self.brutabattu = self.chercher_valeurs(PARAMETRES["brutabattu"])[per:]
        self.heures = self.chercher_valeurs(PARAMETRES["heures"])[per:]
        self.heuressup = self.chercher_valeurs(PARAMETRES["heuressup"])[per:]
        self.absences = self.chercher_valeurs(PARAMETRES["absences"])[per:]
        self.reductions_logiciel = self.chercher_valeurs(PARAMETRES["reductions_logiciel"])[per:]
        self.salaire_de_base = self.chercher_valeurs(PARAMETRES["salaire_de_base"])[per:]
        self.CP = (100/90) if sum(self.chercher_valeurs(PARAMETRES["CP"])[per:]) !=0 else 1
        
            
        
        self.reduction_calculee = fillon(sum(self.heures),sum(self.brut) - sum(self.frais), sum(self.brutabattu), Salarie.ANNEE) * self.CP 
        #DRAPEAU POUR CONDITION ULTERIEURE
        self.reduction_calculee = 0 if sum(self.chercher_valeurs(PARAMETRES["assedic"])) == 0 else self.reduction_calculee
        
        
        
        Salarie.LISTE_SALARIES.append(self)

        del self.dict

    def __repr__(self):
        print("La classe Salarie représente un salarié et les attributs qu'il récupère dans les données qu'il contient dans le dictionnaire 'dict'")


    #ON TRAVAILLE LA PREMIERE CELLULE DE CHAQUE FEUILLE POUR EXTRAIRE LE NOM ET LE PRENOM
    def definir_nom(self, feui):

        #On isole le nom à partir de la cellule
        nom = feui.cell_value(0,0).split("-")[1]
        
        #On isole le prenom à partir de la cellule
        self.nom = nom.split(" ")[1]

        #On isole le prenom à partir de la cellule
        
        self.prenom = nom.split(" ")[2:]
        for num,elt in enumerate(self.prenom):
            if "née" in elt:
                self.prenom = self.prenom[0:num]
        self.prenom = ' '.join(self.prenom)

    #ON CHARGE AU NIVEAU DE CHAQUE INSTANCE LE DICTIONNAIRE DE VALEURS
    def charger_dictionnaire(self):
        self.dict = {}
        
        #ON RECUPERE UNE LISTE DE CELLULE QU'UN CONVERTI EN NOMBRES POUR CHAQUE LIGNE DE LA FEUILLE
        for ligne in range(self.feuille.nrows):
            liste = []
            a = self.feuille.row_slice(ligne,2,26)
            for elt in a:
                if elt.value == '':
                    elt.value = 0
                    liste.append(elt.value)
                else:
                    liste.append(elt.value)  

            self.dict[(self.feuille.cell_value(ligne,0),self.feuille.cell_value(ligne,1))] = liste

    #ON DEFINIT UNE METHODE POUR QUE CHAQUE ATTRIBUT RECOIVE LES VALEURS ENREGISTREES PAR LE DICTIONNAIRE 'PARAMETRES'            
    def chercher_valeurs(self,tupl):
        """Fonction de recherche d'une ou plusieurs cles dans le dictionnaire (self.dict) de l'instance de Salarié

        Args:
            tupl (Tuple): Tuple de 3 arguments (les 2 premiers étant la clé du dictionnaire, le 3eme état le slice à appliquer "R" pour la colonne Résultat /"B" pour la colonne Base)

        Returns:
            [LIST]: Retourne la liste des éléments ou la somme des listes si plusieurs clés sont passées dans un tuple
        """
        
        liste_a_retourner = []
        #ON VERIFIE SI ON A UN SEUL OU PLUSIEURS TUPLE A CHARGER ET SI C'EST BIEN UN TUPLE PASSE EN ARGUMENT
        for elt in tupl:
            #LORSQUE L'ON A PLUSIEUR TUPLE A CHERCHER (Dans ce cas, on fait une liste de listes qu'on additionnera à la fin)
            if type(elt)==tuple:
                if len(elt) != 3:
                    print("PARAMETRES DE RECHERCHE INVALIDES, MERCI DE VERIFIER VOTRE FICHER DE CONFIGURATION")
                    break
            
                else:    
                #UNE FOIS CHARGES LES 24 CELLULES DE LA FEUILLE ON NE RETOURNE QU'UNE LISTE DES 12 VALEURS QUI NOUS INTERESSE
                    try:
                        arguments = (elt[0],elt[1])
                        liste_a_retourner.append(self.dict[arguments][resultat]) if elt[2].upper=="R" else liste_a_retourner.append(self.dict[arguments][base])
                    except:
                        liste_a_retourner.append(12 * [0])
       
        #AVEC UN SEUL TUPLE A CHERCHER
            else:
                arguments = (tupl[0],tupl[1])
                try:
                     
                    return  self.dict[arguments][base] if tupl[2].upper=="R" else self.dict[arguments][resultat]
                    
                except:
                    return 12 * [0]

        
                        
        additionne = [sum([row[x] for row in liste_a_retourner]) for x in range(12)]
              
        return additionne

    #METHODE POUR RETOURNER LES TOTAUX DU DOSSIER
    @staticmethod
    def total_dossier():
        """Fonction qui retourne le total du dossier correspond à la somme de toutes les instances

        Returns:
            [LISTE]: Retourne les valeurs suivantes sous forme de float : [totalbrut, totalbrutabattu, totalheures, total_reductions_logiciel, total_redutions_calculees]
        """
        totalbrut = 0
        totalbrutabattu = 0
        totalheures = 0
        total_reductions_logiciel = 0
        total_redutions_calculees = 0


        for elt in Salarie.LISTE_SALARIES:
            totalbrut += round(sum(elt.brut),2)
            totalbrutabattu += round(sum(elt.brutabattu),2)
            totalheures += round(sum(elt.heures),2)
            total_reductions_logiciel += round(sum(elt.reductions_logiciel),2)
            total_redutions_calculees += round(elt.reduction_calculee,2)

        return [totalbrut, totalbrutabattu, totalheures, total_reductions_logiciel, total_redutions_calculees]

    #ON VERIFIE QUE LA FEUILLE SOIT BIEN AU FORMAT ATTENDU
    @staticmethod
    def vérifie_feuille(feuil):
        """Fonction de vérification du format des données
        le contrôle s'appuie sur la vérification du case contenant le mot "total"
        et d'une autre contenant le mot "Code"

        Stop l'exécution du script si la feuille ne correspond pas aux critères

        Returns:
            [None]: [description]
        """
        try:
            if feuil.cell_value(2,26) == "Total" and feuil.cell_value(3,0) == "Code":
                return True
            else:
                os.system("cls")
                print("ERREUR, LA FEUILLE NE CORRESPOND PAS AU FORMAT ATTENDU")
                print("MERCI D'EXTRAIRE DEPUIS SILAE UNE FICHE INDIVIDUELLE DETAILLEE AVEC LES BASES")
                return False
                sys.exit()
        except:
                print("ERREUR, LA FEUILLE NE CORRESPOND PAS AU FORMAT ATTENDU")
                print("MERCI D'EXTRAIRE DEPUIS SILAE UNE FICHE INDIVIDUELLE DETAILLEE AVEC LES BASES")
                sys.exit()

    #ON DEFINIT LA PERIODE DE TRAVAIL EN DEFINISSANT UN SLICE
    @staticmethod
    def definir_annee(feuil):
        """Fonction qui alimente la variable de classe ANNEE et qui retourne le premier argument du slice
        pour définir la période de travail (exemple -5 si on doit travailler sur 5 colonnes)


        Args:
            feuil (xlrd.sheet): Feuille excel retournée par la lib xlrd

        Returns:
            [INT]: retounne le premier argument du slice pour définir les attributs
        """
        Periode = feuil.row_values(2,2,26)[base]
        Periode = [ elt[-4:] for elt in Periode]
        Salarie.ANNEE = Periode[11]
        nombre_de_colonnes = Periode.count(Periode[11])
        
        return -nombre_de_colonnes
        
    def get_salarie(self):
        """Retounre les attributs du salarié selon l'ordre suivant : Nom - Prenom - Heures - Brut - Brut Abattu - Reduction Logiciel - Reduction Calculee

        Returns:
            [LIST]: [Liste des attributs]
        """
        return [self.nom, self.prenom, sum(self.heures), sum(self.brut), sum(self.brutabattu), sum(self.reductions_logiciel), self.reduction_calculee]      


   
