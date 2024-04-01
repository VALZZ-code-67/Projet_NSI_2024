import pygame
import sys
import os
import random as rd
import math
from pygame import mixer

#Base
path = os.getcwd()
os.chdir(path)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
LARGEUR , HAUTEUR = 1000 , 660
ecran = pygame.display.set_mode((LARGEUR , HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Spaceship Attack")
FPS = 60
texte_final_font = pygame.font.SysFont('Verdana', 70, True)
score_final_font = pygame.font.SysFont('Verdana', 40, True)
score_font = pygame.font.SysFont('Verdana', 30, False)
parametre_font = pygame.font.SysFont('Verdana', 25, False)

z_image = pygame.image.load('Fichiers/images/z.png')

q_image = pygame.image.load('Fichiers/images/q.png')

s_image = pygame.image.load('Fichiers/images/s.png')

d_image = pygame.image.load('Fichiers/images/d.png')

espace_image = pygame.image.load('Fichiers/images/espace.png')

echap_image = pygame.image.load('Fichiers/images/echap.png')

entrer_image = pygame.image.load('Fichiers/images/entrer.png')

text_image = pygame.image.load('Fichiers/images/text.png')

separation_image = pygame.image.load('Fichiers/images/separation.png')

banniere_parametre_image = pygame.image.load('Fichiers/images/banner_setting.png')

parametre_bouton_image = pygame.image.load('Fichiers/images/setting.png')

retour_bouton_image = pygame.image.load('Fichiers/images/back.png')

image_bouton_rejouer = pygame.image.load("Fichiers/Images/bouton_rejouer.png") #57x13

image_bouton_quitter = pygame.image.load("Fichiers/Images/bouton_quitter.png") #57x13

image_bouton_plus = pygame.image.load("Fichiers/Images/bouton_plus.png") #50x50

image_bouton_moins = pygame.image.load("Fichiers/Images/bouton_moins.png") #50x50

image_bouton_jouer = pygame.image.load('Fichiers/images/bouton_jouer_menu.png') #45x13

image_bouton_menu = pygame.image.load('Fichiers/images/bouton_menu_pause.png') #45x13

terre_image = pygame.image.load('Fichiers/images/image_terre.png')

victoire_image = pygame.image.load('Fichiers/images/victoire.png')

#Couleurs
BLANC = (255,255,255)
NOIR = (0,0,0)
ROUGE = (255,0,0)
VERT = (0,255,0)
BLEU = (0,0,255)
GRIS = (127,127,127)
JAUNE = (255,255,0)

#Sons
pygame.mixer.set_num_channels(60)

son_tir = pygame.mixer.Sound("Fichiers/Sons/tir.wav")
son_amelioration = pygame.mixer.Sound("Fichiers/Sons/upgrade.wav")
son_bouclier = pygame.mixer.Sound("Fichiers/Sons/bouclier.wav")
son_ouvrir_menu = pygame.mixer.Sound("Fichiers/Sons/ouvrir_menu.wav")
son_fermer_menu = pygame.mixer.Sound("Fichiers/Sons/fermer_menu.mp3")
son_soin = pygame.mixer.Sound("Fichiers/Sons/soin.wav")
son_missile_guide_pret = pygame.mixer.Sound("Fichiers/Sons/notif.wav")
son_niveau = pygame.mixer.Sound("Fichiers/Sons/niveau.wav")
son_explosion_1 = pygame.mixer.Sound("Fichiers/Sons/explosion_1.wav")
son_explosion_2 = pygame.mixer.Sound("Fichiers/Sons/explosion_2.wav")
son_alerte_1 = pygame.mixer.Sound("Fichiers/Sons/alerte_1.mp3")
son_jouer_clique = pygame.mixer.Sound("Fichiers/Sons/jouer_clique.mp3")
son_standard_clique = pygame.mixer.Sound("Fichiers/Sons/clique.mp3")
son_menu_clique = pygame.mixer.Sound("Fichiers/Sons/menu_son.mp3")
son_reprendre_clique = pygame.mixer.Sound("Fichiers/Sons/jouer_clique2.mp3")
son_arrier_plan = pygame.mixer.Sound("Fichiers/Sons/musique_de_fond.mp3")
son_game_over = pygame.mixer.Sound("Fichiers/Sons/game_over.mp3")

class Jeu:
    """Classe principale ayant comme attribut tous les elements du jeu"""
    def __init__(self,LARGEUR,HAUTEUR,FPS,SCORE = 0,NIVEAU = 1):
        self.largeur = LARGEUR
        self.hauteur = HAUTEUR
        self.fps = FPS
        self.fond = pygame.image.load("Fichiers/Images/fond_espace.png").convert()
        self.defile = 0
        self.defile_planete = 0
        #Vague
        self.vague_active = True
        self.vague_delai = 0
        self.vague_quota = 40
        self.vague_progression = 0
        self.vague = 1
        self.vague_meteorite = False
        self.vague_boss = False
        self.combat_boss = False
        self.boss_actuel = 0
        self.alerte_active = True
        self.meteorite_delai = 0
        self.coeffs = [[50,0,0,0,0,0,0,0] , [37,13,0,0,0,0,0,0] , [15,25,10,0,0,0,0,0] , [12,18,10,10,0,0,0,0] , [10,15,10,8,7,0,0,0] , [10,13,10,10,10,7,0,0] , [0,0,0,0,5,15,30,0] , [0,0,0,0,0,15,20,15]]
        #Score
        self.score = SCORE
        self.meilleur_score = 0
        #Objets
        self.chance_de_soin = 0
        self.chance_de_projectiles = 4
        self.chance_de_bouclier = 3
        self.chance_de_joueur_2 = 0
        self.objet_joueur_2_actif = True
        self.chance_de_vitesse = 2
        self.chance_de_ulti = 1
        #Texte
        self.end_text = texte_final_font.render(f'Vous avez perdu !', True, ROUGE, None)
        self.end_textx_size = self.end_text.get_width()
        self.end_texty_size = self.end_text.get_height()
        self.texte_score_final = score_final_font.render(f'Votre score: {self.score}', True, ROUGE, None)
        #Niveaux
        self.niveau = NIVEAU
        self.exp = 0
        self.points_ameliorations = 0
        #Joueur
        self.groupe_joueur = pygame.sprite.Group()
        self.joueur = Joueur()
        self.groupe_joueur.add(self.joueur)
        #Ennemis
        self.groupe_ennemi = pygame.sprite.Group()
        #Projectiles
        self.groupe_projectiles_joueur = pygame.sprite.Group()
        self.groupe_projectiles_ennemis = pygame.sprite.Group()
        self.projectile_ennemi_8 = True
        #Explosions
        self.groupe_explosions = pygame.sprite.Group()
        #Meteorites
        self.groupe_meteorites = pygame.sprite.Group()
        #Menu ameliorations
        self.menu_ameliorations = Menu_ameliorations()
        #Objets
        self.groupe_objets = pygame.sprite.Group()
        #Autres
        self.groupe_autre = pygame.sprite.Group()
        #Menu pause
        self.menu_pause = Menu_pause()
        #Menu dev
        self.menu_developpeur = Menu_developpeur()
        #Menu
        self.menu = Menu()

        self.victoire = False
    #Rejouer
    def nouvelle_partie(self,ETAT_MENU):
        """Methode permettant de recommencer à 0"""
        global JEU
        JEU = Jeu(self.largeur, self.hauteur, self.fps)
        JEU.meilleur_score = self.meilleur_score
        JEU.menu.est_actif = ETAT_MENU
    #VAGUE METEORITES
    def creer_vague_meteorites(self):
        """Methode permettant de creer des vagues de meteorites"""
        if self.alerte_active:
            self.groupe_autre.add(Alerte())
            self.alerte_active = False
        self.joueur.tire = False
        self.meteorite_delai += 1
        #Debut des vagues
        if 300 <= self.meteorite_delai <= 900:
            mode_apparition = rd.choices(["aleatoire","precis"], weights = [4,1])
            nombre_meteorites = rd.randint(1,3)
            if self.meteorite_delai % 30 == 0:
                for _ in range(nombre_meteorites):
                    y = rd.randint(-361,-100)
                    if mode_apparition[0] == "aleatoire":
                        x = rd.randint(61, JEU.largeur-61)
                        for meteorite in self.groupe_meteorites:
                            if meteorite.x-61 < x < meteorite.x+61 and meteorite.y-141<y<meteorite.y+141:
                                decalage = rd.choices([-180,-80,80,180])
                                x += decalage[0]
                    else:
                        x = JEU.joueur.x
                        mode_apparition[0] = "aleatoire"
                    self.groupe_meteorites.add(Meteorite(x,y))
        #Fin des vagues
        elif self.meteorite_delai >= 1000:
            self.meteorite_delai = 0
            self.vague_active = True
            self.vague_meteorite = False
            self.alerte_active = True
            self.joueur.tire = True
    #VAGUE
    def creer_vague(self):
        """Methode permettant de creer des vagues d'ennemis"""
        if not self.victoire:
            liste_boss = [Boss_1(),Boss_2()]
            if self.vague_active and self.vague_progression >= self.vague_quota:
                self.vague += 1
                self.vague_progression = 0
                self.vague_active = False
            if not self.vague_active and len(JEU.groupe_ennemi)==0:
                self.vague_meteorite = True
            if self.vague_meteorite:
                self.creer_vague_meteorites()
            if self.vague % 5 == 0 and self.vague_active:
                self.vague_boss = True
            if self.vague_boss == False and self.vague_active:
                nombre_ennemis = rd.randint(4,8)
                seconde_vague = rd.choices([True,False] , weights = [1,4]) #seconde_vague = list  |  P(True) = 1/5 | P(False) = 4/5
                ecart_aleatoire = rd.randint(50 , self.largeur//8)
                r = self.largeur/2 - 50*(nombre_ennemis/2 + 3) + ecart_aleatoire
                decalage = 50
                y = 0
                self.vague_progression += nombre_ennemis
                for _ in range(nombre_ennemis):
                    nouveaux_ennemis = rd.choices([Ennemi_1(r,y),Ennemi_2(r,y),Ennemi_3(r,y),Ennemi_4(r,y),Ennemi_5(r,y),Ennemi_6(r,y),Ennemi_7(r,y),Ennemi_8(r,y)] , weights = self.coeffs[self.vague-1-self.boss_actuel])
                    nouvel_ennemi = nouveaux_ennemis[0]
                    r += 50 + decalage
                    self.groupe_ennemi.add(nouvel_ennemi)
                if seconde_vague[0]:
                    x = 75/2
                    y = -75-30
                    nombre_ennemis = rd.randint(4,8)
                    self.vague_progression += nombre_ennemis
                    for _ in range(nombre_ennemis):
                        nouveaux_ennemis = rd.choices([Ennemi_1(r-x,y),Ennemi_2(r-x,y),Ennemi_3(r-x,y),Ennemi_4(r-x,y),Ennemi_5(r-x,0),Ennemi_6(r-x,0),Ennemi_7(r-x,y),Ennemi_8(r-x,y)] , weights = self.coeffs[self.vague-1-self.boss_actuel])
                        nouvel_ennemi = nouveaux_ennemis[0]
                        r -= 50 + decalage
                        self.groupe_ennemi.add(nouvel_ennemi)
                if self.vague_progression >= self.vague_quota:
                    self.vague_progression = self.vague_quota
            elif self.vague_boss and (len(self.groupe_ennemi) == 0) and self.vague_active:
                self.vague_boss = False
                self.combat_boss = True
                self.vague_active = False
                self.groupe_ennemi.add(liste_boss[self.boss_actuel])
                if self.boss_actuel == 0:
                    self.boss_actuel += 1
    #PLANETE DE FIN 
    def planete (self):
        '''
        Cette méthode est lancée dès que le dernier boss est vaincu 
        et permet de stopper l'arrivée des vagues afin de laisser place à un écran
        de victoire.
        '''
        self.joueur.rect.center = (self.largeur/2, 3*self.hauteur/4)
        hauteur_milieu = HAUTEUR/8
        self.defile_planete += 1 
        for i in range(1):
            if (self.defile_planete-i*(terre_image.get_height())-terre_image.get_height()) < hauteur_milieu:
                ecran.blit(terre_image, (LARGEUR/4 , (self.defile_planete-i*(terre_image.get_height()))-terre_image.get_height()))
                self.groupe_joueur.draw(ecran)
            else:
                if self.joueur.est_vivant:
                    self.joueur.kill()
                if self.score > self.meilleur_score:
                    self.meilleur_score = self.score
                ecran.blit(terre_image, (LARGEUR/4 , hauteur_milieu))
                self.texte_score_final = score_final_font.render(f'Votre score: {self.score}', True, ROUGE, None)
                self.texte_meilleur_score_final = score_final_font.render(f'Meilleur score: {self.meilleur_score}', True, (255,0,255), None)
                ecran.blit(self.texte_meilleur_score_final,(0.3*LARGEUR/10,0.5*HAUTEUR/10))
                ecran.blit(self.texte_score_final,(0.3*LARGEUR/10,1.5*HAUTEUR/10))
                ecran.blit(victoire_image,(2.5*LARGEUR/10,0.5*HAUTEUR/10))

                bouton_menu_victoire.draw()
                bouton_rejouer_victoire.draw()
                bouton_quitter_victoire.draw()

                if bouton_quitter_victoire.est_clique():
                    pygame.quit()
                    sys.exit()
                if bouton_menu_victoire.est_clique():
                    canal_libre = pygame.mixer.find_channel()
                    canal_libre.play(son_menu_clique)
                    JEU.nouvelle_partie(True)
                if bouton_rejouer_victoire.est_clique():
                    canal_libre = pygame.mixer.find_channel()
                    canal_libre.play(son_reprendre_clique)
                    JEU.nouvelle_partie(False)
    #BARRE D'EXP
    def progression(self):
        """Methode permettant de monter de niveau et renvoie le pourcentage de progression"""
        quota = 2*self.niveau+8
        pourcentage = self.exp/quota
        if pourcentage >= 1:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_niveau)
            #pygame.mixer.Sound.play(son_niveau)
            self.niveau += 1
            self.points_ameliorations += 2
            self.exp = 0
        return pourcentage
    
    def update(self):
        """Methode permettant d'actualiser le jeu"""
        #vague
        self.vague_delai += 1
        if (self.vague+1) % 5 == 0:
            if len(self.groupe_ennemi) == 0:
                self.creer_vague()
        elif len(self.groupe_ennemi) == 0 or self.vague_delai >= 8*FPS and not self.vague_boss:
            self.creer_vague()
            self.vague_delai = 0

        #affichage
        self.defile += 0.75
        for i in range(2):
            ecran.blit(self.fond, (0 , self.defile-i*(self.fond.get_height()))) 
        if self.defile > self.hauteur:
            self.defile = 0

        if self.joueur.est_vivant and not self.menu_ameliorations.est_actif and not self.victoire:
            self.groupe_explosions.draw(ecran)
            self.groupe_projectiles_joueur.draw(ecran)
            self.groupe_projectiles_ennemis.draw(ecran)
            self.groupe_joueur.draw(ecran)
            self.groupe_ennemi.draw(ecran)
            self.groupe_objets.draw(ecran)
            self.groupe_meteorites.draw(ecran)
            self.groupe_autre.draw(ecran)
            self.groupe_explosions.update()
            self.groupe_joueur.update()
            self.groupe_ennemi.update()
            self.groupe_projectiles_joueur.update()
            self.groupe_projectiles_ennemis.update()
            self.groupe_objets.update()
            self.groupe_meteorites.update()
            self.groupe_autre.update()
            #ATH
                #VIE
            texte_vie_pos_depart = 3*self.largeur/4
            texte_vie_pos_fin = texte_vie_pos_depart + ((self.joueur.vie*100)/self.joueur.vie_max)*2
            pygame.draw.line(ecran , GRIS , (texte_vie_pos_depart-10 , 50) , (texte_vie_pos_depart+210 , 50) , 45) # Grey fond
            pygame.draw.line(ecran , NOIR , (texte_vie_pos_depart , 50) , (texte_vie_pos_depart+200 , 50) , 30) # Black line
            if texte_vie_pos_fin > texte_vie_pos_depart:
                pygame.draw.line(ecran , VERT , (texte_vie_pos_depart , 50) , (texte_vie_pos_fin , 50) , 30) # Green line = vie
            texte_vie = score_font.render(f'{int(JEU.joueur.vie):3d} / {JEU.joueur.vie_max}', True, BLANC, None)
            ecran.blit(texte_vie, (texte_vie_pos_depart+100-texte_vie.get_width()/2 , 50-texte_vie.get_height()/2))
                #SCORE
            texte_score = score_font.render(f'Score: {JEU.score}', True, BLANC, None)
            ecran.blit(texte_score, (0,0))
                #NIVEAUX + EXP
            texte_niveau = score_final_font.render(f'Niveau: {self.niveau}', True , JAUNE , None)
            texte_niveau_y = 0 + texte_niveau.get_height()
            ecran.blit(texte_niveau, (0 , texte_niveau_y))
            texte_exp_pos_depart = 10
            pourcentage = self.progression()
            texte_exp_pos_y = texte_niveau_y + 100
            pygame.draw.line(ecran , GRIS , (texte_exp_pos_depart-10 , texte_exp_pos_y) , (texte_exp_pos_depart+165 , texte_exp_pos_y) , 45)
            pygame.draw.line(ecran , NOIR , (texte_exp_pos_depart , texte_exp_pos_y) , (texte_exp_pos_depart+155 , texte_exp_pos_y) , 30)
            if pourcentage > 0.01:
                pygame.draw.line(ecran , JAUNE , (texte_exp_pos_depart , texte_exp_pos_y) , (pourcentage*(texte_exp_pos_depart+155), texte_exp_pos_y) , 30)
            texte_exp = score_font.render(f'{JEU.exp:2d} / {2*self.niveau+8:2d}', True, BLANC, None)
            ecran.blit(texte_exp, (texte_exp_pos_depart+78-texte_exp.get_width()/2 , texte_exp_pos_y-texte_exp.get_height()/2))
                #Vague
            texte_vague = score_font.render(f'Vague: {JEU.vague:2d}', True, BLEU, None)
            texte_vague_x = texte_vague.get_width()
            texte_vague_pos_depart = self.largeur/2 - 83
            texte_vague_y = texte_vague.get_height()+20
            ecran.blit(texte_vague , (self.largeur/2 - texte_vague_x/2, 0))
            pygame.draw.line(ecran , GRIS , (texte_vague_pos_depart-10 , texte_vague_y) , (texte_vague_pos_depart+165 , texte_vague_y) , 45)
            pygame.draw.line(ecran , NOIR , (texte_vague_pos_depart , texte_vague_y) , (texte_vague_pos_depart+155 , texte_vague_y) , 30)
            if self.vague_progression > 1:
                pygame.draw.line(ecran , BLEU , (texte_vague_pos_depart , texte_vague_y) , (texte_vague_pos_depart+(self.vague_progression/self.vague_quota)*155, texte_vague_y) , 30)
                #MENU AMELIORATIONS
            self.menu_ameliorations.update()

        #ECRAN DE FIN SI LE JOUEUR GAGNE
        elif not self.menu_ameliorations.est_actif and self.victoire:
            self.planete()

        #ECRAN DE FIN
        elif not self.victoire:
            #COULEUR DE L'ECRAN
            ecran.fill((80,30,30))
            #ACTUALISATION DU SCORE
            if self.score > self.meilleur_score:
                self.meilleur_score = self.score
            #TEXTE
            self.texte_score_final = score_final_font.render(f'Votre score: {self.score}', True, ROUGE, None)
            self.texte_score_final_taille_x = self.texte_score_final.get_width()
            self.texte_score_final_taille_y = self.texte_score_final.get_height()
            self.texte_meilleur_score_final = score_final_font.render(f'Meilleur score: {self.meilleur_score}', True, (255,0,255), None)
            end_best_score_textx_size = self.texte_meilleur_score_final.get_width()
            ecran.blit(self.end_text, (self.largeur/2-self.end_textx_size/2 , 1*self.hauteur/4-self.end_texty_size/2))
            ecran.blit(self.texte_score_final, (self.largeur/2-self.texte_score_final_taille_x/2 , 2*self.hauteur/5-self.texte_score_final_taille_y/2))
            ecran.blit(self.texte_meilleur_score_final, (self.largeur/2-end_best_score_textx_size/2 , 2*self.hauteur/5+self.texte_score_final_taille_y/2))
            bouton_rejouer.draw()
            bouton_quitter.draw()
            if bouton_rejouer.est_clique():
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_reprendre_clique)
                self.nouvelle_partie(False)

            elif bouton_quitter.est_clique():
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_menu_clique)
                self.nouvelle_partie(True)  
            
        pygame.display.flip() #update
        clock.tick(self.fps)
        
