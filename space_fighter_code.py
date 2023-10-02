#RANDAXHE Martin
#RUSSE Cyril

import pygame
import random
import math

pygame.KEYPRESSED = pygame.USEREVENT

NOIR    = (0, 0, 0)
BLANC   = (255, 255, 255)
GRIS    = (110, 113, 127)
ROUGE   = (255, 0, 0)
BLEU    = (10, 147, 228)
JAUNE   = (235, 235, 0)
VERT    = (75, 195, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

SANTE_MAX = 100
MUNITION_MAX = 5
DEGATS_PROJECTILES = 20
DEGATS_ASTEROIDES = 34

bruit_rect = True

compteur_invulnerabilite1 = 0
compteur_invulnerabilite2 = 0
compteur_fond_ecran = 0
compteur_munition1 = 0
compteur_munition2 = 0

INTERVALLE_ASTEROIDE = 3000
INTERVALLE_BONUS = 20000
TEMPS_BONUS = 5000


#---Initialisation---#

def initialisationVariables():
    global VAISSEAU_LONG, VAISSEAU_COURT, VAISSEAU_CARRE, VITESSE_VAISSEAU
    global norme_vecteur_U, VITESSE_PROJECTILE, VITESSE_ASTEROIDE
    global ASTEROIDE_COTE, BONUS_COTE

    VAISSEAU_LONG = (FENETRE_LARGEUR // (10 * 3//2))
    VAISSEAU_COURT = (FENETRE_LARGEUR // (18 * 3//2))
    VAISSEAU_CARRE = (FENETRE_LARGEUR // (11 * 3//2))

    ASTEROIDE_COTE = FENETRE_LARGEUR // 16
    BONUS_COTE = FENETRE_LARGEUR // 30

    VITESSE_VAISSEAU = (FENETRE_LARGEUR // 150)
    VITESSE_ASTEROIDE = FENETRE_LARGEUR // 130

#@Permet d'initialiser les variables(texte, taille vaisseau...) en fonction
#   de la résolution.
def initialisationResolution():
    global vaisseau1, vaisseau2, imageFond, scene_vaisseau, ecran_titre
    global bonus, ecran_titre_petit
    global menu_jouer, menu_quitter, menu_resolution
    global reso_800_600, reso_1200_900, reso_2400_1800
    global texte_pause, texte_back_menu, texte_joueur1_win, texte_joueur2_win
    global texte_revanche, texte_back_menu_fin_round
    global choix_couleur1, choix_couleur2, couleur_bleu, couleur_vert, couleur_jaune, couleur_rouge
    global police_menu, police_titre, police_titre_petit, police_rechargement
    global texte_rechargement1, texte_rechargement2

    vaisseau1 = nouvelleEntite()
    vaisseau2 = nouvelleEntite()
    imageFond = nouvelleEntite()
    bonus = nouvelleEntite()
    initialisationVariables()

    numeroVaisseau(1, vaisseau1)
    numeroVaisseau(2, vaisseau2)
    vaisseau1['couleur'] = GRIS
    vaisseau2['couleur'] = GRIS

    chargementImagesVaisseau(vaisseau1)
    chargementImagesVaisseau(vaisseau2)
    chargementImageFondEcran(imageFond)
    chargementImageAsteroide()
    chargementImageBonus()

    bonus['position'] = [0, FENETRE_HAUTEUR * 2]

    scene_vaisseau = [vaisseau1, vaisseau2]
    positionInitVaisseau()

    police_titre = pygame.font.Font("polices/Architectural.ttf", FENETRE_LARGEUR // 5)
    police_titre_petit = pygame.font.Font("polices/Architectural.ttf", FENETRE_LARGEUR // 16)
    police_menu = pygame.font.Font("polices/Ailerons-Typeface.otf", FENETRE_LARGEUR // 17)
    police_rechargement = pygame.font.Font("polices/Ailerons-Typeface.otf", FENETRE_LARGEUR // 25)

    ecran_titre = nouveauMessage("Space Fighter", police_titre, BLANC, 0)
    ecran_titre_petit = nouveauMessage("Appuyez sur une touche", police_titre_petit, BLANC, 5)

    menu_jouer = nouveauMessage("Jouer", police_menu, BLANC, 1)
    menu_resolution = nouveauMessage("Résolution", police_menu, BLANC, 2)
    menu_quitter = nouveauMessage("Quitter", police_menu, BLANC, 3)

    reso_800_600 = nouveauMessage("800x600", police_menu, BLANC, 1)
    reso_1200_900 = nouveauMessage("1200x900", police_menu, BLANC, 2)
    reso_2400_1800 = nouveauMessage("2400x1800", police_menu, BLANC, 3)

    texte_pause = nouveauMessage("Pause", police_menu, GRIS, 6)
    texte_back_menu = nouveauMessage("Main Menu", police_menu, BLANC, 1)

    texte_revanche = nouveauMessage("Revanche", police_menu, BLANC, 3)
    texte_back_menu_fin_round = nouveauMessage("Main Menu", police_menu, BLANC, 4)
    texte_joueur1_win = nouveauMessage("Player 1 WIN", police_titre, vaisseau1['couleur'], 0)
    texte_joueur2_win = nouveauMessage("Player 2 WIN", police_titre, vaisseau2['couleur'], 0)

    choix_couleur1 = nouveauMessage("Couleur joueur 1", police_menu, GRIS, 6)
    choix_couleur2 = nouveauMessage("Couleur joueur 2", police_menu, GRIS, 6)
    couleur_bleu = nouveauMessage("Bleu", police_menu, BLEU, 1)
    couleur_vert = nouveauMessage("Vert", police_menu, VERT, 2)
    couleur_jaune = nouveauMessage("Jaune", police_menu, JAUNE, 3)
    couleur_rouge = nouveauMessage("Rouge", police_menu, ROUGE, 4)

def initialisationVecteurU():
    global norme_vecteur_U
    norme_vecteur_U = normeVecteurUnitaire()

def reinitialisationRetourMenu():
    global scene_asteroide

    scene_asteroide = nouvelleScene()
    positionInitVaisseau()
    reinitialiserScore()

#---FIN Initialisation---#

#---Définition ENTITE---#

#@Retourne une entite avec toutes ses propriétés.
def nouvelleEntite():
    return{
    'visible': False,
    'position': [0, 0],
    'imageAffichee': None,
    'poses':{},
    'vitesse': [0, 0],
    'vitesseCollision': [0, 0],
    'x': 0,
    'y': 0,
    'numero':0,
    'sante': SANTE_MAX,
    'direction': 1,
    'couleur': BLANC,
    'toucher': False,
    'invincible': False,
    'munition': MUNITION_MAX,
    'rechargement': False,
    'score': 0
    }

def visible(entite):
    entite['visible'] = True

#@Place l'entite a la position x, y.
def invisible(entite):
    entite['visible'] = False

def estVisible(entite):
    return entite['visible']

def place(entite, x, y):
    entite['position'][0] = x
    entite['position'][1] = y

def position(entite):
    return entite['position']

def ajoutePose(entite, nom, image):
    entite['poses'][nom] = image

def prendsPose(entite, pose):
    entite['imageAffichee'] = entite['poses'][pose]
    visible(entite)

def vitesse(entite, vx, vy):
    entite['vitesse'][0] = vx
    entite['vitesse'][1] = vy

def deplace(entite):
        entite['position'][0] += entite['vitesse'][0]
        entite['position'][1] += entite['vitesse'][1]

        entite['vitesse'][0] = 0
        entite['vitesse'][1] = 0

def numeroVaisseau(numero, vaisseau):
    vaisseau['numero'] = numero

def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])

def rectangle(entite):
    return (entite['imageAffichee'].get_rect().move(entite['position'][0], entite['position'][1]))

#@empeche le vaisseau de sortir du terrain
def repositionnementVaisseaux():
    for vaisseau in (vaisseau1, vaisseau2):
        if vaisseau['position'][0] < 0:
            vaisseau['position'][0] = 0
        elif vaisseau['position'][0] > FENETRE_LARGEUR - VAISSEAU_LONG:
            vaisseau['position'][0] = FENETRE_LARGEUR - VAISSEAU_LONG
        if vaisseau['position'][1] < 0:
            vaisseau['position'][1] = 0
        elif vaisseau['position'][1] > FENETRE_HAUTEUR - VAISSEAU_LONG:
            vaisseau['position'][1] = FENETRE_HAUTEUR - VAISSEAU_LONG

#---FIN ENTITE---#

#---Asteroides---#

#@Permet de créer des angles aléatoires, compris entre x et y, en radians
def angleRandom(x, y):
    random.seed()
    angle = random.randint(x, y)
    angle = math.radians(angle)
    return angle

#@Crée une position initiale aléatoire, pour un astéroide à partir d'un angle
#   aléatoire, créé par la fonction "angleRandom". Le principe est de créer une
#   position sur un cercle imaginaire, de rayon FENETRE_LARGEUR et ayant pour
#   centre, le centre de la fenêtre.
def positionInitRandom(angle):
    centre = (FENETRE_LARGEUR // 2, FENETRE_HAUTEUR // 2)
    position = [int(FENETRE_LARGEUR * math.cos(angle) + centre[0]), int(FENETRE_LARGEUR * math.sin(angle) + centre [1])]
    return position

#@Crée une entité qui représente un nouvel astéroide, à laquel on donne une vitesse
#   se dirigeant à l'opposé, sur le cercle trigonométrique, de l'angle qui a permet
#   de créer sa position initiale. Un angle aléatoire entre -10 et 10 degrés
#   est rajouté pour éviter que tous les astéroides ne passent par le centre de
#   la fenêtre. L'image de l'asteroide est chargée dans l'entité.
def nouvelAsteroide():
    asteroide = nouvelleEntite()
    asteroide['angle'] = angleRandom(0, 359)
    norme_vitesse_asteroide = VITESSE_ASTEROIDE
    angle = asteroide['angle'] - math.pi + angleRandom(-10, 10)
    vitesse(asteroide, int(norme_vitesse_asteroide * math.cos(angle)), int(norme_vitesse_asteroide * math.sin(angle)))
    asteroide['position'] = positionInitRandom(asteroide['angle'])
    ajoutePose(asteroide, 'pose_asteroide', image_asteroide)
    prendsPose(asteroide, 'pose_asteroide')

    return asteroide

#@crée un nouvel astéroide et l'ajoute à la scène dédiée aux astéroides
def faitAsteroide(scene):
    asteroide = nouvelAsteroide()
    ajouteEntite(scene, asteroide)

def deplaceAsteroide(asteroide):
    asteroide['position'][0] += asteroide['vitesse'][0]
    asteroide['position'][1] += asteroide['vitesse'][1]

#@Appelle les fonctions qui gère le déplacement des astéroides,
#   gère les collisions entres astéroides et entres astéroides et vaisseaux et
#   s'occupe de supprimer les entités qui sortent de l'écran.
def majSceneAsteroide(scene):
    for asteroide in scene['acteurs']:
        deplaceAsteroide(asteroide)
    collisionsAsteroide(scene_asteroide)
    supprimerAsteroideHorsZone(scene_asteroide)

#@Gère la création des nouveaux astéroides à paritr de moments aléatoires.
#   appelle la fonction qui met à jour les astéroides et les affiches.
def gestionAsteroide():
    global maintenant, moment_prochain_asteroide
    if not etatJeu['Pause']:
        if moment_prochain_asteroide['momentSuivant'] <= maintenant:
            faitAsteroide(scene_asteroide)
        if estExpire(moment_prochain_asteroide, maintenant):
            # moment_prochain_asteroide = nouveauMomentAleatoire(INTERVALLE_ASTEROIDE)
            suivant(moment_prochain_asteroide, maintenant)
        majSceneAsteroide(scene_asteroide)
    afficheAsteroide(scene_asteroide)

def collisionsAsteroide(scene_asteroide):
    colliAsteroideAsteroide(scene_asteroide)
    colliAsteroideVaisseau(scene_asteroide)

#@Vérifie si il y a des collisions entres astéroides, et si oui, supprime les entités
def colliAsteroideAsteroide(scene_asteroide):
    entiteasupprimer = []
    for i in range(len(scene_asteroide['acteurs'])):
        for j in range(i+1, len(scene_asteroide['acteurs'])):
            if collisionsRectangle(scene_asteroide['acteurs'][i], scene_asteroide['acteurs'][j]):
                entiteasupprimer.append(j)
                entiteasupprimer.append(i)

    #Trie la liste représentant les indexs des astéroides à supprimer
    #   du plus grand au plus petit et en ne gardant les valeurs qu'une seule fois.
    #   Evite donc de supprimer un élément de plus petit index en premier,
    #   ce qui décalerait les suivants et pourrait engendrer la suppression
    #   du mauvais astéroide, voir tenter d'accéder à un élément dépassant la
    #   taille de la liste.
    entiteasupprimer.sort()
    entiteasupprimer.reverse()
    set(entiteasupprimer)

    for i in entiteasupprimer:
        enleveEntite(scene_asteroide, scene_asteroide['acteurs'][i])

#@Vérifie si il y a des collisions avec les vaisseaux et si oui, supprime les
#   astéroides et inflige des dégats au vaisseau touché.
def colliAsteroideVaisseau(scene_asteroide):
    entiteasupprimer = []
    for asteroide in range(len(scene_asteroide['acteurs'])):
        asteroide_centre = scene_asteroide['acteurs'][asteroide]
        asteroide_centre['position'][0] += FENETRE_LARGEUR // 40
        asteroide_centre['position'][1] += FENETRE_LARGEUR // 40
        for vaisseau in (vaisseau1, vaisseau2):
            if not vaisseau['invincible']:
                if vaisseau['direction'] == 2 or vaisseau['direction'] == 6:
                    if droitePositive(asteroide_centre, vaisseau) and droiteNegative(asteroide_centre, vaisseau):
                        degatsAsteroides(vaisseau)
                        entiteasupprimer.append(asteroide)
                elif vaisseau['direction'] == 4 or vaisseau['direction'] == 8:
                    if droiteNegative(asteroide_centre, vaisseau) and droitePositive(asteroide_centre, vaisseau):
                        degatsAsteroides(vaisseau)
                        entiteasupprimer.append(asteroide)
                elif vaisseau['direction'] == 1 or vaisseau['direction'] == 5:
                    if asteroide_centre['position'][0] + ASTEROIDE_COTE // 2 > vaisseau['position'][0] and asteroide_centre['position'][0] - ASTEROIDE_COTE // 2 < vaisseau['position'][0] + VAISSEAU_COURT:
                        if asteroide_centre['position'][1] + ASTEROIDE_COTE // 2 > vaisseau['position'][1] and asteroide_centre['position'][1] - ASTEROIDE_COTE // 2 < vaisseau['position'][1] + VAISSEAU_LONG:
                            degatsAsteroides(vaisseau)
                            entiteasupprimer.append(asteroide)
                elif vaisseau['direction'] == 3 or vaisseau['direction'] == 7:
                    if asteroide_centre['position'][0] + ASTEROIDE_COTE // 2 > vaisseau['position'][0] and asteroide_centre['position'][0] - ASTEROIDE_COTE // 2 < vaisseau['position'][0] + VAISSEAU_LONG:
                        if asteroide_centre['position'][1] + ASTEROIDE_COTE // 2 > vaisseau['position'][1] and asteroide_centre['position'][1] - ASTEROIDE_COTE // 2 < vaisseau['position'][1] + VAISSEAU_COURT:
                            degatsAsteroides(vaisseau)
                            entiteasupprimer.append(asteroide)
        asteroide_centre['position'][0] -= FENETRE_LARGEUR // 40
        asteroide_centre['position'][1] -= FENETRE_LARGEUR // 40

    #Trie la liste représentant les indexs des astéroides à supprimer
    #   du plus grand au plus petit et en ne gardant les valeurs qu'une seule fois.
    #   Evite donc de supprimer un élément de plus petit index en premier,
    #   ce qui décalerait les suivants et pourrait engendrer la suppression
    #   du mauvais astéroide, voir tenter d'accéder à un élément dépassant la
    #   taille de la liste.
    entiteasupprimer.sort()
    entiteasupprimer.reverse()
    set(entiteasupprimer)

    for i in entiteasupprimer:
        enleveEntite(scene_asteroide, scene_asteroide['acteurs'][i])

#@Inflige les dégats au vaisseau et le rend invincible en rendant l'élément
#   invincible de l'entité True. Augmente le score de l'adversaire si ce dégat
#   fait déscendre la vie du vaisseau en dessous de 0.
def degatsAsteroides(vaisseau):
    global compteur_invulnerabilite1, compteur_invulnerabilite2
    fin_match = finMatch()
    if vaisseau['sante'] != 0 and not finMatch():
        vaisseau['sante'] -= DEGATS_ASTEROIDES
        vaisseau['toucher'] = True
        vaisseau['invincible'] = True
        if vaisseau['sante'] < 0:
            vaisseau['sante'] = 0
        if vaisseau['numero'] == 1:
            compteur_invulnerabilite1 = 0
        else:
            compteur_invulnerabilite2 = 0
    if vaisseau['sante'] == 0 and not fin_match:
        if vaisseau['numero'] == 1:
            augmenteScore(vaisseau2)
        else:
            augmenteScore(vaisseau1)

#@Retourne True si l'asteroide sort de l'écran. Vérifie donc que sa position
#   est bien hors de celui-ci et que le vecteur centre -> position asteroide
#   est plus petit que que le vecteur centre -> position_futur
def sortieEcranAsteroide(asteroide):
    future_position = [0, 0]
    vecteur_centre_future_position = [0, 0]
    vecteur_centre_position_actuelle = [0, 0]
    centre = [FENETRE_LARGEUR // 2, FENETRE_HAUTEUR // 2]
    position_asteroide = asteroide['position']

    future_position[0] = position_asteroide[0] + asteroide['vitesse'][0]
    future_position[1] = position_asteroide[1] + asteroide['vitesse'][1]

    vecteur_centre_position_actuelle[0] = position_asteroide[0] - centre[0]
    vecteur_centre_position_actuelle[1] = position_asteroide[1] - centre[1]
    vecteur_centre_future_position[0] = future_position[0] - centre[0]
    vecteur_centre_future_position[1] = future_position[1] - centre[1]

    norme_vecteur_maintenant = math.sqrt(vecteur_centre_position_actuelle[0]**2 + vecteur_centre_position_actuelle[1]**2)
    norme_vecteur_future_position = math.sqrt(vecteur_centre_future_position[0]**2 + vecteur_centre_future_position[1]**2)

    if norme_vecteur_maintenant - norme_vecteur_future_position < 0:
        return True
    else:
        return False

#@Supprime les asteroides sortis de l'écran.
def supprimerAsteroideHorsZone(scene):
    entiteasupprimer = []
    for asteroide in range(len(scene['acteurs'])):
        if sortieEcranAsteroide(scene['acteurs'][asteroide]):
            if scene['acteurs'][asteroide]['position'][0] - FENETRE_LARGEUR // 4 > FENETRE_LARGEUR or scene['acteurs'][asteroide]['position'][0] + FENETRE_LARGEUR // 4 < 0:
                if scene['acteurs'][asteroide]['position'][1] - FENETRE_HAUTEUR // 4 > FENETRE_HAUTEUR or scene['acteurs'][asteroide]['position'][1] + FENETRE_LARGEUR // 4 < 0:
                    entiteasupprimer.append(asteroide)

    #Trie la liste représentant les indexs des astéroides à supprimer
    #   du plus grand au plus petit et en ne gardant les valeurs qu'une seule fois.
    #   Evite donc de supprimer un élément de plus petit index en premier,
    #   ce qui décalerait les suivants et pourrait engendrer la suppression
    #   du mauvais astéroide, voir tenter d'accéder à un élément dépassant la
    #   taille de la liste.
    entiteasupprimer.sort()
    entiteasupprimer.reverse()
    set(entiteasupprimer)

    for i in entiteasupprimer:
        enleveEntite(scene_asteroide, scene_asteroide['acteurs'][i])

#---FIN Asteroides---#

#---Moment Aléatoire---#

#@Crée une bibliothèque pour une nouveau moment aléatoire.
def nouveauMomentAleatoire(intervalle):
    return{
    'momentSuivant': 0,
    'max': intervalle,
    'min': intervalle // 2
    }

#@Crée aléatoirement un prochain moment suivant.
def suivant(momentAleatoire, maintenant):
    momentAleatoire['momentSuivant'] = (maintenant + random.randint(momentAleatoire['min'], momentAleatoire['max']))

#@Retroune vrai si le moment aléatoire du dernier asteroide créé a expiré.
def estExpire(momentAleatoire, maintenant):
        return momentAleatoire['momentSuivant'] <= maintenant

#---FIN Moment Aléatoire---#

#---Gestion Plusieurs Touches---#

def nouveauEtatTouche():
    return{
        'actif':False,
        'delai':0,
        'periode':0,
        'suivant':0
    }

def nouvelleGestionClavier():
    return {}

def repeteTouche(gc, touche, delai, periode):
    pygame.key.set_repeat()

    if touche in gc:
        entree = gc[touche]
    else:
        entree = nouveauEtatTouche()

    entree['delai'] = delai
    entree['periode'] = periode
    gc[touche] = entree

def scan(gc):
    maintenant = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    for touche in gc:
        if keys[touche] == 1:
            if gc[touche]['actif']:
                if maintenant >= gc[touche]['suivant']:
                    gc[touche]['suivant'] = gc[touche]['periode'] + maintenant
                    pygame.event.post(pygame.event.Event(pygame.KEYPRESSED, {'key':touche}))
            else:
                gc[touche]['actif'] = True
                gc[touche]['suivant'] = gc[touche]['delai'] + maintenant
        else:
            gc[touche]['actif'] = False
            gc[touche]['suivant'] = 0

def initialisationCommandeJoueur1():
    return{
    'TOUCHE_HAUT': pygame.K_s,
    'TOUCHE_DROITE': pygame.K_c,
    'TOUCHE_GAUCHE': pygame.K_w,
    'TOUCHE_BAS': pygame.K_x,
    'TIR': pygame.K_u
    }

def initialisationCommandeJoueur2():
    return{
    'TOUCHE_HAUT': pygame.K_UP,
    'TOUCHE_DROITE': pygame.K_RIGHT,
    'TOUCHE_GAUCHE': pygame.K_LEFT,
    'TOUCHE_BAS': pygame.K_DOWN,
    'TIR': pygame.K_m
    }

#---FIN Gestion Plusieurs Touches---#

#---Gestion Touches---#

#@gère les entrées de l'utilisateur
def traiteEntree():
    global etatJeu
    vaisseau1['x'] = 0
    vaisseau1['y'] = 0
    vaisseau2['x'] = 0
    vaisseau2['y'] = 0
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            etatJeu['fini'] = True
        if evenement.type == pygame.KEYDOWN:
            if etatJeu['inMenuIntro']:
                etatJeu['inMenuIntro'] = False
                etatJeu['inMainMenu'] = True
            if etatJeu['inMainMenu']:
                if evenement.key == pygame.K_p:
                    etatJeu['inMainMenu'] = False
                    etatJeu['enJeu'] = True
                    etatJeu['inMenu'] = False
            if evenement.key == pygame.K_ESCAPE:
                if etatJeu['inMenu']:
                    menuPrecedent()
                elif etatJeu['enJeu'] and not finMatch():
                    menuPause()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if etatJeu['inMenu'] or etatJeu['Pause'] or finMatch():
                traiteClic(evenement.button)
        elif evenement.type == pygame.KEYPRESSED:
            if etatJeu['enJeu'] and not etatJeu['Pause'] and not finMatch():
                gestionVaisseau(evenement)
                tirNormal(evenement)
    deplacementVaisseau()

#@Gestion du clique gauche de la souris et affichage de rectangles si
#   la position de la souris est sur une des cases des menus
def traiteClic(bouton):
    global etatJeu, texte_joueur1_win, texte_joueur2_win, texte_rechargement1
    global texte_rechargement2, texte_score1, texte_score2
    global musique_jeuc
    global FENETRE_LARGEUR, FENETRE_HAUTEUR
    if not bouton == 1:
        return
    if etatJeu['enJeu']:
        if etatJeu['Pause']:
            if positionRectangle(texte_back_menu):
                etatJeu['enJeu'] = False
                etatJeu['inMenu'] = True
                etatJeu['inMainMenu'] = True
                etatJeu['Pause'] = False
                reinitialisationRetourMenu()
                return
        elif finMatch():
            if positionRectangle(texte_revanche):
                initialisationSante()
                positionInitVaisseau()
                musique_jeuc = True
            elif positionRectangle(texte_back_menu_fin_round):
                etatJeu['enJeu'] = False
                etatJeu['inMenu'] = True
                etatJeu['inMainMenu'] = True
                etatJeu['Pause'] = False
                reinitialisationRetourMenu()
    if etatJeu['inMainMenu']:
        if positionRectangle(menu_jouer):
            etatJeu['inMainMenu'] = False
            etatJeu['inChoixCouleur'] = True
            etatJeu['choix_joueur1'] = True
            initialisationSante()
        elif positionRectangle(menu_quitter):
            etatJeu['fini'] = True
        elif positionRectangle(menu_resolution):
            etatJeu['inMainMenu'] = False
            etatJeu['inMenuResolution'] = True
    elif etatJeu['inChoixCouleur']:
        if etatJeu['choix_joueur1']:
            if positionRectangle(couleur_bleu):
                vaisseau1['couleur'] = BLEU
                chargementImagesVaisseau(vaisseau1)
                etatJeu['choix_joueur1'] = False
                texte_joueur1_win = nouveauMessage("Player 1 WIN", police_titre, vaisseau1['couleur'], 0)
                texte_rechargement1 = nouveauMessage("Rechargement", police_rechargement, vaisseau1['couleur'], 7)
                texte_score1 = nouveauMessage("0", police_menu, vaisseau1['couleur'], 9)
            elif positionRectangle(couleur_rouge):
                vaisseau1['couleur'] = ROUGE
                chargementImagesVaisseau(vaisseau1)
                etatJeu['choix_joueur1'] = False
                texte_joueur1_win = nouveauMessage("Player 1 WIN", police_titre, vaisseau1['couleur'], 0)
                texte_rechargement1 = nouveauMessage("Rechargement", police_rechargement, vaisseau1['couleur'], 7)
                texte_score1 = nouveauMessage("0", police_menu, vaisseau1['couleur'], 9)
            elif positionRectangle(couleur_vert):
                vaisseau1['couleur'] = VERT
                chargementImagesVaisseau(vaisseau1)
                etatJeu['choix_joueur1'] = False
                texte_joueur1_win = nouveauMessage("Player 1 WIN", police_titre, vaisseau1['couleur'], 0)
                texte_rechargement1 = nouveauMessage("Rechargement", police_rechargement, vaisseau1['couleur'], 7)
                texte_score1 = nouveauMessage("0", police_menu, vaisseau1['couleur'], 9)
            elif positionRectangle(couleur_jaune):
                vaisseau1['couleur'] = JAUNE
                chargementImagesVaisseau(vaisseau1)
                etatJeu['choix_joueur1'] = False
                texte_joueur1_win = nouveauMessage("Player 1 WIN", police_titre, vaisseau1['couleur'], 0)
                texte_rechargement1 = nouveauMessage("Rechargement", police_rechargement, vaisseau1['couleur'], 7)
                texte_score1 = nouveauMessage("0", police_menu, vaisseau1['couleur'], 9)
        else:
            if positionRectangle(couleur_bleu):
                if vaisseau1['couleur'] != BLEU:
                    vaisseau2['couleur'] = BLEU
                    chargementImagesVaisseau(vaisseau2)
                    etatJeu['choix_joueur1'] = False
                    etatJeu['enJeu'] = True
                    etatJeu['inMenu'] = False
                    etatJeu['inChoixCouleur'] = False
                    texte_joueur2_win = nouveauMessage("Player 2 WIN", police_titre, vaisseau2['couleur'], 0)
                    texte_rechargement2 = nouveauMessage("Rechargement", police_rechargement, vaisseau2['couleur'], 8)
                    texte_score2 = nouveauMessage("0", police_menu, vaisseau2['couleur'], 10)
                    positionInitVaisseau()
            elif positionRectangle(couleur_rouge):
                if vaisseau1['couleur'] != ROUGE:
                    vaisseau2['couleur'] = ROUGE
                    chargementImagesVaisseau(vaisseau2)
                    etatJeu['choix_joueur1'] = False
                    etatJeu['enJeu'] = True
                    etatJeu['inMenu'] = False
                    etatJeu['inChoixCouleur'] = False
                    texte_joueur2_win = nouveauMessage("Player 2 WIN", police_titre, vaisseau2['couleur'], 0)
                    texte_rechargement2 = nouveauMessage("Rechargement", police_rechargement, vaisseau2['couleur'], 8)
                    texte_score2 = nouveauMessage("0", police_menu, vaisseau2['couleur'], 10)
                    positionInitVaisseau()
            elif positionRectangle(couleur_vert):
                if vaisseau1['couleur'] != VERT:
                    vaisseau2['couleur'] = VERT
                    chargementImagesVaisseau(vaisseau2)
                    etatJeu['enJeu'] = True
                    etatJeu['inMenu'] = False
                    etatJeu['inChoixCouleur'] = False
                    etatJeu['choix_joueur1'] = False
                    texte_joueur2_win = nouveauMessage("Player 2 WIN", police_titre, vaisseau2['couleur'], 0)
                    texte_rechargement2 = nouveauMessage("Rechargement", police_rechargement, vaisseau2['couleur'], 8)
                    texte_score2 = nouveauMessage("0", police_menu, vaisseau2['couleur'], 10)
                    positionInitVaisseau()
            elif positionRectangle(couleur_jaune):
                if vaisseau1['couleur'] != JAUNE:
                    vaisseau2['couleur'] = JAUNE
                    chargementImagesVaisseau(vaisseau2)
                    etatJeu['choix_joueur1'] = False
                    etatJeu['enJeu'] = True
                    etatJeu['inMenu'] = False
                    etatJeu['inChoixCouleur'] = False
                    texte_joueur2_win = nouveauMessage("Player 2 WIN", police_titre, vaisseau2['couleur'], 0)
                    texte_rechargement2 = nouveauMessage("Rechargement", police_rechargement, vaisseau2['couleur'], 8)
                    texte_score2 = nouveauMessage("0", police_menu, vaisseau2['couleur'], 10)
                    positionInitVaisseau()
    elif etatJeu['inMenuResolution']:
        if positionRectangle(reso_800_600):
            changerResolution(800, 600)
        elif positionRectangle(reso_1200_900):
            changerResolution(1200, 900)
        elif positionRectangle(reso_2400_1800):
            changerResolution(2400, 1800)

def menuPrecedent():
    global etatJeu

    if etatJeu['inMenuResolution']:
        etatJeu['inMenuResolution'] = False
        etatJeu['inMainMenu'] = True
    elif etatJeu['inChoixCouleur']:
        etatJeu['inChoixCouleur'] = False
        etatJeu['inMainMenu'] = True

def menuPause():
    global etatJeu

    if not etatJeu['Pause']:
        etatJeu['Pause'] = True
    else:
        etatJeu['Pause'] = False

def initialisationRepeteTouche():
    repeteTouche(gc, commande_joueur2['TOUCHE_DROITE'], 15, 15)
    repeteTouche(gc, commande_joueur2['TOUCHE_HAUT'], 15, 15)
    repeteTouche(gc, commande_joueur2['TOUCHE_BAS'], 15, 15)
    repeteTouche(gc, commande_joueur2['TOUCHE_GAUCHE'], 15, 15)
    repeteTouche(gc, commande_joueur1['TOUCHE_HAUT'], 15, 15)
    repeteTouche(gc, commande_joueur1['TOUCHE_BAS'], 15, 15)
    repeteTouche(gc, commande_joueur1['TOUCHE_DROITE'], 15, 15)
    repeteTouche(gc, commande_joueur1['TOUCHE_GAUCHE'], 15, 15)
    repeteTouche(gc, commande_joueur1['TIR'], 50, 250)
    repeteTouche(gc, commande_joueur2['TIR'], 50, 250)

#---FIN Gestion Touches---#

#---Résolution---#

#@change la taille de la fenetre et recharge/redimmensionne tous les éléments qui
#   nécéssite de changer de taille en fonction des nouvelles dimensions
def changerResolution(fenetre_largeur, fenetre_hauteur):
    global fenetre, FENETRE_LARGEUR, FENETRE_HAUTEUR
    FENETRE_LARGEUR = fenetre_largeur
    FENETRE_HAUTEUR = fenetre_hauteur
    fenetre_taille = [FENETRE_LARGEUR, FENETRE_HAUTEUR]
    fenetre = pygame.display.set_mode(fenetre_taille)
    initialisationResolution()

#---FIN Résolution---#

#---Déplacement Vaisseaux---#

#@Permet de savoir la direction du vaisseau en changeant les éléments "x" et "y" par
#   1 ou -1, ces valeurs sont réinitialisées à 0 à chaque déplacement dans la
#   fonction "traiteEntree()" de l'entité vaisseau,
#   pour pouvoir par après gérer le déplacement des vaisseaux.
def gestionVaisseau(evenement):
    for n_vaisseau, commande_vaisseau in ((vaisseau1, commande_joueur1), (vaisseau2, commande_joueur2)):
        if evenement.key == commande_vaisseau['TOUCHE_HAUT']:
            n_vaisseau['y'] -= 1
        if evenement.key == commande_vaisseau['TOUCHE_BAS']:
            n_vaisseau['y'] += 1
        if evenement.key == commande_vaisseau['TOUCHE_DROITE']:
            n_vaisseau['x'] += 1
        if evenement.key == commande_vaisseau['TOUCHE_GAUCHE']:
            n_vaisseau['x'] -= 1

#@Change la vitesse dans l'entité vaisseau en fonction de sa direction et change
#   de pose afin d'afficher l'image correspondante à cette direction.
def deplacementVaisseau():
    for n_vaisseau in (vaisseau1, vaisseau2):
        if n_vaisseau['x'] == 0:
            vitesse(n_vaisseau, n_vaisseau['x'] * VITESSE_VAISSEAU, n_vaisseau['y'] * VITESSE_VAISSEAU)
            if n_vaisseau['y'] == 1:
                prendsPose(n_vaisseau, 'vaisseau_down')
                n_vaisseau['direction'] = 5
            elif n_vaisseau['y'] == -1:
                prendsPose(n_vaisseau, 'vaisseau_up')
                n_vaisseau['direction'] = 1
        elif n_vaisseau['y'] == 0:
            vitesse(n_vaisseau, n_vaisseau['x'] * VITESSE_VAISSEAU, n_vaisseau['y'] * VITESSE_VAISSEAU)
            if n_vaisseau['x'] == 1:
                prendsPose(n_vaisseau, 'vaisseau_right')
                n_vaisseau['direction'] = 3
            elif n_vaisseau['x'] == -1:
                prendsPose(n_vaisseau, 'vaisseau_left')
                n_vaisseau['direction'] = 7
        else:
            vitesse(n_vaisseau, n_vaisseau['x'] * VITESSE_VAISSEAU * (math.sqrt(2) / 2), n_vaisseau['y'] * VITESSE_VAISSEAU * (math.sqrt(2) / 2))
            if n_vaisseau['x'] == 1 and n_vaisseau['y'] == 1:
                prendsPose(n_vaisseau, 'vaisseau_bas_droit')
                n_vaisseau['direction'] = 4
            elif n_vaisseau['x'] == 1 and n_vaisseau['y'] == -1:
                prendsPose(n_vaisseau, 'vaisseau_haut_droit')
                n_vaisseau['direction'] = 2
            elif n_vaisseau['x'] == -1 and n_vaisseau['y'] == 1:
                prendsPose(n_vaisseau, 'vaisseau_bas_gauche')
                n_vaisseau['direction'] = 6
            elif n_vaisseau['x'] == -1 and n_vaisseau['y'] == -1:
                prendsPose(n_vaisseau, 'vaisseau_haut_gauche')
                n_vaisseau['direction'] = 8

#@Positionne les vaisseaux à leur position de départ
def positionInitVaisseau():
    place(vaisseau1, FENETRE_LARGEUR // 16, FENETRE_HAUTEUR // 2 - (VAISSEAU_LONG / 2))
    place(vaisseau2, FENETRE_LARGEUR - (FENETRE_LARGEUR // 16 + VAISSEAU_LONG), FENETRE_HAUTEUR / 2 - (VAISSEAU_LONG / 2))
    prendsPose(vaisseau1, 'vaisseau_right')
    prendsPose(vaisseau2, 'vaisseau_left')
    vaisseau1['direction'] = 3
    vaisseau2['direction'] = 7

#@Mets à jour la position des vaisseaux et utilise la fonction
#   "repositionnementVaisseaux" pour les empêcher de sortir de l'écran
def majVaisseau(scene):
    for objet in scene:
        deplace(objet)
    repositionnementVaisseaux()

#---FIN Déplacement---#

#---Projectile--#

#@Crée une entité projectile qui appartient à un des deux vaisseaux
def nouveauProjectile(vaisseau):
    return{
    'position': [0, 0],
    'rayon': FENETRE_LARGEUR // 80,
    'couleur': vaisseau['couleur'],
    'proprietaire': vaisseau['numero'],
    'vitesse': [0, 0],
    'norme_vitesse': FENETRE_LARGEUR // (16 * 5)
    }

#@Crée un projectile si une des touches de tir est enfoncées. Crée les bruitages.
#   Applique la constantes VITESSE_PROJECTILE dans la même direction que le vaisseau.
#   Retire une munition.
def tirNormal(evenement):
    global compteur_munition1, compteur_munition2
    for commande, vaisseau in ((commande_joueur1, vaisseau1), (commande_joueur2, vaisseau2)):
        if evenement.key == commande['TIR']:
            if not vaisseau['rechargement']:
                if vaisseau['numero'] == 1:
                    compteur_munition1 = 0
                else:
                    compteur_munition2 = 0
                vaisseau['munition'] -= 1
                if vaisseau['munition'] == 0:
                    vaisseau['rechargement'] = True
                laser1.play(sons['piou_piou'])
                laser2.play(sons['piou_piou'])
                projectile = nouveauProjectile(vaisseau)
                if vaisseau['direction'] == 3 or vaisseau['direction'] == 7:
                    projectile['position'] = [vaisseau['position'][0] + VAISSEAU_LONG // 2, vaisseau['position'][1] + VAISSEAU_COURT // 2]
                elif vaisseau['direction'] == 5 or vaisseau['direction'] == 1:
                    projectile['position'] = [vaisseau['position'][0] + VAISSEAU_COURT // 2, vaisseau['position'][1] + VAISSEAU_LONG // 2]
                elif vaisseau['direction'] == 2 or vaisseau['direction'] == 4 or vaisseau['direction'] == 6 or vaisseau['direction'] == 8:
                    projectile['position'] = [vaisseau['position'][0] + VAISSEAU_CARRE // 2, vaisseau['position'][1] + VAISSEAU_CARRE // 2]
                vitesseProjectile(projectile, vaisseau)
                ajouteEntite(scene_projectile, projectile)

#@Applique la constantes VITESSE_PROJECTILE dans la même direction que le vaisseau.
def vitesseProjectile(projectile, vaisseau):
    racine2_2 = math.sqrt(2) / 2
    if vaisseau['direction'] == 1:
        projectile['vitesse'] = [0, -projectile['norme_vitesse']]
    elif vaisseau['direction'] == 2:
        projectile['vitesse'] = [projectile['norme_vitesse'] * racine2_2, -projectile['norme_vitesse'] * racine2_2]
    elif vaisseau['direction'] == 3:
        projectile['vitesse'] = [projectile['norme_vitesse'], 0]
    elif vaisseau['direction'] == 4:
        projectile['vitesse'] = [projectile['norme_vitesse'] * racine2_2, projectile['norme_vitesse'] * racine2_2]
    elif vaisseau['direction'] == 5:
        projectile['vitesse'] = [0, projectile['norme_vitesse']]
    elif vaisseau['direction'] == 6:
        projectile['vitesse'] = [-projectile['norme_vitesse'] * racine2_2, projectile['norme_vitesse'] * racine2_2]
    elif vaisseau['direction'] == 7:
        projectile['vitesse'] = [-projectile['norme_vitesse'], 0]
    elif vaisseau['direction'] == 8:
        projectile['vitesse'] = [-projectile['norme_vitesse'] * racine2_2, -projectile['norme_vitesse'] * racine2_2]

def dessineProjectile(projectile):
    pygame.draw.circle(fenetre, projectile['couleur'], (int(projectile['position'][0]), int(projectile['position'][1])), projectile['rayon'])

def deplaceProjectile(projectile):
    if not etatJeu['Pause']:
        projectile['position'][0] += projectile['vitesse'][0]
        projectile['position'][1] += projectile['vitesse'][1]

#@Mets à jour les projectiles :
#   change sa position, verifie les collisions avec les vaisseaux et les suppriment
#   si ils sortent de l'écran.
def majProjectiles(scene_projectile):
    for projectiles in scene_projectile['acteurs']:
        deplaceProjectile(projectiles)
        CollProjectile(projectiles)
        supprimerProjectilesHorsZone(projectiles, scene_projectile)

def supprimerProjectilesHorsZone(objet, scene_projectile):
    if objet['position'][0] + objet['rayon'] > FENETRE_LARGEUR or objet['position'][0] - objet['rayon'] < 0:
        enleveEntite(scene_projectile, objet)
    elif objet['position'][1] + objet['rayon'] > FENETRE_HAUTEUR or objet['position'][1] - objet['rayon'] < 0:
        enleveEntite(scene_projectile, objet)

#---FIN Projectile---#

#---Scene Projectiles---#

#@Crée une bibliothèque qui garde en mémoire toutes les entités d'une catégorie.
def nouvelleScene():
    return{
    'acteurs': []
    }

#@Ajoute une entite à scene.
def ajouteEntite(scene, entite):
    scene['acteurs'].append(entite)

#@Retire une entite à scene.
def enleveEntite(scene, entite):
    acteurs = scene['acteurs']
    if entite in acteurs:
        acteurs.remove(entite)

#@Retourne la liste de tous les éléments de la scene.
def acteurs(scene):
    return list(scene['acteurs'])

#---FIN Scene Projectiles---#

#---Collisions---#

#@Retourne True si il y a collisions entre les 2 rectangles qui entoure l'image
#   des entite1 et entite2.
def collisionsRectangle(entite1, entite2):
    rect1 = rectangle(entite1)
    rect2 = rectangle(entite2)
    return rect1.colliderect(rect2)

#@Vérifie les collisions entre les 2 vaisseaux.
def detecCollisionVaisseau():
    return collisionsRectangle(vaisseau1, vaisseau2)

#Calcule la distance entre les deux vaisseaux.
def normeVecteurUnitaire():
    vx = vaisseau1['position'][0] - vaisseau2['position'][0]
    vy = vaisseau1['position'][1] - vaisseau2['position'][1]
    norme_vecteur = math.sqrt(vx**2 + vy**2)
    return norme_vecteur

#@Retourne le vecteur unitaire pointant d'un vaisseau à l'autre.
def vecteurUnitaire():
    vx = vaisseau1['position'][0] - vaisseau2['position'][0]
    vy = vaisseau1['position'][1] - vaisseau2['position'][1]
    norme_vecteur = normeVecteurUnitaire()
    return (vx / norme_vecteur, vy / norme_vecteur)

#@Crée une vitesse opposée au vecteur entre les deux vaisseaux
#   au moment de la collision.
def changeVitesseCollision(vaisseau):
    vecteurU = vecteurUnitaire()
    if vaisseau['numero'] == 2:
        vaisseau['vitesseCollision'] = [-int(vecteurU[0] * FENETRE_LARGEUR / 80), -int(vecteurU[1] * FENETRE_LARGEUR / 80)]
    else:
        vaisseau['vitesseCollision'] = [int(vecteurU[0] * FENETRE_LARGEUR / 80), int(vecteurU[1] * FENETRE_LARGEUR / 80)]

#@Gère toutes les vérifications de collisions de sorte de créer un ressenti
#   de collision inélastique. Cette vitesse artificielle, décroit légerement à
#   chaque passage.
def collisions(vaisseau1, vaisseau2):
    global norme_vecteur_U_precedent, vecteurU_derniere_collision

    vecteurU = vecteurUnitaire()
    norme_vecteur_U = normeVecteurUnitaire()
    if detecCollisionVaisseau() and norme_vecteur_U_precedent - norme_vecteur_U >= 0:
        changeVitesseCollision(vaisseau1)
        changeVitesseCollision(vaisseau2)
        vecteurU_derniere_collision = vecteurU
    norme_vecteur_U_precedent = norme_vecteur_U
    if vaisseau1['vitesseCollision'] == [0, 0]:
        return
    vaisseau1['position'][0] += vaisseau1['vitesseCollision'][0]
    vaisseau1['position'][1] += vaisseau1['vitesseCollision'][1]
    vaisseau2['position'][0] += vaisseau2['vitesseCollision'][0]
    vaisseau2['position'][1] += vaisseau2['vitesseCollision'][1]

    vaisseau1['vitesseCollision'][0] -= (vecteurU_derniere_collision[0])
    vaisseau1['vitesseCollision'][1] -= (vecteurU_derniere_collision[1])
    vaisseau2['vitesseCollision'][0] -= (-vecteurU_derniere_collision[0])
    vaisseau2['vitesseCollision'][1] -= (-vecteurU_derniere_collision[1])
    if abs(vaisseau1['vitesseCollision'][0]) < FENETRE_LARGEUR/1000 and abs(vaisseau1['vitesseCollision'][1]) < FENETRE_LARGEUR/1000:
        vaisseau1['vitesseCollision'][0] = 0
        vaisseau1['vitesseCollision'][1] = 0
        vaisseau2['vitesseCollision'][0] = 0
        vaisseau2['vitesseCollision'][1] = 0

#@Retourne True si la position de l'objet se trouve entre les 2 droites parallèles
#   au vaisseau lorsque le vaisseau est en diagonale.
def droiteNegative(objet, vaisseau):
    dedans = False
    if objet['position'][0] > vaisseau['position'][0] and objet['position'][0] < vaisseau['position'][0] + VAISSEAU_CARRE:
        if objet['position'][1] < objet['position'][0] - vaisseau['position'][0] + vaisseau['position'][1] + VAISSEAU_CARRE // 2 and objet['position'][1] > objet['position'][0] - vaisseau['position'][0] - VAISSEAU_CARRE//2 + vaisseau['position'][1]:
            dedans = True
    return dedans

#@Retourne True si la position de l'objet se trouve entre les 2 droites parallèles
#   au vaisseau lorsque le vaisseau est en diagonale.
def droitePositive(objet, vaisseau):
    dedans = False
    if objet['position'][0] > vaisseau['position'][0] and objet['position'][0] < vaisseau['position'][0] + VAISSEAU_CARRE:
        if objet['position'][1] < -objet['position'][0] + vaisseau['position'][1] + (3/2) * VAISSEAU_CARRE + vaisseau['position'][0] and objet['position'][1] > -objet['position'][0] + vaisseau['position'][1] + vaisseau['position'][0] + VAISSEAU_CARRE/2:
            dedans = True
    return dedans

#@Vérifie la collision entre projectile et les vaisseaux en fonction de leur
#   direction et, si oui, leur inflige des dégats et supprime le projectile.
def CollProjectile(projectile):
        if projectile['proprietaire'] == 1 and not vaisseau2['invincible']:
            if vaisseau2['direction'] == 2 or vaisseau2['direction'] == 6:
                if droitePositive(projectile, vaisseau2) and droiteNegative(projectile, vaisseau2):
                    enleveEntite(scene_projectile, projectile)
                    degatsProjectiles(vaisseau2)
            elif vaisseau2['direction'] == 4 or vaisseau2['direction'] == 8:
                if droiteNegative(projectile, vaisseau2) and droitePositive(projectile, vaisseau2):
                    enleveEntite(scene_projectile, projectile)
                    degatsProjectiles(vaisseau2)
            elif vaisseau2['direction'] == 1 or vaisseau2['direction'] == 5:
                if projectile['position'][0] > vaisseau2['position'][0] and projectile['position'][0] < vaisseau2['position'][0] + VAISSEAU_COURT:
                    if projectile['position'][1] > vaisseau2['position'][1] and projectile['position'][1] < vaisseau2['position'][1] + VAISSEAU_LONG:
                        enleveEntite(scene_projectile, projectile)
                        degatsProjectiles(vaisseau2)
            elif vaisseau2['direction'] == 3 or vaisseau2['direction'] == 7:
                if projectile['position'][0] > vaisseau2['position'][0] and projectile['position'][0] < vaisseau2['position'][0] + VAISSEAU_LONG:
                    if projectile['position'][1] > vaisseau2['position'][1] and projectile['position'][1] < vaisseau2['position'][1] + VAISSEAU_COURT:
                        enleveEntite(scene_projectile, projectile)
                        degatsProjectiles(vaisseau2)

        elif projectile['proprietaire'] == 2 and not vaisseau1['invincible']:
            if vaisseau1['direction'] == 2 or vaisseau1['direction'] == 6:
                if droitePositive(projectile, vaisseau1) and droiteNegative(projectile, vaisseau1):
                    enleveEntite(scene_projectile, projectile)
                    degatsProjectiles(vaisseau1)
            elif vaisseau1['direction'] == 4 or vaisseau1['direction'] == 8:
                if droiteNegative(projectile, vaisseau1) and droitePositive(projectile, vaisseau1):
                    enleveEntite(scene_projectile, projectile)
                    degatsProjectiles(vaisseau1)
            elif vaisseau1['direction'] == 1 or vaisseau1['direction'] == 5:
                if projectile['position'][0] > vaisseau1['position'][0] and projectile['position'][0] < vaisseau1['position'][0] + VAISSEAU_COURT:
                    if projectile['position'][1] > vaisseau1['position'][1] and projectile['position'][1] < vaisseau1['position'][1] + VAISSEAU_LONG:
                        enleveEntite(scene_projectile, projectile)
                        degatsProjectiles(vaisseau1)
            elif vaisseau1['direction'] == 3 or vaisseau1['direction'] == 7:
                if projectile['position'][0] > vaisseau1['position'][0] and projectile['position'][0] < vaisseau1['position'][0] + VAISSEAU_LONG:
                    if projectile['position'][1] > vaisseau1['position'][1] and projectile['position'][1] < vaisseau1['position'][1] + VAISSEAU_COURT:
                        enleveEntite(scene_projectile, projectile)
                        degatsProjectiles(vaisseau1)

#---FIN Collisions---#

#---Textes---#

#@Facilite la création de message à afficher à l'écran en retournant une
#   bibliothèque comprenant le message, sa position et ses dimensions.
def nouveauMessage(message, police, couleur, position):
    texte = police.render(message, True, couleur)
    texteL, texteH = police.size(message)
    if position == 0:
        position_texte = [(FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 3]
    elif position == 1:
        position_texte = ((FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 3)
    elif position == 2:
        position_texte = ((FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 2)
    elif position == 3:
        position_texte = ((FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) * 2 // 3)
    elif position == 4:
        position_texte = ((FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) * 5 // 6)
    elif position == 5:
        position_texte = [(FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) * 7 // 8]
    elif position == 6:
        position_texte = [(FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 6]
    elif position == 7:
        position_texte = [FENETRE_LARGEUR // 30, FENETRE_HAUTEUR - FENETRE_LARGEUR // 20 - texteH]
    elif position == 8:
        position_texte = [FENETRE_LARGEUR - texteL - FENETRE_LARGEUR // 30, FENETRE_HAUTEUR - FENETRE_LARGEUR // 20 - texteH]
    elif position == 9:
        position_texte = [FENETRE_LARGEUR // 2 - FENETRE_LARGEUR // 40 - texteL, FENETRE_HAUTEUR // 80]
    elif position == 10:
        position_texte = [FENETRE_LARGEUR // 2 + FENETRE_LARGEUR // 40, FENETRE_HAUTEUR // 80]
    return{
    'message': texte,
    'messageL': texteL,
    'messageH': texteH,
    'position': position_texte
    }

#@Retourne True si la position de la souris se trouve sur l'emplacement du rectangle
#   à afficher à l'emplacement de "message".
def positionRectangle(message):
    global bruit_rect
    if position_souris[0] >= (FENETRE_LARGEUR // 3) and position_souris [0] <= (FENETRE_LARGEUR * 2 // 3):
        if position_souris[1] >= message['position'][1] and position_souris[1] <= message['position'][1] + message['messageH']:
            return True

#@Crée un bruitage lorsque la souris passe sur un rectangle d'un menu.
def bruitagesRectangle():
    global bruit_rect
    if etatJeu['inMainMenu']:
        if positionRectangle(menu_jouer) or positionRectangle(menu_resolution) or positionRectangle(menu_quitter) :
            if bruit_rect:
                click.play(sons['click'])
                bruit_rect = False
            return
        bruit_rect = True
    elif etatJeu['inChoixCouleur']:
        if positionRectangle(couleur_bleu) or positionRectangle(couleur_vert) or positionRectangle(couleur_jaune) or positionRectangle(couleur_rouge):
            if bruit_rect:
                click.play(sons['click'])
                bruit_rect = False
            return
        bruit_rect = True
    elif etatJeu['inMenuResolution']:
        if positionRectangle(reso_800_600) or positionRectangle(reso_1200_900) or positionRectangle(reso_2400_1800):
            if bruit_rect:
                click.play(sons['click'])
                bruit_rect = False
            return
        bruit_rect = True
    elif etatJeu['Pause']:
        if positionRectangle(texte_back_menu):
            if bruit_rect:
                click.play(sons['click'])
                bruit_rect = False
            return
        bruit_rect = True
    elif etatJeu['enJeu']:
        if positionRectangle(texte_back_menu_fin_round) or positionRectangle(texte_revanche):
            if bruit_rect:
                click.play(sons['click'])
                bruit_rect = False
            return
        bruit_rect = True

#---FIN Textes---#

#---Chargement Images---#

def chargementImagesVaisseau(vaisseau):
    if vaisseau['couleur'] == ROUGE:
        chemin = 'images/vaisseau_images/rouge/'
    elif vaisseau['couleur'] == BLEU:
        chemin = 'images/vaisseau_images/bleu/'
    elif vaisseau['couleur'] == VERT:
        chemin = 'images/vaisseau_images/vert/'
    elif vaisseau['couleur'] == JAUNE:
        chemin = 'images/vaisseau_images/jaune/'
    elif vaisseau['couleur'] == GRIS:
        chemin = 'images/vaisseau_images/gris/'

    for nom_pose, nom_fichier in (('vaisseau_up','vaisseau_up.png'),
                            ('vaisseau_down', 'vaisseau_down.png')):
        IMAGE_VAISSEAU = pygame.image.load(chemin + nom_fichier).convert_alpha(fenetre)
        IMAGE_VAISSEAU = pygame.transform.scale(IMAGE_VAISSEAU, (VAISSEAU_COURT,
                                                                VAISSEAU_LONG))
        ajoutePose(vaisseau, nom_pose, IMAGE_VAISSEAU)

    for nom_pose, nom_fichier in (('vaisseau_right', 'vaisseau_right.png'),
                            ('vaisseau_left', 'vaisseau_left.png')):
        IMAGE_VAISSEAU = pygame.image.load(chemin + nom_fichier).convert_alpha(fenetre)
        IMAGE_VAISSEAU = pygame.transform.scale(IMAGE_VAISSEAU, (VAISSEAU_LONG,
                                                                VAISSEAU_COURT))
        ajoutePose(vaisseau, nom_pose, IMAGE_VAISSEAU)

    for nom_pose, nom_fichier in (('vaisseau_haut_droit', 'vaisseau_45_droit.png'),
                            ('vaisseau_bas_droit', 'vaisseau_135_droit.png'),
                            ('vaisseau_haut_gauche', 'vaisseau_45_gauche.png'),
                            ('vaisseau_bas_gauche', 'vaisseau_135_gauche.png')):
        IMAGE_VAISSEAU = pygame.image.load(chemin + nom_fichier).convert_alpha(fenetre)
        IMAGE_VAISSEAU = pygame.transform.scale(IMAGE_VAISSEAU, (VAISSEAU_CARRE,
                                                                VAISSEAU_CARRE))
        ajoutePose(vaisseau, nom_pose, IMAGE_VAISSEAU)

def chargementImageFondEcran(fond_ecran):
    chemin = 'images/fond_ecran/'
    image_Fond = pygame.image.load(chemin + 'image_fond1.png').convert_alpha(fenetre)
    image_Fond = pygame.transform.scale(image_Fond, (FENETRE_LARGEUR, FENETRE_HAUTEUR))
    ajoutePose(fond_ecran, 'image1', image_Fond)
    image_Fond = pygame.image.load(chemin + 'image_fond2.png').convert_alpha(fenetre)
    image_Fond = pygame.transform.scale(image_Fond, (FENETRE_LARGEUR, FENETRE_HAUTEUR))
    ajoutePose(fond_ecran, 'image2', image_Fond)
    image_Fond = pygame.image.load(chemin + 'image_fond3.png').convert_alpha(fenetre)
    image_Fond = pygame.transform.scale(image_Fond, (FENETRE_LARGEUR, FENETRE_HAUTEUR))
    ajoutePose(fond_ecran, 'image3', image_Fond)
    image_Fond = pygame.image.load(chemin + 'image_fond4.png').convert_alpha(fenetre)
    image_Fond = pygame.transform.scale(image_Fond, (FENETRE_LARGEUR, FENETRE_HAUTEUR))
    ajoutePose(fond_ecran, 'image4', image_Fond)
    image_Fond = pygame.image.load(chemin + 'image_fond5.png').convert_alpha(fenetre)
    image_Fond = pygame.transform.scale(image_Fond, (FENETRE_LARGEUR, FENETRE_HAUTEUR))
    ajoutePose(fond_ecran, 'image5', image_Fond)

def chargementImageAsteroide():
    global image_asteroide
    image_asteroide = pygame.image.load('images/asteroide.png').convert_alpha(fenetre)
    image_asteroide = pygame.transform.scale(image_asteroide, (ASTEROIDE_COTE, ASTEROIDE_COTE))

def chargementImageBonus():
    global image_bonus_vie, image_bonus_munition, image_bonus_invincibilite

    image_bonus_vie = pygame.image.load('images/bonus/bonus_vie.png').convert_alpha(fenetre)
    image_bonus_vie = pygame.transform.scale(image_bonus_vie, (BONUS_COTE, BONUS_COTE))
    ajoutePose(bonus, 'bonus_vie', image_bonus_vie)

    image_bonus_munition = pygame.image.load('images/bonus/bonus_munition.png').convert_alpha(fenetre)
    image_bonus_munition = pygame.transform.scale(image_bonus_munition, (BONUS_COTE, BONUS_COTE))
    ajoutePose(bonus, 'bonus_munition', image_bonus_munition)

    image_bonus_invincibilite = pygame.image.load('images/bonus/bonus_invincibilite.png').convert_alpha(fenetre)
    image_bonus_invincibilite = pygame.transform.scale(image_bonus_invincibilite, (BONUS_COTE, BONUS_COTE))
    ajoutePose(bonus, 'bonus_invincibilite', image_bonus_invincibilite)

#---FIN Chargement Images---#

#---Affichage---#

def afficheVaisseau(entites, ecran):
    for objet in entites:
        if estVisible(objet):
            dessine(objet, ecran)

def affichageRectangle(message):
    pygame.draw.rect(fenetre, GRIS, ((FENETRE_LARGEUR // 3, message['position'][1]), (FENETRE_LARGEUR // 3, message['messageH'])))

def affichageTexte(message):
    fenetre.blit(message['message'], message['position'])

def affichageTexteMenu():
    if etatJeu['inMenuIntro']:
        affichageTexte(ecran_titre)
        affichageTexte(ecran_titre_petit)
    elif etatJeu['inMainMenu']:
        if positionRectangle(menu_jouer):
            affichageRectangle(menu_jouer)
        elif positionRectangle(menu_resolution):
            affichageRectangle(menu_resolution)
        elif positionRectangle(menu_quitter):
            affichageRectangle(menu_quitter)
        affichageTexte(menu_jouer)
        affichageTexte(menu_resolution)
        affichageTexte(menu_quitter)
    elif etatJeu['inChoixCouleur']:
        if etatJeu['choix_joueur1']:
            affichageTexte(choix_couleur1)
        else:
            affichageTexte(choix_couleur2)
        if positionRectangle(couleur_bleu):
            affichageRectangle(couleur_bleu)
        elif positionRectangle(couleur_vert):
            affichageRectangle(couleur_vert)
        elif positionRectangle(couleur_jaune):
            affichageRectangle(couleur_jaune)
        elif positionRectangle(couleur_rouge):
            affichageRectangle(couleur_rouge)
        affichageTexte(couleur_bleu)
        affichageTexte(couleur_vert)
        affichageTexte(couleur_jaune)
        affichageTexte(couleur_rouge)
    elif etatJeu['inMenuResolution']:
        if positionRectangle(reso_800_600):
            affichageRectangle(reso_800_600)
        elif positionRectangle(reso_1200_900):
            affichageRectangle(reso_1200_900)
        elif positionRectangle(reso_2400_1800):
            affichageRectangle(reso_2400_1800)
        affichageTexte(reso_800_600)
        affichageTexte(reso_1200_900)
        affichageTexte(reso_2400_1800)

def affichageTexteEnJeu():
    if etatJeu['enJeu']:
        afficheProjectile(scene_projectile)
        afficheScore()
    if etatJeu['Pause']:
        if positionRectangle(texte_back_menu):
            affichageRectangle(texte_back_menu)
        affichageTexte(texte_back_menu)
        affichageTexte(texte_pause)
    if not etatJeu['Pause']:
        if not enVie(vaisseau2) or not enVie(vaisseau1):
            if not enVie(vaisseau2):
                affichageTexte(texte_joueur1_win)
            else:
                affichageTexte(texte_joueur2_win)
            if positionRectangle(texte_revanche):
                affichageRectangle(texte_revanche)
            elif positionRectangle(texte_back_menu_fin_round):
                affichageRectangle(texte_back_menu_fin_round)
            affichageTexte(texte_revanche)
            affichageTexte(texte_back_menu_fin_round)

def afficheProjectile(scene):
    entites = acteurs(scene)
    for objet in entites:
        dessineProjectile(objet)

def affichageFondEcran(image):
    global compteur_fond_ecran
    if compteur_fond_ecran == 240:
        compteur_fond_ecran = 0
    if compteur_fond_ecran <= 30:
        fenetre.blit(image['poses']['image1'], (0, 0))
    elif compteur_fond_ecran > 30 and compteur_fond_ecran <= 60:
        fenetre.blit(image['poses']['image2'], (0, 0))
    elif compteur_fond_ecran > 60 and compteur_fond_ecran <= 90:
        fenetre.blit(image['poses']['image3'], (0, 0))
    elif compteur_fond_ecran > 90 and compteur_fond_ecran <= 120:
        fenetre.blit(image['poses']['image4'], (0, 0))
    elif compteur_fond_ecran > 120 and compteur_fond_ecran <= 150:
        fenetre.blit(image['poses']['image5'], (0, 0))
    elif compteur_fond_ecran > 150 and compteur_fond_ecran <= 180:
        fenetre.blit(image['poses']['image4'], (0, 0))
    elif compteur_fond_ecran > 180 and compteur_fond_ecran <= 210:
        fenetre.blit(image['poses']['image3'], (0, 0))
    elif compteur_fond_ecran > 210 and compteur_fond_ecran <= 240:
        fenetre.blit(image['poses']['image2'], (0, 0))

def afficheMunition():
    if not vaisseau1['munition']:
        affichageTexte(texte_rechargement1)
    else:
        for i in range(0, vaisseau1['munition']):
            mun = [FENETRE_LARGEUR/50 + i * FENETRE_LARGEUR/50,  FENETRE_HAUTEUR * 47/50, FENETRE_HAUTEUR/55, FENETRE_LARGEUR/40]
            pygame.draw.rect(fenetre, vaisseau1['couleur'], mun)
    if not vaisseau2['munition']:
        affichageTexte(texte_rechargement2)
    else:
        for i in range(0, vaisseau2['munition']):
            mun = [FENETRE_LARGEUR - FENETRE_LARGEUR/30 - i * FENETRE_LARGEUR/50, FENETRE_HAUTEUR * 47/50, FENETRE_HAUTEUR/55, FENETRE_LARGEUR/40]
            pygame.draw.rect(fenetre, vaisseau2['couleur'], mun)

def afficheAsteroide(scene):
    for asteroide in scene['acteurs']:
        dessine(asteroide, fenetre)

#---FIN Affichage---#

#---Santé---#

def initialisationSante():
    for vaisseau in (vaisseau1, vaisseau2):
        vaisseau['sante'] = SANTE_MAX
        vaisseau['munition'] = MUNITION_MAX

def degatsProjectiles(vaisseau):
    global compteur_invulnerabilite1, compteur_invulnerabilite2
    fin_match = finMatch()
    if vaisseau['sante'] != 0 and not finMatch():
        vaisseau['sante'] -= DEGATS_PROJECTILES
        vaisseau['toucher'] = True
        vaisseau['invincible'] = True
        if vaisseau['sante'] < 0:
            vaisseau['sante'] = 0
        if vaisseau['numero'] == 1:
            compteur_invulnerabilite1 = 0
        else:
            compteur_invulnerabilite2 = 0
    if vaisseau['sante'] == 0 and not fin_match:
        if vaisseau['numero'] == 1:
            augmenteScore(vaisseau2)
        else:
            augmenteScore(vaisseau1)

#@Alterne la visibilité du vaisseau afin de le faire clignoter à l'écran
#   lorsqu'un vaisseau se fait toucher. Enleve son invincibilité après le clignotement.
def clignotement(vaisseau, compteur):
    if compteur < 20 or (compteur > 40 and compteur <= 60) or (compteur > 80 and compteur <= 100):
        invisible(vaisseau)
    elif (compteur >= 20 and compteur <= 40) or (compteur > 60 and compteur <= 80):
        visible(vaisseau)
    elif compteur > 100 and compteur <= 120:
        visible(vaisseau)
        vaisseau['toucher'] = False
        vaisseau['invincible'] = False

#@Empêche, pendant un certain lapse de temps, les vaisseaux ayant été touchés de
#   reprendre des dégats.
def invulnerabilite():
    if vaisseau1['toucher']:
        clignotement(vaisseau1, compteur_invulnerabilite1)
    if vaisseau2['toucher']:
        clignotement(vaisseau2, compteur_invulnerabilite2)

#@Vérifie si la santé du vaisseau est supérieure à 0.
def enVie(vaisseau):
    if vaisseau['sante'] > 0:
        return True
    return False

#@Retourne la valeur de la santé actuelle de vaisseau.
def nombreSante(vaisseau):
    return int(vaisseau['sante'])

def affichageSante():
    for vaisseau in (vaisseau1, vaisseau2):
        sante = nombreSante(vaisseau)/100
        degat = 1-sante
        if vaisseau['numero'] == 1:
            if enVie(vaisseau1):
                mort1 =[-2 + FENETRE_LARGEUR/30 + (sante * FENETRE_LARGEUR/9), FENETRE_HAUTEUR/25, degat * FENETRE_LARGEUR/9, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, ROUGE, mort1)
                vie1 = [FENETRE_LARGEUR/30, FENETRE_HAUTEUR/25, FENETRE_LARGEUR/9 * sante, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, VERT, vie1)
            else:
                mort1 =[FENETRE_LARGEUR/30, FENETRE_HAUTEUR/25, FENETRE_LARGEUR/9, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, ROUGE, mort1)
        elif vaisseau['numero'] == 2:
            if enVie(vaisseau2):
                mort2 = [1 + FENETRE_LARGEUR - FENETRE_LARGEUR/30 - FENETRE_LARGEUR/9, FENETRE_HAUTEUR/25, degat * FENETRE_LARGEUR/9, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, ROUGE, mort2)
                vie2 = [FENETRE_LARGEUR - FENETRE_LARGEUR/30 - sante * FENETRE_LARGEUR/9, FENETRE_HAUTEUR/25,  sante * FENETRE_LARGEUR/9, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, VERT, vie2)
            else:
                mort2 = [FENETRE_LARGEUR - FENETRE_LARGEUR/30 - FENETRE_LARGEUR/9, FENETRE_HAUTEUR/25, FENETRE_LARGEUR/9, FENETRE_HAUTEUR/55]
                pygame.draw.rect(fenetre, ROUGE, mort2)

#@Retourne True si la santé d'un joueur est inférieure à 0.
def finMatch():
    return not enVie(vaisseau1) or not enVie(vaisseau2)

#---FIN Santé---#

#---fonctionnalité jeu---#

#@Empêche le joueur de tirer pendant un certaine nombre de passage par la fonction
#   si munition du vaisseau égal 0.

def gestionBonus():
    global moment_apparition_bonus, bonus, moment_prochain_bonus
    if moment_prochain_bonus['momentSuivant'] <= maintenant and not estVisible(bonus):
        creeBonus()
        moment_apparition_bonus = moment_prochain_bonus['momentSuivant']
    if estExpire(moment_prochain_bonus, maintenant):
        suivant(moment_prochain_bonus, maintenant)
    if estVisible(bonus):
        if moment_apparition_bonus + TEMPS_BONUS <= maintenant:
            invisible(bonus)
            bonus['position'] = [0, FENETRE_HAUTEUR * 2]
        dessine(bonus, fenetre)
        recupereBonus()

def creeBonus():
    global bonus
    bonus['position'][0] = random.randint(0, FENETRE_LARGEUR - BONUS_COTE)
    bonus['position'][1] = random.randint(0, FENETRE_HAUTEUR - BONUS_COTE)

    choix_pos = random.randint(1, 3)
    if choix_pos == 1:
        prendsPose(bonus, 'bonus_vie')
    elif choix_pos == 2:
        prendsPose(bonus, 'bonus_munition')
    elif choix_pos == 3:
        prendsPose(bonus, 'bonus_invincibilite')

def recupereBonus():
    bonus_centre = bonus
    bonus_centre['position'][0] += BONUS_COTE // 2
    bonus_centre['position'][1] += BONUS_COTE // 2
    for vaisseau in (vaisseau1, vaisseau2):
        if vaisseau['direction'] == 2 or vaisseau['direction'] == 6:
            if droitePositive(bonus_centre, vaisseau) and droiteNegative(bonus_centre, vaisseau):
                effet_bonus(vaisseau)
                invisible(bonus)
        elif vaisseau['direction'] == 4 or vaisseau['direction'] == 8:
            if droiteNegative(bonus_centre, vaisseau) and droitePositive(bonus_centre, vaisseau):
                effet_bonus(vaisseau)
                invisible(bonus)
        elif vaisseau['direction'] == 1 or vaisseau['direction'] == 5:
            if bonus_centre['position'][0] + BONUS_COTE // 2 > vaisseau['position'][0] and bonus_centre['position'][0] - BONUS_COTE // 2 < vaisseau['position'][0] + VAISSEAU_COURT:
                if bonus_centre['position'][1] + BONUS_COTE // 2 > vaisseau['position'][1] and bonus_centre['position'][1] - BONUS_COTE // 2 < vaisseau['position'][1] + VAISSEAU_LONG:
                    effet_bonus(vaisseau)
                    invisible(bonus)
        elif vaisseau['direction'] == 3 or vaisseau['direction'] == 7:
            if bonus_centre['position'][0] + BONUS_COTE // 2 > vaisseau['position'][0] and bonus_centre['position'][0] - BONUS_COTE // 2 < vaisseau['position'][0] + VAISSEAU_LONG:
                if bonus_centre['position'][1] + BONUS_COTE // 2 > vaisseau['position'][1] and bonus_centre['position'][1] - BONUS_COTE // 2 < vaisseau['position'][1] + VAISSEAU_COURT:
                    effet_bonus(vaisseau)
                    invisible(bonus)
    bonus_centre['position'][0] -= BONUS_COTE // 2
    bonus_centre['position'][1] -= BONUS_COTE // 2

def effet_bonus(vaisseau):
    powerup.play(sons['powerup'])
    if bonus['imageAffichee'] == bonus['poses']['bonus_vie']:
        bonusVie(vaisseau)
    elif bonus['imageAffichee'] == bonus['poses']['bonus_munition']:
        bonusMunition(vaisseau)
    elif bonus['imageAffichee'] == bonus['poses']['bonus_invincibilite']:
        bonusInvincibilite(vaisseau)

def rechargement():
    global compteur_munition1, compteur_munition2
    if vaisseau1['rechargement']:
        compteur_munition1 += 1
        if compteur_munition1 == 300:
            vaisseau1['munition'] = MUNITION_MAX
            vaisseau1['rechargement'] = False
    if vaisseau2['rechargement']:
        compteur_munition2 += 1
        if compteur_munition2 == 300:
            vaisseau2['munition'] = MUNITION_MAX
            vaisseau2['rechargement'] = False

def bonusVie(vaisseau):
    vaisseau['sante'] += 34
    if vaisseau['sante'] > 100:
        vaisseau['sante'] = SANTE_MAX

def bonusMunition(vaisseau):
    vaisseau['munition'] = MUNITION_MAX
    vaisseau['rechargement'] = False

def bonusInvincibilite(vaisseau):
    global compteur_invulnerabilite1, compteur_invulnerabilite2
    vaisseau['invincible'] = True
    vaisseau['toucher'] = True
    if vaisseau['numero'] == 1:
        compteur_invulnerabilite1 = 0
    else:
        compteur_invulnerabilite2 = 0

#---FIN fonctionnalité jeu---#

#---Sons---#
def initialisationSons():
    global sons, laser1, laser2, degat, powerup, click
    sons = {}
    sons['music_menu'] = pygame.mixer.Sound("music/musique_menu.wav")
    sons['music_jeu1'] = pygame.mixer.Sound("music/musique_jeu.wav")
    sons['victoire'] = pygame.mixer.Sound("music/victoire.wav")
    sons['piou_piou'] = pygame.mixer.Sound("bruitage/poui_poui.wav")
    sons['click'] = pygame.mixer.Sound("bruitage/click.wav")
    sons['degat'] = pygame.mixer.Sound("bruitage/degat.wav")
    sons['powerup'] = pygame.mixer.Sound("bruitage/powerup.wav")
    laser1 = pygame.mixer.Channel(5)
    laser2 = pygame.mixer.Channel(6)
    click = pygame.mixer.Channel(4)
    degat = pygame.mixer.Channel(3)
    powerup = pygame.mixer.Channel(7)

#@Gère le sons du jeu en fonction de où l'on se trouve dans le jeu.
def gestionSons():
    global musique_victoirec, musique_menuc, musique_jeuc
    if etatJeu['inMenu']:
        if musique_menuc:
            sons['music_jeu1'].stop()
            sons['music_menu'].play(loops=-1)
            musique_menuc = False
        musique_jeuc = True
    elif etatJeu['enJeu']:
        sons['music_menu'].stop()
        musique_menuc = True
        if musique_jeuc:
            sons['music_jeu1'].play(loops=-1)
            musique_victoirec = True
            musique_jeuc = False
        if finMatch():
            sons['music_jeu1'].stop()
            if musique_victoirec:
                sons['victoire'].play()
                musique_victoirec = False

#---FIN Sons---#

#---Score---#

#@Incrémente de 1, le score de vaisseau.
def augmenteScore(vaisseau):
    global texte_score1, texte_score2
    vaisseau['score'] += 1

    score1 = str(vaisseau1['score'])
    score2 = str(vaisseau2['score'])
    texte_score1 = nouveauMessage(score1, police_menu, vaisseau1['couleur'], 9)
    texte_score2 = nouveauMessage(score2, police_menu, vaisseau2['couleur'], 10)

#@Remets les scores des 2 vaisseaux à 0.
def reinitialiserScore():
    vaisseau1['score'] = 0
    vaisseau2['score'] = 0

def afficheScore():
    affichageTexte(texte_score1)
    affichageTexte(texte_score2)
    pygame.draw.rect(fenetre, GRIS, (FENETRE_LARGEUR//2 - FENETRE_LARGEUR//200, FENETRE_HAUTEUR // 80, FENETRE_LARGEUR // 100, texte_score1['messageH']))

#---FIN Score---#

#---Etat Jeu---#

#@Crée une bibliotèque qui reprend des booléens indiquant dans quel endroit du
#   jeu, on se trouve.
def nouvelEtatJeu():
    return{
    'fini': False,

    'inMenu': True,
    'inMenuIntro': True,
    'inMainMenu': False,
    'inMenuResolution': False,

    'inChoixCouleur': False,
    'choix_joueur1':False,

    'enJeu': False,

    'Pause': False
    }

#---FIN Etat Jeu---#


pygame.init()

pygame.mixer.init()

temps = pygame.time.Clock()

moment_prochain_asteroide = nouveauMomentAleatoire(INTERVALLE_ASTEROIDE)
moment_prochain_bonus = nouveauMomentAleatoire(INTERVALLE_BONUS)

fenetre_taille = [FENETRE_LARGEUR, FENETRE_HAUTEUR]
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('Space Fighter®')

etatJeu = nouvelEtatJeu()

initialisationSons()
initialisationVariables()
initialisationResolution()
initialisationVecteurU()

scene_projectile = nouvelleScene()
scene_asteroide = nouvelleScene()

commande_joueur1 = initialisationCommandeJoueur1()
commande_joueur2 = initialisationCommandeJoueur2()

gc = nouvelleGestionClavier()
initialisationRepeteTouche()

musique_jeuc = True
musique_menuc = True
musique_victoirec = True

sons['music_menu'].play(loops=-1)

while not etatJeu['fini']:
    compteur_fond_ecran += 1
    compteur_invulnerabilite1 += 1
    compteur_invulnerabilite2 += 1

    scan(gc)

    maintenant = pygame.time.get_ticks()
    position_souris = pygame.mouse.get_pos()

    affichageFondEcran(imageFond)
    traiteEntree()
    bruitagesRectangle()

    if etatJeu['inMenu']:
        gestionSons()
        affichageTexteMenu()
    elif etatJeu['enJeu']:
        gestionAsteroide()
        gestionSons()
        gestionBonus()

        majProjectiles(scene_projectile)

        majVaisseau(scene_vaisseau)
        collisions(vaisseau1, vaisseau2)
        invulnerabilite()
        rechargement()

        afficheVaisseau(scene_vaisseau, fenetre)
        affichageSante()
        affichageTexteEnJeu()
        afficheMunition()

    pygame.display.flip()
    temps.tick(60)

sons['music_menu'].stop()
sons['music_jeu1'].stop()
pygame.display.quit()
pygame.quit()
exit()
