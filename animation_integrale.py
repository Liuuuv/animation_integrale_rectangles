import pygame as py
import math
import numpy as np
from scipy.integrate import quad
from sympy import*

py.init()
# py.display.set_caption("base")



blanc=(255,255,255)
noir=(0,0,0)
gris_clair=(200,200,200)

rouge=(255,0,0)
vert=(0,255,0)

inf=float('inf')


class Affichage:
    def __init__(self,facteur):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        # self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)

        self.fps=10



        self.police=py.font.Font(None,23)

        self.facteur_x=200
        self.facteur_y=340

        self.origine=[int(self.dimensions[0]*(0.25)),int(self.dimensions[1]*(0.2))]

        self.liste_abscisses=np.linspace(0.01,8,600)
        self.liste_points=[]
        self.calculer_coordonnees_points()

        self.origine[1]=self.dimensions[1]-self.origine[1]


        self.x_debut=1
        self.x_fin=2
        self.nb_rectangles=1

        self.aire_rectangles_dessous=None

        self.valeur_exacte=quad(self.fonction,self.x_debut,self.x_fin)[0]
        # print(self.valeur_exacte)



    def fonction(self,x):
        return 1/x

    def calculer_coordonnees_points(self):
        for x in self.liste_abscisses:
            y=self.fonction(x)
            self.liste_points.append((x+self.origine[0],self.dimensions[1]-(y+self.origine[1])))

    def calculer_points_rectangles(self):
        self.epaisseur_rectangles=(self.x_fin-self.x_debut)/self.nb_rectangles



        self.liste_rectangles=[]

        x=self.x_debut
        self.aire_rectangles_dessous=0
        self.aire_rectangles_dessus=0
        for _ in range(self.nb_rectangles):
            UL=[x,self.fonction(x)]
            UR=[x+self.epaisseur_rectangles,self.fonction(x)]
            DR=[x+self.epaisseur_rectangles,0]
            DL=[x,0]
            self.liste_rectangles.append([UL,UR,DR,DL])


            UL=[x,self.fonction(x+self.epaisseur_rectangles)]
            UR=[x+self.epaisseur_rectangles,self.fonction(x+self.epaisseur_rectangles)]
            DR=[x+self.epaisseur_rectangles,0]
            DL=[x,0]
            self.liste_rectangles.append([UL,UR,DR,DL])


            self.aire_rectangles_dessus+=self.epaisseur_rectangles*self.fonction(x)
            self.aire_rectangles_dessous+=self.epaisseur_rectangles*self.fonction(x+self.epaisseur_rectangles)



            x+=self.epaisseur_rectangles
        # print(self.aire_rectangles_dessous)


    def dessiner_rectangles(self):
        for rectangle in self.liste_rectangles:
            UL=[
            (rectangle[0][0])*self.facteur_x+self.origine[0],
            (-rectangle[0][1])*self.facteur_y+self.origine[1]
            ]
            UR=[
            (rectangle[1][0])*self.facteur_x+self.origine[0],
            -(rectangle[1][1])*self.facteur_y+self.origine[1]
            ]
            DR=[
            (rectangle[2][0])*self.facteur_x+self.origine[0],
            (-rectangle[2][1])*self.facteur_y+self.origine[1]
            ]
            DL=[
            (rectangle[3][0])*self.facteur_x+self.origine[0],
            (-rectangle[3][1])*self.facteur_y+self.origine[1]
            ]

            py.draw.polygon(self.fenetre,noir,[UL,UR,DR,DL],1)
            # print([UL,UR,DR,DL])


    def dessiner_fonction(self):
        # self.origine[1]=self.dimensions[1]-self.origine[1]
        for i in range(len(self.liste_points)-1):
            point_i=[(self.liste_points[i][0]-self.origine[0])*self.facteur_x+self.origine[0],(self.liste_points[i][1]-self.origine[1])*self.facteur_y+self.origine[1]]
            point_i1=[(self.liste_points[i+1][0]-self.origine[0])*self.facteur_x+self.origine[0],(self.liste_points[i+1][1]-self.origine[1])*self.facteur_y+self.origine[1]]
            py.draw.line(self.fenetre,noir,point_i,point_i1,2)
            # print(point_i)
        # self.origine[1]=self.dimensions[1]-self.origine[1]

    def dessiner_grille(self):
        largeur_x=self.facteur_x
        compteur=0
        for x in range(0,self.dimensions[0],largeur_x):
            py.draw.line(self.fenetre,gris_clair,[self.origine[0]-x,0],[self.origine[0]-x,self.dimensions[1]])
            py.draw.line(self.fenetre,gris_clair,[self.origine[0]+x,0],[self.origine[0]+x,self.dimensions[1]])

            texte_surface=self.police.render(str(compteur),True,noir)
            self.fenetre.blit(texte_surface,(x+self.origine[0]-5,self.origine[1]+5))
            compteur+=1


        largeur_y=self.facteur_y
        for y in range(0,self.dimensions[0],largeur_y):
            py.draw.line(self.fenetre,gris_clair,[0,self.origine[1]-y],[self.dimensions[0],self.origine[1]-y])
            py.draw.line(self.fenetre,gris_clair,[0,y+self.origine[1]],[self.dimensions[0],y+self.origine[1]])

    def dessiner_axes(self):
        py.draw.line(self.fenetre,noir,[0,self.origine[1]],[self.dimensions[0],self.origine[1]],2)
        py.draw.line(self.fenetre,noir,[self.origine[0],0],[self.origine[0],self.dimensions[1]],2)

    def i_ieme_decimale(self,nombre,i):
        return int((nombre * 10**i)%10)

    def couleur_dessous(self,i):    # i-ieme decimale
        for l in range(i+1):
            if self.i_ieme_decimale(self.aire_rectangles_dessous,l)!=self.i_ieme_decimale(self.valeur_exacte,l):
                return noir
        return vert

    def couleur_dessus(self,i):    # i-ieme decimale
        for l in range(i+1):
            if self.i_ieme_decimale(self.aire_rectangles_dessus,l)!=self.i_ieme_decimale(self.valeur_exacte,l):
                return noir
        return vert

    def generer_formule(self):


        x=symbols('x')

        formule_latex = latex(1/x)
        formule_latex = str("$y=") + str(formule_latex) + str("$")

        preview(formule_latex, viewer='file', filename='temp.png', euler=False, dvioptions=["-T", "tight", "--truecolor", "-D", str(150)])
        image_latex = py.image.load('temp.png').convert_alpha()

        # Enlever le fond blanc
        for x in range(image_latex.get_width()):
            for y in range(image_latex.get_height()):
                pixel_color = image_latex.get_at((x, y))
                if pixel_color == blanc:
                    image_latex.set_at((x, y), (0, 0, 0, 0))  # Mettre le pixel en transparent

        return image_latex

    def loop(self):
        horloge=py.time.Clock()

        image_latex=self.generer_formule()

        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False

            keys = py.key.get_pressed()
            if keys[py.K_s]:
                self.fps-=5
            if keys[py.K_z]:
                self.fps+=5
            self.fps=np.clip(self.fps,0.3,inf)


            horloge.tick(self.fps)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            self.fenetre.fill(blanc)



            self.dessiner_grille()
            self.dessiner_axes()
            self.dessiner_fonction()

            self.calculer_points_rectangles()
            self.dessiner_rectangles()

            texte_surface1=self.police.render("number of rectangles:"+str(self.nb_rectangles),True,noir)
            self.fenetre.blit(texte_surface1,(470,110))

            texte_surface2=self.police.render("total area of the rectangles:",True,noir)
            self.fenetre.blit(texte_surface2,(470,130))

            texte_surface3=self.police.render("small ones:",True,noir)
            self.fenetre.blit(texte_surface3,(600,170))

            texte_surface4=self.police.render("big ones:",True,noir)
            self.fenetre.blit(texte_surface4,(600,200))

            self.fenetre.blit(image_latex,(645,280))


            # dessous
            segments=[(str(self.i_ieme_decimale(self.aire_rectangles_dessous,0)),self.couleur_dessous(0))]+[(str(',')+str(self.i_ieme_decimale(self.aire_rectangles_dessous,1)),self.couleur_dessous(1))]+[(str(self.i_ieme_decimale(self.aire_rectangles_dessous,i)),self.couleur_dessous(i)) for i in range(2,6)]+[(str("..."),noir)]


            x_position=685
            for segment, couleur in segments:
                rendu_segment = self.police.render(segment, True, couleur)
                self.fenetre.blit(rendu_segment, (x_position,170))
                x_position += rendu_segment.get_width()

            # dessus
            segments=[(str(self.i_ieme_decimale(self.aire_rectangles_dessus,0)),self.couleur_dessus(0))]+[(str(',')+str(self.i_ieme_decimale(self.aire_rectangles_dessus,1)),self.couleur_dessus(1))]+[(str(self.i_ieme_decimale(self.aire_rectangles_dessus,i)),self.couleur_dessus(i)) for i in range(2,6)]+[(str("..."),noir)]


            x_position=670
            for segment, couleur in segments:
                rendu_segment = self.police.render(segment, True, couleur)
                self.fenetre.blit(rendu_segment, (x_position,200))
                x_position += rendu_segment.get_width()



            self.nb_rectangles+=1


            py.display.flip()

        py.quit()


facteur=0.6
affichage=Affichage(facteur)
affichage.loop()