def normalise_vecteur(x, y):
    norme = get_norme(x,y)
    return x/norme, y/norme

def get_norme(x,y):
    return math.sqrt(x*x + y*y)

class Bouton:
    """Classe Bouton"""
    def __init__(self, x , y , image , scale = 1):
        self.largeur = image.get_width()
        self.hauteur = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.largeur * scale) , int(self.hauteur * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        self.clique = False
    def draw(self):
        """Methode permettant l'affichage"""
        ecran.blit(self.image , (self.rect.x , self.rect.y))
    def est_clique(self):
        """Methode qui renvoie True si on a clique sur le bouton et False dans le cas echeant"""
        action = False
        pos_souris = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_souris):
            if pygame.mouse.get_pressed()[0] and self.clique == False:
                self.clique = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clique = False
        return action


class Joueur(pygame.sprite.Sprite):
    """Classe du joueur"""
    def __init__(self):
        super().__init__()
        self.x = LARGEUR/2
        self.y = 3*HAUTEUR/4
        self.image = pygame.image.load("Fichiers/Images/joueur1_1.png").convert_alpha() #pygame.Surface((50,75))
        self.image_originale = self.image
        self.image_largeur = self.image.get_width()
        self.image_hauteur = self.image.get_height()
        self.rect = self.image.get_rect(center = (LARGEUR/2 , HAUTEUR/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.vie = 100
        self.vie_max = 100
        self.degats = 25
        self.est_vivant = True
        self.delai = 0
        self.cadence_de_tir = 30
        self.nombre_projectiles = 1
        self.delai_invincibilite = 30
        self.est_paralyse = False
        self.paralyse_delai = 0
        self.missile_guide_actif = False
        self.missile_guide_delai = 0
        self.tire = True
        self.angle = 90
        self.boost_vitesse_actif = False
        self.vitesse = 6
        self.boost_vitesse = 2
        self.compteur_boost_vitesse = 600
        self.index_image = 1
        self.nombre_joueur = 1
        self.boost_ulti_actif = False
        self.compteur_boost_ulti = 300
    def deplace(self,DX,DY):
        """Methode permettant le deplacement du joueur"""
        if not self.est_paralyse:
            if -(self.vitesse+25)*DX < self.x < LARGEUR -(self.vitesse+30)*DX:
                self.x += DX * self.vitesse
            if -(self.vitesse+45)*DY < self.y < HAUTEUR -(self.vitesse+55)*DY:
                self.y += DY * self.vitesse
    def update(self):
        """Methode permettant l'actualisation du joueur"""
        if self.index_image < 3:
            self.index_image += 1
        else:
            self.index_image = 1
        self.image = pygame.image.load(f"Fichiers/Images/joueur{self.nombre_joueur}_{self.index_image}.png").convert_alpha()
        if self.boost_vitesse_actif:
            self.compteur_boost_vitesse -= 1
            if self.compteur_boost_vitesse <= 0:
                self.boost_vitesse_actif = False
                self.compteur_boost_vitesse = 300
                JEU.chance_de_vitesse = 2
                self.vitesse -= self.boost_vitesse
        if self.boost_ulti_actif:
            self.compteur_boost_ulti -= 1
            if self.compteur_boost_ulti <= 0:
                self.boost_ulti_actif = False
                JEU.joueur.nombre_projectiles -= 5
                JEU.joueur.vie_max -= 50
                if JEU.joueur.vie > 50:
                    JEU.joueur.vie -= 50
                JEU.joueur.degats -= 50
                JEU.joueur.cadence_de_tir += 5
                self.compteur_boost_ulti = 600
                JEU.chance_de_ulti = 1
        if not self.missile_guide_actif:
            self.missile_guide_delai += 1
        self.combat_boss()
        if self.tire:
            self.tire_projectile()
            if pygame.mouse.get_pressed()[0] and self.missile_guide_delai >= 100 and not self.missile_guide_actif:
                JEU.groupe_projectiles_joueur.add(Missile_guide())
                self.missile_guide_delai = 0
                self.missile_guide_actif = True
            if self.missile_guide_delai == 100:
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_missile_guide_pret)
        if self.vie <= 0:
            self.vie = 0
            self.explose()
            self.est_vivant = False
        self.rect.center = (self.x , self.y)
        self.mask = pygame.mask.from_surface(self.image)
        for ennemi in JEU.groupe_ennemi:
            if self.rect.colliderect(ennemi.rect) and self.delai_invincibilite >= 30 and ennemi.fait_degats_collision:
                if self.mask.overlap(ennemi.mask, (ennemi.x-self.x , ennemi.y-self.y)):
                    self.delai_invincibilite = 0
                    self.vie -= ennemi.degats_collision
                    if isinstance(ennemi, Ennemi):
                        ennemi.explose()
        self.delai_invincibilite += 1
        self.delai += 1
        if self.est_paralyse:
            self.paralyse_delai -= 1
            if self.paralyse_delai <= 0:
                self.est_paralyse = False
    def tire_projectile(self):
        """Methode permettant de tirer des projectiles"""
        if self.delai >= self.cadence_de_tir:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_tir)
            self.delai = 0
            decalage = 9*2
            nombre = self.nombre_projectiles//2
            nombre_impair = self.nombre_projectiles%2 == 1
            if nombre_impair:
                if not JEU.combat_boss:
                    projectile = Projectile_joueur(self.x, self.y - self.image_hauteur/2, self.angle)
                else:
                    projectile = Projectile_joueur(self.x, self.y, self.angle)
                JEU.groupe_projectiles_joueur.add(projectile)
                decalage = 9*2*2
            for _ in range(nombre):
                if not JEU.combat_boss:
                    projectile_1 = Projectile_joueur(self.x + decalage, self.y - self.image_hauteur/2, self.angle)
                    projectile_2 = Projectile_joueur(self.x - decalage, self.y - self.image_hauteur/2, self.angle)
                else:
                    projectile_1 = Projectile_joueur(self.x + decalage, self.y, self.angle)
                    projectile_2 = Projectile_joueur(self.x - decalage, self.y, self.angle)
                JEU.groupe_projectiles_joueur.add(projectile_1)
                JEU.groupe_projectiles_joueur.add(projectile_2)
                decalage += 9*2*2
    def combat_boss(self):
        """Methode permettant de mettre à jour le mode de tir si on combat un boss"""
        if JEU.combat_boss:
            pos = pygame.mouse.get_pos()
            x_dist = pos[0] - self.x
            y_dist = -(pos[1] - self.y)
            self.angle = math.degrees(math.atan2(y_dist, x_dist))
            self.image = pygame.transform.rotate(self.image_originale, self.angle - 90)
            self.rect = self.image.get_rect(center = (self.x,self.y))
            self.mask = pygame.mask.from_surface(self.image)
    def paralyse(self,duration):
        """Methode permettant d'immobiliser le joueur"""
        self.est_paralyse = True
        self.paralyse_delai = duration
    def explose(self):
        """Methode permettant de faire exploser le joueur lors de la mort"""
        mixer.music.set_volume(0)
        self.kill()
        self.est_vivant = False
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (300,300), 7))
        if not JEU.victoire:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_game_over)

