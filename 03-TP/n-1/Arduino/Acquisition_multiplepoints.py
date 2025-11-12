#Ce code est developpé par l'IUT d'Orsay dans le cadre
#du module 3.06/3.16 à destination des BUT2
#Auteur : Jean-François Olivieri
#Licence : Creative Commons,  CC-BY-NC-SA
#Attribution, Pas d'utilisation commerciale, Partage dans les mêmes conditions
###############################################
# TP n°1, IV : Acquisition de la tension électrique
# aux bornes d'un accumulateur au plomb
###############################################
#Importation des packages python nécessaire à l'acquisition
from pyfirmata import Arduino, util
import time

## Paramètres à ne pas modifier
_A_tension = "A0" #str, entrée analogique = mesure de la tension
_A_courant = "A1" #str, entrée analogique = mesure du courant
_R = 1000.0 #float, valeur de résistance servant à la mesure du courant

#Paramètres à modifier
COM = '/dev/ttyACM0' # str, entrée analogique associée à la lecture de la tension
dt = 0.5             # float, Pas de temps en seconde    
Dt = 700.0             # Durée d'un demi-cycle de charge/décharge = 1 charge ou décharge, en seconde


#Calcul du nombre de pas de temps et correction du pas
N = int(Dt//dt)             # Nombre de demi-cycle
dt = Dt/N                   # Correction du pas d temps si Dt n'est pas un multiple de dt.

#Début de l'acquisition
carte=Arduino(COM)                  #Definition de la cart d'acquisition
acquisition=util.Iterator(carte)    #
acquisition.start()                 #

#Initiation des mesures de tension
tension_0 = carte.get_pin("a:1:i") #définition des entrées de l'arduino, analogique:pin-0:input
tension_1 = carte.get_pin("a:2:i") #définition des entrées de l'arduino, analogique:pin-1:input
tension_2 = carte.get_pin("a:3:i") #définition des entrées de l'arduino, analogique:pin-1:input
time.sleep(1.0)

#Initiation des grandeurs
t = []                          #list, temps
U0n, U1n, U2n = 0.0, 0.0, 0.0             #float, tension au pas de temps n
U0, U1, U2 = [], [], []                 #list, list où seront stockées la tension du générateur et la tension associée au courant

n = 0 #int, pas de temps
t0 = time.time()                #float, temps initial

#Boucle : lectures des valeurs par pas de temps régulier
for n in range(0,N) :
    U0n = tension_0.read()
    U1n = tension_1.read()
    U2n = tension_2.read()
    t.append(time.time() - t0)

    U0.append(U0n)
    U1.append(U1n)
    U2.append(U2n)

    time.sleep(dt)

#Fin de l'acquisition
carte.exit()

#Ecrire d'un fichier dont les colonnes sont t, U0, I=U1/R
newfile=open('Donnee.csv', "w")
newfile.write("Temps[s] ; V0[V] ; V1[V] ; V2[V] \n")
for n in range(0, N) : 
    newfile.write("{t} ; {U0} ; {U1} ; {U2} \n".format(t=t[n], U0 = U0[n], U1 = U1[n], U2 = U2[n]))
newfile.close()
