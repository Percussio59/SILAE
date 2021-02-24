param = {
    "2020":(10.15,0.3205,0.3245),
    "2021":(10.25,0.3206,0.3246)
}


def fillon(heures, brut, brut_abattu, annee, majoree = False, ):
    """Retourne la réduction fillon calculée avec le plafonnement pour les personnes bénéficiant d'un abattement

    Args:
        heures ([float]): Nombre d'heures du salarié
        brut ([float]): Salaire brut avant abattement
        brut_abattu ([float]): Salaire brut après abattement
        annee ([int]): [Année pour la formule à appliquer]
        majoree (bool, optional): [Savoir si l'enteprise applique la réduction normale ou majorée]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if majoree == False:
        R=param[annee][1]
    else:
        R=param[annee][2]
    smic = param[annee][0]

    
    if brut != 0:
        coef1 = (R / 0.6) * ( ((1.6 * heures * smic) / brut ) - 1)
        coef1 = round(coef1,4)

        coef2 = (R / 0.6) * ( ((1.6 * heures * smic) / brut_abattu ) - 1)
        coef2 = round(coef2, 4)

        if coef1 < 0:
            coef1 = 0
        
        if coef1 > R:
            coef1 = R
        
        if coef2 < 0:
            coef2 = 0
        
        if coef2 > R:
            coef2 = R
        
        return round(min(coef1 * brut * 1.3, coef2 * brut_abattu),2) if brut != brut_abattu else round(coef2 * brut_abattu,2)
        
    else:
        return 0    
    