class Joueur_2(Joueur):
    """Classe fille de Joueur"""
    def __init__(self,args):
        super().__init__()
        self.x = JEU.joueur.x
        self.y = JEU.joueur.y
        self.image = pygame.image.load("Fichiers/Images/joueur2_1.png").convert_alpha() #pygame.Surface((50,75))
        self.image_originale = self.image
        self.image_largeur = self.image.get_width()
        self.image_hauteur = self.image.get_height()
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.degats = args[0]
        self.vie = args[1]
        self.vie_max = args[2]
        self.est_vivant = True
        self.delai = 0
        self.cadence_de_tir = args[3]
        self.nombre_projectiles = 3
        self.delai_invincibilite = 30
        self.est_paralyse = False
        self.paralyse_delai = 0
        self.missile_guide_actif = False
        self.missile_guide_delai = 0
        self.tire = True
        self.angle_diff = 5
        self.nombre_joueur = 2
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_tir)
            self.delai = 0
            decalage = 9*2
            nombre = self.nombre_projectiles//2
            nombre_impair = self.nombre_projectiles%2 == 1
            if nombre_impair:
                if not JEU.combat_boss:
                    projectile = Projectile_joueur(self.x, self.y - self.image_hauteur/2, self.angle)
                else:
                    projectile = Projectile_joueur(self.x, self.y, self.angle)
                JEU.groupe_projectiles_joueur.add(projectile)
                decalage = 9*2*2
            for _ in range(nombre):
                if not JEU.combat_boss:
                    self.angle = 90
                    projectile_1 = Projectile_joueur(self.x + decalage, self.y - self.image_hauteur/2 , self.angle - self.angle_diff)
                    projectile_2 = Projectile_joueur(self.x - decalage, self.y - self.image_hauteur/2 , self.angle + self.angle_diff)
                else:
                    projectile_1 = Projectile_joueur(self.x + decalage, self.y, self.angle - self.angle_diff)
                    projectile_2 = Projectile_joueur(self.x - decalage, self.y, self.angle + self.angle_diff)
                JEU.groupe_projectiles_joueur.add(projectile_1)
                JEU.groupe_projectiles_joueur.add(projectile_2)
                decalage += 9*2*2

#EN COURS DE DEVELOPPEMENT
class Joueur_3(Joueur):
    """Classe fille de joueur"""
    def __init__(self):#,args):
        super().__init__()
        self.x = 500#JEU.joueur.x
        self.y = 300#JEU.joueur.y
        self.image = pygame.image.load("Fichiers/Images/joueur1_1.png").convert_alpha() #pygame.Surface((50,75))
        self.image_originale = self.image
        self.image_largeur = self.image.get_width()
        self.image_hauteur = self.image.get_height()
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.vie =1000#args[2]
        self.vie_max = 1000#args[1]
        self.degats = 50#args[0]
        self.cadence_de_tir = 5#args[3] - 10
        self.nombre_projectiles = 3
        self.delai_invincibilite = 30
        self.angle_diff = 3
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir:
            #pygame.mixer.music.stop()
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_tir)
            #pygame.mixer.Sound.play(son_tir)
            self.delai = 0
            decalage = 9*2
            nombre = self.nombre_projectiles//2
            nombre_impair = self.nombre_projectiles%2 == 1
            if nombre_impair:
                projectile = Lance_flammes(self.angle)
                JEU.groupe_projectiles_joueur.add(projectile)
                decalage = 9*2*2
            for _ in range(nombre):
                if not JEU.combat_boss:
                    self.angle = 90
                projectile_1 = Lance_flammes(self.angle - self.angle_diff )
                projectile_2 = Lance_flammes(self.angle + self.angle_diff )
                JEU.groupe_projectiles_joueur.add(projectile_1)
                JEU.groupe_projectiles_joueur.add(projectile_2)
                decalage += 9*2*2

class Projectile_joueur(pygame.sprite.Sprite):
    """Classe des projectiles du joueur"""
    def __init__(self , x , y, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.degats = JEU.joueur.degats
        self.vitesse = 10
        self.angle_degree = angle
        self.angle_radians = math.radians(angle)
        self.dx = math.cos(self.angle_radians)*self.vitesse
        self.dy = math.sin(self.angle_radians)*self.vitesse
        if isinstance(JEU.joueur, Joueur_2):
            self.image = pygame.image.load(f"Fichiers/Images/projectile_joueur_2.png") #10x20
            self.image = pygame.transform.rotate(self.image, self.angle_degree+270)
            self.image = pygame.transform.scale(self.image, (20,40))
        else:
            self.image = pygame.image.load(f"Fichiers/Images/projectile_joueur_1.png")
            self.image = pygame.transform.rotate(self.image, self.angle_degree+270)
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.compteur = 300
    def update(self):
        """Methode d'actualisation des projectiles"""
        self.compteur -= 1
        self.x += self.dx
        self.y -= self.dy
        self.rect.center = (self.x, self.y)
        if self.compteur <= 0:
            self.kill()
        for ennemi in JEU.groupe_ennemi:
            if self.rect.colliderect(ennemi.rect): #if there is collision with ennemi
                if self.mask.overlap(ennemi.mask, (ennemi.rect.x-self.x , ennemi.rect.y-self.y)):
                    self.explose()
                    ennemi.vie -= self.degats
    def explose(self):
        """Methode permettant l'explosion des projectiles à l'impact"""
        pygame.mixer.Sound.play(son_explosion_2)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (100,100), 2))

class Missile_guide(pygame.sprite.Sprite):
    """Classe du missile guide du joueur"""
    def __init__(self):
        super().__init__()
        self.x = JEU.joueur.x
        self.y = JEU.joueur.y
        self.degats = JEU.joueur.degats + 50
        self.vitesse = 8
        self.image = pygame.image.load("Fichiers/Images/missile_guide.png")
        self.image = pygame.transform.scale(self.image, (20,50))
        self.image_originale = self.image
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.delai = 0
    def update(self):
        """Methode permettant l'actualisation du missile"""
        pos = pygame.mouse.get_pos()
        self.cible = normalise_vecteur(pos[0] - self.x, pos[1] - self.y)
        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        if get_norme(pos[0] - self.x, pos[1] - self.y) >= 8:
            self.image = pygame.transform.rotate(self.image_originale, self.angle+90)
            self.mask = pygame.mask.from_surface(self.image)
            self.x += self.cible[0] * self.vitesse
            self.y += self.cible[1] * self.vitesse
            self.rect = self.image.get_rect(center = (self.x , self.y))
        for ennemi in JEU.groupe_ennemi:
            if self.rect.colliderect(ennemi.rect):
                if self.mask.overlap(ennemi.mask, (ennemi.rect.x-self.rect.x , ennemi.rect.y-self.rect.y)):
                    self.explose()
                    ennemi.vie -= self.degats
        for projectile in JEU.groupe_projectiles_ennemis:
            if self.rect.colliderect(projectile.rect):
                if self.mask.overlap(projectile.mask, (projectile.x-self.rect.x , projectile.y-self.rect.y)):
                    self.explose()
                    projectile.explose()
    def explose(self):
        """Methode permettant l'explosion du missile à l'impact"""
        JEU.joueur.missile_guide_actif = False
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_2)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (100,100), 2))

#EN COURS DE DEVELOPPEMENT
class Lance_flammes(pygame.sprite.Sprite):
    def __init__(self, angle):
        super().__init__()
        self.x = JEU.joueur.x
        self.y = JEU.joueur.y
        self.degats = 8
        self.vitesse = 8
        self.angle_degree = angle + rd.randint(-20,20)
        self.angle_radians = math.radians(angle)
        self.dx = math.cos(self.angle_radians)*self.vitesse
        self.dy = math.sin(self.angle_radians)*self.vitesse
        self.image = pygame.image.load("Fichiers/Images/flame.png")
        self.image = pygame.transform.rotate(self.image, self.angle_degree+90)
        self.image_originale = self.image
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.delai = 0
        self.compteur = 180
    def update(self):
        self.compteur -= 1
        self.x += self.dx
        self.y -= self.dy
        self.rect.center = (self.x, self.y)
        if self.compteur <= 0:
            self.kill()
        for ennemi in JEU.groupe_ennemi:
            if self.rect.colliderect(ennemi.rect):
                if self.mask.overlap(ennemi.mask, (ennemi.rect.x-self.x , ennemi.rect.y-self.y)):
                    self.explose()
                    ennemi.vie -= self.degats
    def explose(self):
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (100,100), 1))

class Projectile_ennemi(pygame.sprite.Sprite):
    """Classe du projectile de l'ennemi"""
    def __init__(self , x , y , degats , vitesse , image_speciale = None , angle = -90):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        if image_speciale == None:
            self.image = pygame.image.load('Fichiers/Images/projectile_ennemi.png') #6x50
        else:
            self.image = image_speciale
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.image = pygame.transform.rotate(self.image, self.angle+90)
        self.mask = pygame.mask.from_surface(self.image)
        self.vitesse = vitesse
        self.degats = degats
        self.angle_radians = math.radians(angle)
        self.dx = math.cos(self.angle_radians)*self.vitesse
        self.dy = math.sin(self.angle_radians)*self.vitesse
        self.compteur = 200
    def update(self):
        """Methode permettant l'actualisation des projectiles de l'ennemi"""
        self.compteur -= 1
        self.x += self.dx
        self.y -= self.dy
        self.rect.center = (self.x, self.y)
        if self.compteur <= 0:
            self.kill()
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.explose()
                JEU.joueur.vie -= self.degats
    def explose(self):
        """Methode permettant l'explosion des projectiles à l'impact"""
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_2)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.rect.x, self.rect.y+35, 'Explosion3', (100,100), 2))

class Missile_guide_ennemi(pygame.sprite.Sprite):
    """Classe du missile guide de l'ennemi"""
    def __init__(self, x , y ,degats):
        super().__init__()
        self.x = x
        self.y = y
        self.degats = degats
        self.vitesse = 3
        self.image = pygame.image.load("Fichiers/Images/missile_guide.png")
        self.image = pygame.transform.scale(self.image, (20,50))
        self.image_originale = self.image
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.delai = 0
        self.cible = normalise_vecteur(JEU.joueur.x - self.x, JEU.joueur.y - self.y)
        self.pos = (JEU.joueur.x , JEU.joueur.y)
        self.x_dist = self.pos[0] - self.x
        self.y_dist = -(self.pos[1] - self.y)
        self.actif = True
        self.compteur = 600
    def update(self):
        """Methode permettant l'actualisation du missile guide de l'enemi"""
        self.compteur -= 1
        if self.y < JEU.joueur.rect.y and self.actif:
            self.pos = (JEU.joueur.x , JEU.joueur.y)
            self.cible = normalise_vecteur(self.pos[0] - self.x , self.pos[1] - self.y)
            self.x_dist = self.pos[0] - self.x
            self.y_dist = -(self.pos[1] - self.y)
            self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
            self.image = pygame.transform.rotate(self.image_originale, self.angle+90)
        else:
            self.actif = False
        self.x += self.cible[0] * self.vitesse
        self.y += self.cible[1] * self.vitesse
        self.rect = self.image.get_rect(center = (self.x , self.y))
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.explose()
                JEU.joueur.vie -= self.degats
        if self.compteur <= 0:
            self.kill()
    def explose(self):
        """Methode permettant l'explosion du missile à l'impact"""
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_2)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (100,100), 2))

class Projectile_paralysant_ennemi(pygame.sprite.Sprite):
    """Classe du projectile paralysant de l'ennemi"""
    def __init__(self, x, y, degats, vitesse, duree_effet):
        super().__init__()
        self.x = x
        self.y = y
        self.degats = degats
        self.vitesse = vitesse
        self.duree_effet = duree_effet
        pos = (JEU.joueur.x , JEU.joueur.y)
        x_dist = pos[0] - self.x
        y_dist = -(pos[1] - self.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.angle_degree = angle
        self.angle_radians = math.radians(angle)
        self.dx = math.cos(self.angle_radians)*self.vitesse
        self.dy = math.sin(self.angle_radians)*self.vitesse
        self.image = pygame.image.load("Fichiers/Images/projectile_ennemi_7.png")
        self.image = pygame.transform.rotate(self.image, self.angle_degree+90)
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.compteur = 200
    def update(self):
        """Methode permettant l'actualisation du projectile paralysant de l'ennemi"""
        self.compteur -= 1
        self.x += self.dx
        self.y -= self.dy
        self.rect.center = (self.x, self.y)
        if self.compteur <= 0:
            self.kill()
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.explose()
                JEU.joueur.vie -= self.degats
                JEU.joueur.paralyse(self.duree_effet)
    def explose(self):
        """Methode permettant l'explosion du projectile paralysant de l'ennemi"""
        #canal_libre = pygame.mixer.find_channel()
        #canal_libre.play(son_explosion_2)
        self.kill()

class Ennemi(pygame.sprite.Sprite):
    def __init__(self , x , y , degats , vie , vitesse , cadence_de_tir , points , exp , vitesse_projectile = 4 , bullet_image = None):
        super().__init__()
        self.x = x
        self.y = y
        self.degats = degats
        self.vie = vie
        self.vitesse = vitesse
        self.cadence_de_tir = cadence_de_tir
        self.points = points
        self.exp = exp
        self.fait_degats_collision = True
        self.degats_collision = JEU.joueur.vie_max//8
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.delai = 0
        self.vitesse_projectile = vitesse_projectile
        self.bullet_image = bullet_image
    def update(self):
        if self.vie <= 0:
            self.explose()
            self.lache_objet()
            JEU.score += self.points
            JEU.exp += self.exp
        self.delai += 1
        self.y += self.vitesse
        self.rect.center = (self.x, self.y)
        self.tire_projectile()
        if self.rect.y > JEU.hauteur + 75 or not (50 < self.rect.x < JEU.largeur-50):
            self.kill()
    def explose(self):
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_1)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion4', (200,200), 2))
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Projectile_ennemi(self.x , self.rect.y + 50 , self.degats , self.vitesse_projectile , self.bullet_image))
            self.delai = 0
    def lache_objet(self):
        if JEU.joueur.nombre_projectiles == 5 and not isinstance(JEU.joueur, Joueur_2) and JEU.objet_joueur_2_actif and not JEU.joueur.boost_ulti_actif:
            JEU.chance_de_joueur_2 = 5
        no_item_chance = 100 - JEU.chance_de_soin - JEU.chance_de_projectiles - JEU.chance_de_bouclier - JEU.chance_de_joueur_2 - JEU.chance_de_vitesse - JEU.chance_de_ulti
        item_list = [Soin(self.x, self.y), Objet_missile(self.x, self.y), Objet_bouclier(self.x, self.y), Objet_joueur_2(self.x, self.y), Objet_vitesse(self.x, self.y), Objet_ulti(self.x, self.y), False]
        prob_list = [JEU.chance_de_soin , JEU.chance_de_projectiles , JEU.chance_de_bouclier , JEU.chance_de_joueur_2 , JEU.chance_de_vitesse, JEU.chance_de_ulti, no_item_chance]
        if JEU.joueur.vie == JEU.joueur.vie_max:
            prob_list[0] = 0 
        drop = rd.choices(item_list, weights = prob_list)
        if drop[0]:
            JEU.groupe_objets.add(drop)
            if isinstance(drop[0], Objet_missile) and JEU.chance_de_projectiles-1 >= 0:
                JEU.chance_de_projectiles -= 1
            elif isinstance(drop[0], Objet_bouclier):
                JEU.chance_de_bouclier = 0
            elif isinstance(drop[0], Objet_vitesse):
                JEU.chance_de_vitesse = 0
            elif isinstance(drop[0], Objet_ulti):
                JEU.chance_de_ulti = 0
        
class Ennemi_1(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_1.png")
        self.degats = 10
        self.vie = 50
        self.vitesse = 0.75
        self.cadence_de_tir = 120
        self.points = 10
        self.exp = 1
        super().__init__(x , y , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)

class Ennemi_2(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_2.png")
        self.degats = 20
        self.vie = 75
        self.vitesse = 0.75
        self.cadence_de_tir = 120
        self.points = 20
        self.exp = 2
        super().__init__(x , y , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Projectile_ennemi(self.x - 12 , self.rect.y + 50 , self.degats , self.vitesse_projectile))
            JEU.groupe_projectiles_ennemis.add(Projectile_ennemi(self.x + 12, self.rect.y + 50 , self.degats , self.vitesse_projectile))
            self.delai = 0

class Ennemi_3(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_3.png")
        self.image = pygame.transform.scale(self.image, (75,75))
        self.degats = 40
        self.vie = 200
        self.vitesse = 0.4
        self.cadence_de_tir = 160
        self.points = 30
        self.exp = 4
        super().__init__(x , y , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)

class Ennemi_4(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_4.png")
        self.degats = 0
        self.vie = 250
        self.vitesse = 0.5
        self.cadence_de_tir = 300
        self.points = 40
        self.exp = 5
        super().__init__(x , y , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)
        self.delai = 250
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_ennemi.add(Ennemi_1(self.x - 70 , self.y + 75 + 20))
            JEU.groupe_ennemi.add(Ennemi_1(self.x , self.y + 75 + 20))
            JEU.groupe_ennemi.add(Ennemi_1(self.x + 70 , self.y + 75 + 20))
            self.delai = 0

class Ennemi_5(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_5.png")
        self.degats = 45
        self.vie = 175
        self.vitesse = 0
        self.cadence_de_tir = 160
        self.points = 50
        self.exp = 6
        super().__init__(x , y+45 , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Missile_guide_ennemi(self.x , self.rect.y + 50 , self.degats))
            self.delai = 0

class Ennemi_6(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_6.png")
        self.degats = 100
        self.vie = 150
        self.vitesse = 0
        self.cadence_de_tir = 160
        self.points = 60
        self.exp = 6
        self.vitesse_projectile = 8
        self.bullet_image = pygame.image.load("Fichiers/Images/projectile_ennemi_6.png") #6x200
        super().__init__(x , y+45 , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp , self.vitesse_projectile , self.bullet_image)
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Projectile_ennemi(self.x , self.y +100 , self.degats , self.vitesse_projectile , self.bullet_image))
            self.delai = 0

class Ennemi_7(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x , y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_7.png")
        self.degats = 10
        self.vie = 200
        self.vitesse = 0.75
        self.cadence_de_tir = 140
        self.points = 70
        self.exp = 7
        self.vitesse_projectile = 5
        super().__init__(x , y+45 , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp , self.vitesse_projectile)
        self.duree_effet = 30
    def update(self):
        if self.vie <= 0:
            self.explose()
            self.lache_objet()
            JEU.score += self.points
            JEU.exp += self.exp
        self.delai += 1
        self.y += self.vitesse
        self.rect.center = (self.x, self.y)
        self.tire_projectile()
        if self.rect.y > JEU.hauteur + 75 or self.rect.x > JEU.largeur-75:
            self.kill()
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Projectile_paralysant_ennemi(self.x , self.rect.y + 50 , self.degats , self.vitesse_projectile , self.duree_effet))
            self.delai = 0

class Ennemi_8(Ennemi):
    """Classe fille de Ennemi"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/ennemi_8.png")
        self.image_explosion = pygame.image.load("Fichiers/Images/projectile_ennemi_8.png").convert_alpha()
        self.scale = (250,250)
        self.degats = 2
        self.vie = 300
        self.vitesse = 0.5
        self.cadence_de_tir = 140
        self.points = 80
        self.exp = 8
        self.speed_animation = 2
        self.duree_effet = 90
        self.number_images = 27
        super().__init__(x , y+45 , self.degats , self.vie , self.vitesse , self.cadence_de_tir , self.points , self.exp)
    def tire_projectile(self):
        if self.delai >= self.cadence_de_tir and self.vie > 0 and JEU.projectile_ennemi_8:
            JEU.projectile_ennemi_8 = False
            JEU.groupe_explosions.add(Explosion_charge(JEU.joueur.x, JEU.joueur.y, 'Explosion7', self.scale, self.speed_animation, self.degats, self.duree_effet, self.image_explosion, self.number_images))
            self.delai = 0

class Projectile_boss(Projectile_ennemi):
    """Classe fille de Projectile_ennemi"""
    def __init__(self , x , y , degats , vitesse , angle):
        super().__init__(x ,y ,degats ,vitesse)
        self.x = x
        self.y = y
        self.degats = degats
        self.vitesse = vitesse
        self.angle_degrees = angle
        self.angle_radians = math.radians(angle)
        self.image = pygame.image.load('Fichiers/Images/projectile_boss_1.png') #6x75
        self.image = pygame.transform.rotate(self.image, self.angle_degrees - 90)
        self.mask = pygame.mask.from_surface(self.image)
        self.dx = math.cos(self.angle_radians)*self.vitesse
        self.dy = math.sin(self.angle_radians)*self.vitesse
        self.compteur = 300
    def update(self):
        self.compteur -= 1
        self.x += self.dx
        self.y -= self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.compteur <= 0: 
            self.kill()
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.explose()
                JEU.joueur.vie -= self.degats

class Missile_guide_boss(Missile_guide_ennemi):
    """Classe fille de Missile_guide_ennemi"""
    def __init__(self, x, y, degats, vitesse, temps):
        super().__init__(x, y, degats)
        self.vitesse = vitesse
        self.temps = temps
        self.compteur = 0
    def update(self):
        self.compteur += 1
        self.pos = (JEU.joueur.x , JEU.joueur.y)
        self.cible = normalise_vecteur(self.pos[0] - self.x , self.pos[1] - self.y)
        self.x_dist = self.pos[0] - self.x
        self.y_dist = -(self.pos[1] - self.y)
        self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
        self.image = pygame.transform.rotate(self.image_originale, self.angle+90)
        self.x += self.cible[0] * self.vitesse
        self.y += self.cible[1] * self.vitesse
        self.rect = self.image.get_rect(center = (self.x , self.y))
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.explose()
                JEU.joueur.vie -= self.degats
        if self.compteur >= self.temps:
            self.explose()

class Boss_1(pygame.sprite.Sprite):
    """Classe du premier boss"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Fichiers/Images/boss_1.png")
        self.image_originale = self.image
        self.x = JEU.largeur/2
        self.y = self.image.get_height()/2
        self.degats = 60
        self.vie = 10000
        self.vie_max = self.vie
        self.vie_max = self.vie
        self.vitesse = 4
        self.cadence_de_tir = 60
        self.points = 1000
        self.exp = 5
        self.fait_degats_collision = True
        self.degats_collision = JEU.joueur.vie_max//4
        self.delai = 0
        self.vitesse_projectile = 8
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = rd.choices(["Droite","Gauche"])
    def update(self):
        """Methode permettant l'actualisation du boss"""
        self.delai += 1
        x_dist = JEU.joueur.x - self.x
        y_dist = -(JEU.joueur.y - self.y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image_originale, self.angle + 90)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.rect.center = (self.x , self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.tire_projectile()
        if self.vie > self.vie_max/2:
            self.phase_1()
        elif self.vie > 0:
            self.phase_2()
        else:
            self.explose()
        texte_vie_pos_depart = JEU.largeur/4
        texte_pos_fin = texte_vie_pos_depart *3
        texte_vie_pos_fin = texte_vie_pos_depart + (self.vie/self.vie_max)*500
        pygame.draw.line(ecran , (50,50,50) , (texte_vie_pos_depart-10 , JEU.hauteur-50) , (texte_pos_fin+10 , JEU.hauteur-50) , 45)
        pygame.draw.line(ecran , NOIR , (texte_vie_pos_depart , JEU.hauteur-50) , (texte_pos_fin , JEU.hauteur-50) , 30)
        if texte_vie_pos_fin > texte_vie_pos_depart:
            pygame.draw.line(ecran , ROUGE , (texte_vie_pos_depart , JEU.hauteur-50) , (texte_vie_pos_fin , JEU.hauteur-50) , 30)
        texte_vie = score_font.render(f'{int(self.vie):5d} / {self.vie_max}', True, BLANC, None)
        ecran.blit(texte_vie, (texte_vie_pos_depart+162 , JEU.hauteur-50-texte_vie.get_height()/2))
    def phase_1(self):
        """Methode du premier deplacement du boss """
        if self.direction == "Droite":
            if self.x+self.image.get_width()/2 < JEU.largeur-28:
                self.x += self.vitesse
            else:
                self.direction = "Gauche"
        elif self.x-self.image.get_width()/2 > 28:
                self.x -= self.vitesse
        else:
            self.direction = "Droite"
    def phase_2(self):
        """Methode du second deplacement du boss"""
        self.cadence_de_tir = 30
        self.vitesse = 8
        self.degats = 80
        if self.direction == "Droite":
            if self.x+self.image.get_width()/2 < JEU.largeur-28:
                self.x += self.vitesse
            else:
                self.direction = "Bas"
        elif self.direction == "Bas":
            if self.y+self.image.get_height()/2 < JEU.hauteur-28:
                self.y += self.vitesse
            else:
                self.direction = "Haut"
        elif self.direction == "Haut":
            if self.y-self.image.get_height()/2 > 28:
                self.y -= self.vitesse
            elif JEU.largeur - self.x < self.x:
                self.direction = "Gauche"
            else:
                self.direction = "Droite"
        elif self.direction == "Gauche":
            if self.x-self.image.get_width()/2 > 28:
                self.x -= self.vitesse
            else:
                self.direction = "Bas"
    def tire_projectile(self):
        """Methode permettant au boss de tirer"""
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            JEU.groupe_projectiles_ennemis.add(Projectile_boss(self.x , self.y , self.degats , self.vitesse_projectile , self.angle))
            self.delai = 0
    def explose(self):
        """Methode permettant l'explosion du boss à la mort"""
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_1)
        self.kill()
        for _ in range(2):
            JEU.groupe_objets.add(Soin(self.x,self.y))
        JEU.combat_boss = False
        JEU.joueur.angle = 90
        JEU.joueur.image = JEU.joueur.image_originale
        JEU.joueur.rect = JEU.joueur.image.get_rect(center = (JEU.joueur.x,JEU.joueur.y))
        JEU.vague += 1
        JEU.score += self.points
        JEU.niveau += self.exp
        JEU.points_ameliorations += self.exp*2
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (500,500), 10))
        JEU.vague_active = True

class Boss_2(pygame.sprite.Sprite):
    """Classe du second boss"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Fichiers/Images/boss_2.png")
        self.image_originale = self.image
        self.x = JEU.largeur/2
        self.y = self.image.get_height()/2
        self.degats = 90
        self.vitesse_projectile = 10
        self.vie = 25000
        self.vie_max = self.vie
        self.vie_max = self.vie
        self.vitesse = 5
        self.cadence_de_tir = 80
        self.points = 2000
        self.exp = 10
        self.fait_degats_collision = True
        self.degats_collision = JEU.joueur.vie_max//4
        self.angle = 0
        self.delai = -40
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_animation = 1
        self.number_images = 30
        self.compteur = 0
        self.tire = True
        self.modes = ["laser","dispersion","missile"]
        self.attaques = ["dash","pulse"]
        self.mode_tir = self.modes[rd.randint(0,len(self.modes)-1)]
        self.mode_attaque = self.attaques[rd.randint(0,len(self.attaques)-1)]
        self.nombre_missiles_guides = 1
        self.vitesse_de_guidage = 5
        self.temps_de_guidage = 150
        self.vitesse_explosion_animation = 1
        self.nombre_images_explosion = 27
        self.duree_effet = 120
    def update(self):
        """Methode permettant l'actualisation du boss"""
        if self.vie > 0:
            if self.tire:
                self.delai += 1
                if self.delai >= self.cadence_de_tir/2:
                    if self.mode_tir == "laser":
                        JEU.groupe_projectiles_ennemis.add(Projectile_boss(self.x , self.y , self.degats , self.vitesse_projectile , self.angle))
                    elif self.mode_tir == "dispersion": 
                        JEU.groupe_projectiles_ennemis.add(Projectile_boss(self.x , self.y , self.degats , self.vitesse_projectile , self.angle + rd.randint(-10,10)))
                    elif self.mode_tir == "missile" and self.nombre_missiles_guides > 0:
                        JEU.groupe_projectiles_ennemis.add(Missile_guide_boss(self.x , self.y , self.degats , self.vitesse_de_guidage, self.temps_de_guidage))
                        self.nombre_missiles_guides -= 1
                    self.fait_degats_collision = True
                x_dist = JEU.joueur.x - self.x
                y_dist = -(JEU.joueur.y - self.y)
                self.angle = math.degrees(math.atan2(y_dist, x_dist))
            self.image = pygame.transform.rotate(self.image_originale, self.angle + 90)
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.mask = pygame.mask.from_surface(self.image)
            self.attaque()
            if not self.tire:
                self.compteur += 1
                if self.compteur >= self.speed_animation*self.number_images-1:
                    self.angle_radians = math.radians(self.angle)
                    self.dx = math.cos(self.angle_radians)*20
                    self.dy = math.sin(self.angle_radians)*20
                    self.x += self.dx
                    self.y -= self.dy
                    if self.x < 100:
                        self.x = 100
                    elif self.x > JEU.largeur-100:
                        self.x = JEU.largeur-100
                    if self.y < 100:
                        self.y = 100
                    elif self.y > JEU.hauteur-100:
                        self.y = JEU.hauteur-100
                    self.fait_degats_collision = False
                if self.compteur >= (self.speed_animation*self.number_images)+20:
                    self.tire = True
                    self.compteur = 0
        elif self.vie <= 0:
            self.explose()
            JEU.victoire = True
        texte_vie_pos_depart = JEU.largeur/4
        texte_pos_fin = texte_vie_pos_depart *3
        texte_vie_pos_fin = texte_vie_pos_depart + (self.vie/self.vie_max)*500
        pygame.draw.line(ecran , (50,50,50) , (texte_vie_pos_depart-10 , JEU.hauteur-50) , (texte_pos_fin+10 , JEU.hauteur-50) , 45)
        pygame.draw.line(ecran , NOIR , (texte_vie_pos_depart , JEU.hauteur-50) , (texte_pos_fin , JEU.hauteur-50) , 30)
        if texte_vie_pos_fin > texte_vie_pos_depart:
            pygame.draw.line(ecran , ROUGE , (texte_vie_pos_depart , JEU.hauteur-50) , (texte_vie_pos_fin , JEU.hauteur-50) , 30)
        texte_vie = score_font.render(f'{int(self.vie):5d} / {self.vie_max}', True, BLANC, None)
        ecran.blit(texte_vie, (JEU.largeur/2-texte_vie.get_width()/2 , JEU.hauteur-50-texte_vie.get_height()/2))
        self.rect.center = (self.x , self.y)
    def attaque(self):
        """Methode permettant au boss d'attaquer"""
        if self.delai >= self.cadence_de_tir and self.vie > 0:
            self.delai = 0
            self.tire= False
            self.nombre_missiles_guides = 1
            mode = rd.choices(self.modes)
            attaque = rd.choices(self.attaques)
            self.mode_tir = mode[0]
            self.mode_attaque = attaque[0]
            if self.mode_attaque == "dash":
                JEU.groupe_explosions.add(Dash_charge(self.x, self.y, self.speed_animation, self.degats, self.angle, self.number_images))
            elif self.mode_attaque == "pulse":
                JEU.groupe_explosions.add(Implosion_boss(self.x, self.y, 'Explosion7', (500,500), self.vitesse_explosion_animation, self.degats, self.duree_effet, self.nombre_images_explosion))
    def explose(self):
        """Methode permettant l'explosion du boss à la mort"""
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_1)
        self.kill()
        for _ in range(2):
            JEU.groupe_objets.add(Soin(self.x,self.y))
        JEU.combat_boss = False
        JEU.joueur.angle = 90
        JEU.joueur.image = JEU.joueur.image_originale
        JEU.joueur.rect = JEU.joueur.image.get_rect(center = (JEU.joueur.x,JEU.joueur.y))
        JEU.vague += 1
        JEU.score += self.points
        JEU.niveau += self.exp
        JEU.points_ameliorations += self.exp*2
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (500,500), 7))
        JEU.vague_active = True

class Meteorite(pygame.sprite.Sprite):
    """Classe des meteorites"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.degats = JEU.joueur.vie_max//5
        self.vitesse = 10
        self.image = pygame.image.load("Fichiers/Images/meteorite.png")
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        """Methode permettant l'actualisation des meteorites"""
        self.y += self.vitesse
        self.rect.center = (self.x , self.y)
        for entity in JEU.groupe_joueur:
            if self.rect.colliderect(entity.rect):
                if self.mask.overlap(entity.mask, (entity.rect.x-self.rect.x , entity.rect.y-self.rect.y)):
                    entity.vie -= self.degats
                    self.explose()
        if self.y >= JEU.hauteur + self.image.get_height():
            self.kill()
        for projectile in JEU.groupe_projectiles_joueur:
            if self.rect.colliderect(projectile.rect):
                if self.mask.overlap(projectile.mask, (projectile.rect.x-self.rect.x , projectile.rect.y-self.rect.y)):
                    projectile.explose()
    def explose(self):
        """Methode permettant l'explosionion des meteorites au contact"""
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_explosion_1)
        self.kill()
        JEU.groupe_explosions.add(Explosion(self.x, self.y, 'Explosion3', (500,500), 2))

class Menu_ameliorations:
    """Classe du menu d'ameliorations"""
    def __init__(self):
        self.couleur = GRIS
        self.coords = (0 , 3*HAUTEUR/10)
        self.largeur_hauteur = (3.5*LARGEUR/10 , 7*HAUTEUR/10)
        self.rect = pygame.Rect(self.coords , self.largeur_hauteur)
        self.est_actif = False
    def update(self):
        """Methode permettant l'actualisation du menu"""
        if self.est_actif:
            #Upgrade texte
            texte_points_ameliorations = score_font.render(f'Points: {JEU.points_ameliorations}' , True , VERT)
            texte_amelioration_degats = score_font.render(f'Degats: {JEU.joueur.degats}' , True , NOIR)
            texte_amelioration_vie = score_font.render(f'Vie: {JEU.joueur.vie_max}' , True , NOIR)
            texte_amelioratiob_cadence = score_font.render(f'Cadence: {30-JEU.joueur.cadence_de_tir}' , True , NOIR)
            texte_amelioration_soin = score_font.render(f'Soin: {JEU.chance_de_soin}%' , True , NOIR)
            pygame.draw.rect(ecran, self.couleur, self.rect)
            ecran.blit(texte_points_ameliorations , (10 , 22.5*JEU.hauteur/66-texte_points_ameliorations.get_height()/2))
            ecran.blit(texte_amelioration_degats , (10 , 30*JEU.hauteur/66-texte_amelioration_degats.get_height()/2))
            ecran.blit(texte_amelioration_vie , (10 , 40*JEU.hauteur/66-texte_amelioration_vie.get_height()/2))
            ecran.blit(texte_amelioratiob_cadence , (10 , 50*JEU.hauteur/66-texte_amelioratiob_cadence.get_height()/2))
            ecran.blit(texte_amelioration_soin , (10 , 60*JEU.hauteur/66-texte_amelioration_soin.get_height()/2))

            if isinstance(JEU.joueur, Joueur_2):
                if JEU.joueur.degats < 90:
                    bouton_amelioration_degats.draw()
                if JEU.joueur.vie_max < 200:
                    bouton_amelioration_vie.draw()
                if JEU.joueur.cadence_de_tir > 20:
                    bouton_amelioration_cadence.draw()
                if JEU.chance_de_soin < 10:
                    bouton_amelioration_soin.draw()

                if bouton_amelioration_degats.est_clique() and JEU.joueur.degats < 90 and JEU.points_ameliorations >= 1:
                    JEU.joueur.degats += 5
                    self.depenser_points()
                elif bouton_amelioration_vie.est_clique() and JEU.joueur.vie_max < 200 and JEU.points_ameliorations >= 1:
                    JEU.joueur.vie_max += 10
                    JEU.joueur.vie = (JEU.joueur.vie * JEU.joueur.vie_max)/(JEU.joueur.vie_max-10)
                    self.depenser_points()
                elif bouton_amelioration_cadence.est_clique() and JEU.joueur.cadence_de_tir > 20 and JEU.points_ameliorations >= 1:
                    JEU.joueur.cadence_de_tir -= 0.5
                    self.depenser_points()
                elif bouton_amelioration_soin.est_clique() and JEU.chance_de_soin < 10 and JEU.points_ameliorations >= 1:
                    JEU.chance_de_soin += 0.5
                    self.depenser_points()

            else:
                if JEU.joueur.degats < 60:
                    bouton_amelioration_degats.draw()
                if JEU.joueur.vie_max < 150:
                    bouton_amelioration_vie.draw()
                if JEU.joueur.cadence_de_tir > 25:
                    bouton_amelioration_cadence.draw()
                if JEU.chance_de_soin < 5:
                    bouton_amelioration_soin.draw()
                
                if bouton_amelioration_degats.est_clique() and JEU.joueur.degats < 60 and JEU.points_ameliorations >= 1:
                    JEU.joueur.degats += 5
                    self.depenser_points()
                elif bouton_amelioration_vie.est_clique() and JEU.joueur.vie_max < 150 and JEU.points_ameliorations >= 1:
                    JEU.joueur.vie_max += 10
                    JEU.joueur.vie = (JEU.joueur.vie * JEU.joueur.vie_max)/(JEU.joueur.vie_max-10)
                    self.depenser_points()
                elif bouton_amelioration_cadence.est_clique() and JEU.joueur.cadence_de_tir > 25 and JEU.points_ameliorations >= 1:
                    JEU.joueur.cadence_de_tir -= 0.5
                    self.depenser_points()
                elif bouton_amelioration_soin.est_clique() and JEU.chance_de_soin < 5 and JEU.points_ameliorations >= 1:
                    JEU.chance_de_soin += 0.5
                    self.depenser_points()

    def depenser_points(self):
        """Methode permettant de dépenser les points d'ameliorations"""
        #pygame.mixer.music.stop()
        canal_libre = pygame.mixer.find_channel()
        canal_libre.play(son_amelioration)
        #pygame.mixer.Sound.play(son_amelioration)
        JEU.points_ameliorations -= 1

class Explosion(pygame.sprite.Sprite):
    """Classe de l'explosion"""
    def __init__(self, x, y, path, scale, vitesse, nombre = 25, rotation = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.images = []
        self.action = False
        for i in range(1,nombre):
            image = pygame.image.load(f'Fichiers/Explosions_animations/{path}/00{i:02}.png')
            image = pygame.transform.scale(image, scale)
            image_orientee = pygame.transform.rotate(image, rotation+90)
            self.images.append(image_orientee)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.compteur = 0
        self.vitesse_explosion = vitesse
    def update(self):
        """Methode permettant l'actualisation de l'explosion"""
        self.compteur += 1
        if self.compteur >= self.vitesse_explosion and self.index < len(self.images)-1:
            self.compteur = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images)-1 and self.compteur >= self.vitesse_explosion:
            self.action = True
            self.kill()

class Explosion_charge(Explosion):
    """Classe de la charge de l'explosion, utilisee par Ennemi_8, fille de Explosion"""
    def __init__(self, x, y, path, scale, vitesse, degats, duree_effet, image, nombre):
        super().__init__(x, y, path, scale, vitesse, nombre)
        self.scale = scale
        self.degats = degats
        self.duree_effet = duree_effet
        self.image_explosion = image
        self.image_explosion = pygame.transform.scale(self.image_explosion, self.scale)
        self.image_orientee = self.image_explosion
        self.rect = self.image_explosion.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.image_explosion)
        self.angle = 0
    def update(self):
        """Methode permettant l'actualisation de la charge"""
        self.compteur += 1
        if self.compteur >= self.vitesse_explosion and self.index < len(self.images)-1:
            self.compteur = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images)-1 and self.compteur >= self.vitesse_explosion and not self.action:
            self.action = True
        if self.action:
            self.angle += 1
            self.duree_effet -= 1
            if self.duree_effet > 0:
                self.image_orientee = pygame.transform.rotate(self.image_explosion, self.angle)
                self.x, self.y = self.rect.center  # Sauvegarde le centre actuel
                self.rect = self.image_orientee.get_rect()  # Remplace l'ancien rect par le nouveau rect
                self.rect.center = (self.x, self.y)  # Definit le centre du nouveau rect à celui de l'ancien
                ecran.blit(self.image_orientee, self.rect)
                if self.rect.colliderect(JEU.joueur.rect):
                    if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                        JEU.joueur.vie -= self.degats
            else:
                self.kill()
                JEU.projectile_ennemi_8 = True

class Implosion_boss(Explosion):
    """Classe de l'implosion du boss, utilisee par Boss_2, fille de Explosion"""
    def __init__(self, x, y, path, scale, vitesse, degats, duree_effet, nombre):
        super().__init__(x, y, path, scale, vitesse, nombre)
        self.x = x
        self.y = y
        self.scale = scale
        self.degats = degats
        self.duree_effet = duree_effet
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 15
    def update(self):
        """Methode permettant l'actualisation de l'implosion"""
        self.compteur += 1
        if self.compteur >= self.vitesse_explosion and self.index < len(self.images)-1:
            self.compteur = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images)-1 and self.compteur >= self.vitesse_explosion and not self.action:
            self.action = True
        if self.action:
            if self.rect.colliderect(JEU.joueur.rect):
                if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                    JEU.joueur.vie -= self.degats
            for i in range(0,24):
                projectile = Projectile_ennemi(self.x, self.y, self.degats/2, 7, None , self.angle*i)
                JEU.groupe_projectiles_ennemis.add(projectile)
            self.kill()

class Dash_charge(pygame.sprite.Sprite):
    """Classe de la charge du dash du boss, utilisee par Boss_2"""
    def __init__(self, x, y, vitesse, degats, angle, nombre):
        super().__init__()
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.degats = degats
        self.angle = angle
        self.nombre = nombre
        self.index = 1
        self.sprite = Dash(self.x , self.y , self.index , self.angle)
        self.image = self.sprite.image
        self.rect = self.image.get_rect(center = (self.sprite.x , self.sprite.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.compteur = 0
    def update(self):
        """Methode permettant l'actualisation de la charge"""
        self.compteur += 1
        if self.compteur >= self.vitesse and self.index < self.nombre:
            self.compteur = 0
            self.index += 1
            self.sprite = Dash(self.x , self.y , self.index , self.angle)
            self.image = self.sprite.image
            self.rect = self.image.get_rect(center = (self.sprite.x, self.sprite.y))
        if self.index >= self.nombre and self.compteur >= self.vitesse:
            if self.rect.colliderect(JEU.joueur.rect):
                if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                    JEU.joueur.vie -= self.degats
            self.kill()
            
class Dash(pygame.sprite.Sprite):
    """Classe du dash du boss, utilisee par Boss_2"""
    def __init__(self, x, y, index, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.angle_radians = math.radians(angle)
        self.dx = math.cos(self.angle_radians)*200
        self.dy = math.sin(self.angle_radians)*200
        self.x += self.dx
        self.y -= self.dy
        self.image = pygame.image.load(f'Fichiers/Explosions_animations/Explosion8/00{index:02}.png')
        self.image = pygame.transform.rotate(self.image, self.angle+90)
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.compteur = 0
    def update(self):
        """Methode permettant l'actualisation du dash"""
        self.compteur += 1
        if self.compteur >= 2:
            self.compteur = 0
            self.kill()

class Bouclier(pygame.sprite.Sprite):
    """Classe du bouclier du joueur"""
    def __init__(self):
        super().__init__()
        self.x = JEU.joueur.x
        self.y = JEU.joueur.y
        self.image = pygame.image.load("Fichiers/Images/bouclier.png")
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.vie = JEU.joueur.vie_max//4
        self.vie_max = self.vie
    def update(self):
        """Methode permettant l'actualisation du bouclier"""
        self.x = JEU.joueur.x
        self.y = JEU.joueur.y
        self.rect.center = (self.x , self.y)
        texte_vie_pos_depart = (self.x-50, self.y + 80)
        texte_vie_pos_fin = (texte_vie_pos_depart[0] + 100, texte_vie_pos_depart[1])
        vie_fin = texte_vie_pos_depart[0] + ((self.vie*100)/self.vie_max)
        pygame.draw.line(ecran , GRIS , (texte_vie_pos_depart[0]-10 , texte_vie_pos_depart[1]) , (texte_vie_pos_fin[0]+10 , texte_vie_pos_fin[1]) , 20)
        pygame.draw.line(ecran , NOIR , texte_vie_pos_depart , texte_vie_pos_fin , 10)
        pygame.draw.line(ecran , BLEU , (texte_vie_pos_depart) , (vie_fin , texte_vie_pos_fin[1]) , 10)
        for projectile in JEU.groupe_projectiles_ennemis:
            if self.rect.colliderect(projectile.rect) and not isinstance(projectile, Projectile_paralysant_ennemi):
                if self.mask.overlap(projectile.mask, (projectile.rect.x-self.rect.x , projectile.rect.y-self.rect.y)):
                    self.vie -= projectile.degats
                    projectile.explose()
        if self.vie <= 0:
            self.kill()
            JEU.chance_de_bouclier = 3

class Objet(pygame.sprite.Sprite):
    """Classe des objets apparaissants aleatoirement a la mort d'un ennemi"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.action = False
    def update_item(self):
        """Methode permettant l'actualisation de l'objet"""
        self.rect.y += 0.75
        if self.rect.colliderect(JEU.joueur.rect):
            if self.mask.overlap(JEU.joueur.mask, (JEU.joueur.rect.x-self.rect.x , JEU.joueur.rect.y-self.rect.y)):
                self.action = True
                self.kill()

class Objet_joueur_2(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/objet_joueur_2.png")
        super().__init__(x, y)
    def update(self):
        """Methode permettant l'actualisation de l'objet"""
        super().update_item()
        JEU.objet_joueur_2_actif = False
        JEU.chance_de_joueur_2 = 0
        if self.action:
            args = (JEU.joueur.degats, JEU.joueur.vie, JEU.joueur.vie_max, JEU.joueur.cadence_de_tir)
            JEU.joueur.kill()
            JEU.joueur = Joueur_2(args)
            JEU.groupe_joueur.add(JEU.joueur)
            JEU.chance_de_projectiles = 2
        if self.rect.y > JEU.hauteur:
            self.kill()
            JEU.chance_de_joueur_2 = 5
            JEU.objet_joueur_2_actif = True

class Soin(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/heal_item.png")
        super().__init__(x, y)
    def update(self):
        """Methode permettant l'actualisation de l'objet"""
        super().update_item()
        if self.action:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_soin)
            JEU.joueur.vie += 15*JEU.joueur.vie_max//100
            if JEU.joueur.vie > JEU.joueur.vie_max:
                JEU.joueur.vie = JEU.joueur.vie_max

class Objet_missile(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/objet_projectile.png")
        super().__init__(x, y)
    def update(self):
        """Methode permettant l'actualisation de l'objet"""
        super().update_item()
        if self.action:
            JEU.joueur.nombre_projectiles += 1
        if self.rect.y > JEU.hauteur:
            self.kill()
            JEU.chance_de_projectiles += 1

class Objet_bouclier(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/objet_bouclier.png")
        super().__init__(x, y)
    def update(self):
        """Methode permettant l'actualisation de l'objet"""
        super().update_item()
        if self.action:
            #pygame.mixer.music.stop()
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_bouclier)
            #pygame.mixer.Sound.play(son_bouclier)
            JEU.groupe_joueur.add(Bouclier())
        if self.rect.y > JEU.hauteur:
            self.kill()
            JEU.chance_de_bouclier = 3

class Objet_vitesse(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/objet_vitesse.png")
        super().__init__(x, y)
    def update(self):
        """Methode permettant l'actualisation de l'objet"""
        super().update_item()
        if self.action:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_bouclier)
            JEU.joueur.boost_vitesse_actif = True
            JEU.joueur.vitesse += JEU.joueur.boost_vitesse
        if self.rect.y > JEU.hauteur:
            self.kill()
            JEU.chance_de_vitesse = 2

class Objet_ulti(Objet):
    """Classe fille de Objet"""
    def __init__(self, x, y):
        self.image = pygame.image.load("Fichiers/Images/boost.png")
        super().__init__(x, y)
    def update(self):
        super().update_item()
        if self.action:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_bouclier)
            JEU.joueur.boost_ulti_actif = True
            JEU.joueur.nombre_projectiles += 5
            JEU.joueur.vie_max += 50
            JEU.joueur.vie += 50
            JEU.joueur.degats += 50
            JEU.joueur.cadence_de_tir -= 5
        if self.rect.y > JEU.hauteur:
            self.kill()
            JEU.chance_de_ulti = 1


class Alerte(pygame.sprite.Sprite):
    """Classe alerte avant les meteorites"""
    def __init__(self):
        super().__init__()
        self.x = LARGEUR/2
        self.y = HAUTEUR/2
        self.image_1 = pygame.image.load("Fichiers/Images/alerte_meteorite.png")
        self.image_2 = pygame.image.load("Fichiers/Images/vide.png")
        self.image = self.image_1
        self.rect = self.image.get_rect(center = (self.x , self.y))
        self.compteur = 60
        self.temps = 360
    def update(self):
        """Methode permettant l'actualisation de l'alerte"""
        if self.temps % 120 == 0:
            canal_libre = pygame.mixer.find_channel()
            canal_libre.play(son_alerte_1)
        self.temps -= 1
        self.compteur -= 1
        if self.compteur == 0:
            if self.image == self.image_1:
                self.image = self.image_2
            else:
                self.image = self.image_1
            self.compteur = 60
        if self.temps == 0:
            self.kill()

class Menu_pause:
    """Classe du menu de pause"""
    def __init__(self):
        self.fond = pygame.image.load("Fichiers/Images/fond_espace.png").convert()
        self.est_actif = False
        self.largeur = LARGEUR
        self.hauteur = HAUTEUR
        self.defile = 0
    def update(self):
        """Methode permettant l'actualisation du menu"""
        if self.est_actif:
            self.defile += 0.75
            for i in range(2):
                ecran.blit(self.fond, (0 , self.defile-i*(self.fond.get_height()))) 
            if self.defile > self.hauteur:
                self.defile = 0
            bouton_jouer_pause.draw()
            bouton_menu_pause.draw()
            bouton_quitter_pause.draw()
            if bouton_jouer_pause.est_clique():
                self.est_actif = False
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_reprendre_clique)
            if bouton_menu_pause.est_clique():
                JEU.nouvelle_partie(True)
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_menu_clique)
            if bouton_quitter_pause.est_clique():
                pygame.quit()
                sys.exit()

class Menu_developpeur:
    """Classe du menu de developpeur"""
    def __init__(self):
        self.couleur = GRIS
        self.coords = (LARGEUR/2 , HAUTEUR/2)
        self.largeur_hauteur = (LARGEUR/2 , HAUTEUR/2)
        self.rect = pygame.Rect(self.coords , self.largeur_hauteur)
        self.est_actif = False
    def update(self):
        """Methode permettant l'actualisation du menu"""
        if self.est_actif:
            pygame.draw.rect(ecran, self.couleur, self.rect)
            bouton_plus_degats_dev.draw()
            bouton_moins_degats_dev.draw()
            bouton_plus_vie_dev.draw()
            bouton_moins_vie_dev.draw()
            bouton_plus_missile_dev.draw()
            bouton_moins_missile_dev.draw()
            bouton_plus_cadence_dev.draw()
            bouton_moins_cadence_dev.draw()
            bouton_plus_vague_dev.draw()
            bouton_moins_vague_dev.draw()
            bouton_plus_boss_dev.draw()
            bouton_moins_boss_dev.draw()

            texte_degats = score_font.render(f'Degats: {JEU.joueur.degats}' , True , NOIR)
            texte_vie = score_font.render(f'Vie: {JEU.joueur.vie}' , True , NOIR)
            texte_missile = score_font.render(f'Projectiles: {JEU.joueur.nombre_projectiles}' , True , NOIR)
            texte_cadence = score_font.render(f'Cadence: {30-JEU.joueur.cadence_de_tir}' , True , NOIR)
            texte_vague = score_font.render(f'Vague: {JEU.vague}' , True , NOIR)
            texte_boss = score_font.render(f'Boss: {JEU.boss_actuel}' , True , NOIR)

            ecran.blit(texte_degats , (JEU.largeur/2+30 , 37*JEU.hauteur/66-texte_degats.get_height()/2))
            ecran.blit(texte_vie , (JEU.largeur/2+30 , 42*JEU.hauteur/66-texte_degats.get_height()/2))
            ecran.blit(texte_missile , (JEU.largeur/2+30 , 47*JEU.hauteur/66-texte_degats.get_height()/2))
            ecran.blit(texte_cadence , (JEU.largeur/2+30 , 52*JEU.hauteur/66-texte_degats.get_height()/2))
            ecran.blit(texte_vague , (JEU.largeur/2+30 , 57*JEU.hauteur/66-texte_degats.get_height()/2))
            ecran.blit(texte_boss , (JEU.largeur/2+30 , 62*JEU.hauteur/66-texte_degats.get_height()/2))

            if bouton_plus_degats_dev.est_clique():
                JEU.joueur.degats += 5
            elif bouton_moins_degats_dev.est_clique() and JEU.joueur.degats-5 >= 0:
                JEU.joueur.degats -= 5
            elif bouton_plus_vie_dev.est_clique():
                JEU.joueur.vie += 5
            elif bouton_moins_vie_dev.est_clique() and JEU.joueur.vie-5>0:
                JEU.joueur.vie -= 5
            elif bouton_plus_missile_dev.est_clique() and JEU.joueur.nombre_projectiles<5:
                JEU.joueur.nombre_projectiles += 1
            elif bouton_moins_missile_dev.est_clique() and JEU.joueur.nombre_projectiles-1>0:
                JEU.joueur.nombre_projectiles -= 1
            elif bouton_plus_cadence_dev.est_clique() and JEU.joueur.cadence_de_tir-0.5>=10:
                JEU.joueur.cadence_de_tir -= 0.5
            elif bouton_moins_cadence_dev.est_clique() and JEU.joueur.cadence_de_tir+0.5<=30:
                JEU.joueur.cadence_de_tir += 0.5
            elif bouton_plus_vague_dev.est_clique() and JEU.vague+1<=10:
                JEU.vague += 1
                if JEU.vague > 5:
                    JEU.boss_actuel = 1
                for ennemi in JEU.groupe_ennemi:
                    ennemi.kill()
                JEU.meteorite_delai = 1000
                JEU.alerte_active = False
                JEU.vague_progression = 0
            elif bouton_moins_vague_dev.est_clique() and JEU.vague-1>=1:
                JEU.vague -= 1
                if JEU.vague <= 5:
                    JEU.boss_actuel = 0
                for ennemi in JEU.groupe_ennemi:
                    ennemi.kill()
                JEU.meteorite_delai = 1000
                JEU.alerte_active = False
                JEU.vague_progression = 0
            elif bouton_plus_boss_dev.est_clique() and JEU.boss_actuel+1<=1:
                JEU.boss_actuel += 1
            elif bouton_moins_boss_dev.est_clique() and JEU.boss_actuel-1>=0:
                JEU.boss_actuel -= 1

class Menu:
    """Classe du menu de demarrage"""
    def __init__(self):
        self.fond = pygame.image.load("Fichiers/Images/fond_espace.png").convert()
        self.est_actif = True
        self.largeur = LARGEUR 
        self.hauteur = HAUTEUR
        self.defile = 0
        self.parametre = Parametre()
    def update(self):
        """Methode permettant l'actualisation du menu"""
        if not self.parametre.est_actif:
            self.defile += 0.75
            for i in range(2):
                ecran.blit(self.fond, (0 , self.defile-i*(self.fond.get_height()))) 
            if self.defile > self.hauteur:
                self.defile = 0
            pygame.mouse.set_visible(True) 
            #creation de la bannière
            titre = pygame.image.load('Fichiers/images/spaceship_attack.png')
            titre = pygame.transform.scale(titre,(0.5*LARGEUR,0.4*HAUTEUR))
            titre_rect = titre.get_rect()
            titre_rect.center = (LARGEUR/2 , HAUTEUR/4)
            # draw le bouton Jouer
            bouton_jouer_menu.draw()
            bouton_quitter_menu.draw()
            parametre_bouton_menu.draw()

            #Boutons du menu
            if bouton_jouer_menu.est_clique():
                JEU.nouvelle_partie(False)
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_jouer_clique)
            if parametre_bouton_menu.est_clique():
                self.parametre.est_actif = True
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_standard_clique)
            if bouton_quitter_menu.est_clique():
                canal_libre = pygame.mixer.find_channel()
                canal_libre.play(son_standard_clique)
                pygame.quit()
                sys.exit()

            # affichage de la bannière
            ecran.blit(titre,titre_rect)
        else:
            self.parametre.update()

class Parametre:
    '''
    La class Parametre permet de gérer l'affichage des paramètres du jeu
    '''
    def __init__(self):
        self.fond = pygame.image.load("Fichiers/Images/fond_espace.png").convert()
        self.est_actif = False
        self.largeur = LARGEUR
        self.hauteur = HAUTEUR
        self.defile = 0
        self.banniere_image = banniere_parametre_image
        self.separation_image = separation_image
        self.text = text_image
        self.hauteur = int(((LARGEUR*0.45)*1047)/1000)
    def update(self):
        self.banniere_image = pygame.transform.scale(self.banniere_image,(430,430))
        self.separation_image = pygame.transform.scale(self.separation_image,(7,470))
        self.text = pygame.transform.scale(self.text,(LARGEUR*0.45,self.hauteur))

        #permet de gérer les délais de clique des boutons

        if self.est_actif:
            #défilement du fond
            self.defile += 0.75
            for i in range(2):
                ecran.blit(self.fond, (0 , self.defile-i*(self.fond.get_height()))) 
            if self.defile > self.hauteur:
                self.defile = 0


            # chargement des texts 
            z_texte = score_font.render('se déplacer vers la droite',False,BLANC)
            q_texte = score_font.render('se déplacer vers la gauche',False,BLANC)
            s_texte = score_font.render('se déplacer vers le bas',False,BLANC)
            d_texte = score_font.render('se déplacer vers le haut',False,BLANC)
            espace_text = score_font.render('ouvrir le shop',False,BLANC)
            echap_text = score_font.render('mettre en pause',False,BLANC)
            echap_text_2 = parametre_font.render('echap',False,BLANC)
            entrer_text = score_font.render('menu de developpeur',False,BLANC)

            #affichage du bouton retour
            retour_bouton_menu.draw()

            #affichage de tout les éléments présent à l'écran
            ecran.blit(self.banniere_image,(5.35*JEU.largeur/10,-1.7*JEU.hauteur/10))
            ecran.blit(self.text,(5.3*JEU.largeur/10,2.7*JEU.hauteur/10))
            ecran.blit(self.separation_image,(5*JEU.largeur/10,2*JEU.hauteur/10))
            #les touches
            ecran.blit(z_image,(0.1*JEU.largeur/10,2.5*JEU.hauteur/10))
            ecran.blit(q_image,(0.1*JEU.largeur/10,3.3*JEU.hauteur/10))
            ecran.blit(s_image,(0.1*JEU.largeur/10,4.1*JEU.hauteur/10))
            ecran.blit(d_image,(0.1*JEU.largeur/10,4.9*JEU.hauteur/10))
            ecran.blit(espace_image,(0.1*JEU.largeur/10,5.7*JEU.hauteur/10))
            ecran.blit(echap_image,(0.1*JEU.largeur/10,6.5*JEU.hauteur/10))
            ecran.blit(entrer_image,(0.1*JEU.largeur/10,7.4*JEU.hauteur/10))
            #texts associés aux touches
            ecran.blit(z_texte,(0.7*JEU.largeur/10,2.5*JEU.hauteur/10))
            ecran.blit(q_texte,(0.7*JEU.largeur/10,3.3*JEU.hauteur/10))
            ecran.blit(s_texte,(0.7*JEU.largeur/10,4.1*JEU.hauteur/10))
            ecran.blit(d_texte,(0.7*JEU.largeur/10,4.9*JEU.hauteur/10))
            ecran.blit(espace_text,(0.5*JEU.largeur/10,5.7*JEU.hauteur/10))
            ecran.blit(echap_text,(1.8*JEU.largeur/10,6.53*JEU.hauteur/10))
            ecran.blit(echap_text_2,(0.45*JEU.largeur/10,6.55*JEU.hauteur/10))
            ecran.blit(entrer_text,(1.2*JEU.largeur/10,8*JEU.hauteur/10))
            
            if retour_bouton_menu.est_clique():
                self.est_actif = False
                canal_libre = pygame.mixer.find_channel()
                canal_libre.set_volume(1)
                canal_libre.play(son_standard_clique)

#Jeu
JEU = Jeu(LARGEUR , HAUTEUR , FPS)

#Boutons de l'ecran du menu
bouton_jouer_menu = Bouton(JEU.largeur/2,55*JEU.hauteur/100, image_bouton_jouer, 8)
bouton_quitter_menu = Bouton(JEU.largeur/1.985,70*JEU.hauteur/100, image_bouton_quitter, 6.5)
parametre_bouton_menu = Bouton(55,4*JEU.hauteur/4.4, parametre_bouton_image, 0.3)
retour_bouton_menu = Bouton(JEU.largeur/10,JEU.hauteur/10, retour_bouton_image, 0.3)

#Boutons de l'ecran de fin
bouton_rejouer = Bouton(JEU.largeur/2,6.5*JEU.hauteur/10, image_bouton_rejouer, 8)
bouton_quitter = Bouton(JEU.largeur/2,9*JEU.hauteur/10, image_bouton_menu, 8)

#Bouton de l'écran de victoire
bouton_menu_victoire = Bouton(2*JEU.largeur/10,7*JEU.hauteur/10, image_bouton_menu, 5.5)
bouton_rejouer_victoire = Bouton(4.8*JEU.largeur/10,7*JEU.hauteur/10, image_bouton_jouer, 5.5)
bouton_quitter_victoire = Bouton(8*JEU.largeur/10,7*JEU.hauteur/10, image_bouton_quitter, 5.5)

#Boutons de l'ecran de pause
bouton_menu_pause = Bouton(JEU.largeur/2,30*JEU.hauteur/100, image_bouton_menu, 8)
bouton_jouer_pause = Bouton(JEU.largeur/2,50*JEU.hauteur/100, image_bouton_jouer, 8)
bouton_quitter_pause = Bouton(JEU.largeur/1.98,70*JEU.hauteur/100, image_bouton_quitter, 7)

#Buttons menu d'ameliorations
bouton_amelioration_degats = Bouton(3*JEU.largeur/10 , 30*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_amelioration_vie = Bouton(3*JEU.largeur/10 , 40*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_amelioration_cadence = Bouton(3*JEU.largeur/10 , 50*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_amelioration_soin = Bouton(3*JEU.largeur/10 , 60*JEU.hauteur/66 , image_bouton_plus , 1)

#Boutons menu developpeur
bouton_plus_degats_dev = Bouton(9*JEU.largeur/10 , 37*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_degats_dev = Bouton(9.6*JEU.largeur/10 , 37*JEU.hauteur/66 , image_bouton_moins , 1)
bouton_plus_vie_dev = Bouton(9*JEU.largeur/10 , 42*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_vie_dev = Bouton(9.6*JEU.largeur/10 , 42*JEU.hauteur/66 , image_bouton_moins , 1)
bouton_plus_missile_dev = Bouton(9*JEU.largeur/10 , 47*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_missile_dev = Bouton(9.6*JEU.largeur/10 , 47*JEU.hauteur/66 , image_bouton_moins , 1)
bouton_plus_cadence_dev = Bouton(9*JEU.largeur/10 , 52*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_cadence_dev = Bouton(9.6*JEU.largeur/10 , 52*JEU.hauteur/66 , image_bouton_moins , 1)
bouton_plus_vague_dev = Bouton(9*JEU.largeur/10 , 57*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_vague_dev = Bouton(9.6*JEU.largeur/10 , 57*JEU.hauteur/66 , image_bouton_moins , 1)
bouton_plus_boss_dev = Bouton(9*JEU.largeur/10 , 62*JEU.hauteur/66 , image_bouton_plus , 1)
bouton_moins_boss_dev = Bouton(9.6*JEU.largeur/10 , 62*JEU.hauteur/66 , image_bouton_moins , 1)

complement_diagonale = JEU.joueur.vitesse/(math.sqrt(JEU.joueur.vitesse**2 + JEU.joueur.vitesse**2))

#Initialise le module de mixage et joue la musique d'arrière plan en boucle

mixer.init()
mixer.music.load("Fichiers/Sons/musique_de_fond.mp3")
mixer.music.play(-1)

#Boucle principale du jeu
run = True
while run:
    #Traiteur d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and JEU.joueur.est_vivant:
            if event.key == pygame.K_SPACE and not JEU.menu.est_actif and not JEU.menu_pause.est_actif and not JEU.menu_developpeur.est_actif:
                JEU.menu_ameliorations.est_actif = not JEU.menu_ameliorations.est_actif
                if not JEU.menu_ameliorations.est_actif:
                    pygame.mixer.Sound.play(son_ouvrir_menu)
                else: 
                    pygame.mixer.Sound.play(son_fermer_menu)
            elif event.key == pygame.K_ESCAPE and not JEU.menu.est_actif:
                JEU.menu_pause.est_actif = not JEU.menu_pause.est_actif
                if not JEU.menu_pause.est_actif:
                    pygame.mixer.Sound.play(son_ouvrir_menu)
                else: 
                    pygame.mixer.Sound.play(son_fermer_menu)
            elif event.key == pygame.K_RETURN and not JEU.menu.est_actif and not JEU.menu_pause.est_actif and not JEU.menu_ameliorations.est_actif:
                JEU.menu_developpeur.est_actif = not JEU.menu_developpeur.est_actif
                if not JEU.menu_developpeur.est_actif:
                    pygame.mixer.Sound.play(son_ouvrir_menu)
                else: 
                    pygame.mixer.Sound.play(son_fermer_menu)
    
    #SI LE JOUEUR EST EN JEU   
    if JEU.joueur.est_vivant and not JEU.menu_ameliorations.est_actif and not JEU.menu_pause.est_actif and not JEU.menu_developpeur.est_actif and not JEU.menu.est_actif:
        key = pygame.key.get_pressed()
        if key[pygame.K_q] and key[pygame.K_z]:
            JEU.joueur.deplace(-complement_diagonale , -complement_diagonale)
        elif key[pygame.K_q] and key[pygame.K_s]:
            JEU.joueur.deplace(-complement_diagonale , complement_diagonale)
        elif key[pygame.K_d] and key[pygame.K_z]:
            JEU.joueur.deplace(complement_diagonale , -complement_diagonale)
        elif key[pygame.K_d] and key[pygame.K_s]:
            JEU.joueur.deplace(complement_diagonale , complement_diagonale)
        elif key[pygame.K_q]:
            JEU.joueur.deplace(-1,0)
        elif key[pygame.K_d]:
            JEU.joueur.deplace(1,0)
        elif key[pygame.K_z]:
            JEU.joueur.deplace(0,-1)
        elif key[pygame.K_s]:
            JEU.joueur.deplace(0,1)
        mixer.music.set_volume(0.3)
        JEU.update()

    #ECRAN DU MENU D'AMELIORATION
    elif JEU.joueur.est_vivant and JEU.menu_ameliorations.est_actif and not JEU.menu_pause.est_actif and not JEU.menu_developpeur.est_actif and not JEU.menu.est_actif:
        JEU.menu_ameliorations.update()
        pygame.display.flip() #update
        clock.tick(JEU.fps)

    #ECRAN DU MENU DEV
    elif JEU.menu_developpeur.est_actif and JEU.joueur.est_vivant and not JEU.menu_pause.est_actif and not JEU.menu_ameliorations.est_actif and not JEU.menu.est_actif:
        JEU.menu_developpeur.update()
        pygame.display.flip()
        clock.tick(JEU.fps)

    #SI LE JOUEUR MEURT
    elif not JEU.joueur.est_vivant and len(JEU.groupe_explosions)>0 and not JEU.menu_pause.est_actif and not JEU.menu_developpeur.est_actif and not JEU.menu.est_actif:
        JEU.groupe_explosions.draw(ecran)
        JEU.groupe_explosions.update()
        pygame.display.flip() #update
        clock.tick(JEU.fps)
    
    #ECRAN DU MENU
    elif JEU.menu.est_actif:
        JEU.menu_ameliorations.est_actif = False
        JEU.menu_developpeur.est_actif = False
        mixer.music.set_volume(0.3)
        JEU.menu.update()
        pygame.display.flip() #update
        clock.tick(JEU.fps)

    #ECRAN DE PAUSE
    elif JEU.menu_pause.est_actif and JEU.joueur.est_vivant:
        JEU.menu_ameliorations.est_actif = False
        JEU.menu_developpeur.est_actif = False
        JEU.menu_pause.update()
        pygame.display.flip()
        clock.tick(JEU.fps)

    else:
        JEU.update()