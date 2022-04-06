# -*- python3 pour Raspberry Pi4 -*-
"""
Titre : Buzzer_Led
Projet : Casque vélo
Création : 12 mars 2022
Auteur: Chloe Pelet

"""
import RPi.GPIO as GPIO
import time

#_________________DEBUT_________________Define de note pour pouvoir faire des musiques_________________________________________
#octave 1

DO_1 = 33
D0_1d = 35    # d: dièse
RE_1 =37
RE_1d =39
MI_1 =41
FA_1 =44
FA_1d =47
SOL_1 =49
SOL_1d =52
LA_1 =55
LA_1d =58
SI_1 =62

# octave 2 

DO_2 =131
D0_2d =139 
RE_2 =147
RE_2d =156
MI_2 =165
FA_2 =175
FA_2d =185
SOL_2 =196
SOL_2d =208
LA_2 =220
LA_2d =233
SI_2 =247

# octave 3 

DO_3 =262
D0_3d =277 
RE_3 =294
RE_3d =311
MI_3 =330
FA_3 =349
FA_3d =370
SOL_3 =392
SOL_3d =415
LA_3 =440
LA_3d =466
SI_3 =494

# octave 4 

DO_4 =523
D0_4d =554 
RE_4 =587
RE_4d =622
MI_4 =659
FA_4 =698
FA_4d =740
SOL_4 =784
SOL_4d =831
LA_4 =880
LA_4d =932
SI_4 =988

# octave 5 

DO_5 =1047
D0_5d =1109 
RE_5 =1175
RE_5d =1245
MI_5 =1319
FA_5 =1397
FA_5d =1480
SOL_5 =1568
SOL_5d =1661
LA_5 =1760
LA_5d =1865
SI_5 =1976

# Temps des notes

C =0.25   #croche : 1/2 tps
N =0.5   #noire : 1 tps
P =0.75   #noire pointée : 3/2 tpd
B =1  #blanche : 2 tps
J =1.5  #blanch pointée : 3 tps
R =2  #ronde : 4 tps
S =3 #soupire : note inaudible

#__________________FIN________________Define de note pour pouvoir faire des musiques_________________________________________








#_______________DEBUT________________INITIALISATION__________________________________________________
#GPIO.setmode(GPIO.BCM)          # Configuration en numero GPIO
GPIO.setmode(GPIO.BOARD)         # Configuration en numero pin 
GPIO.setwarnings(False)          # Enlève le warning si on lance plusieur fois le programme

BUZZER = 11                      # Pin n°11
LED = 7                          # Pin n°11


GPIO.setup(BUZZER, GPIO.OUT)     #Active le contrôle du GPIO
GPIO.setup(LED, GPIO.OUT)        #Active le contrôle du GPIO pour la LED
#_______________FIN__________________INITIALISATION__________________________________________________




#_______________DEBUT________________FONCTIONS__________________________________________________
#pour la LED
def lumiere(temps) :
    GPIO.output(LED, GPIO.HIGH) #On l'allume
    time.sleep(temps)           #durée ou la led est allumé
    GPIO.output(LED, GPIO.LOW)  #On l’éteint

#pour le BUZZER mais avec la note de base (très peu agréable)
def buzz():
    GPIO.output(BUZZER, True)
    time.sleep(2) #2 secondes
    GPIO.output(BUZZER, False)

#pour le BUZZER mais avec la note choisie
def note(freq_note, durée_note):
    halveWaveTime = 1 / (freq_note * 2 )
    waves = int(durée_note * freq_note)
    for i in range(waves):
        GPIO.output(BUZZER, True) 
        time.sleep(halveWaveTime)
        GPIO.output(BUZZER, False)
        time.sleep(halveWaveTime)


#pour faire s'allumer le BUZZER (note choisie) et la LED pdt un certain temps donné
def alerte(freq_note, durée_note):
    halveWaveTime = 1 / (freq_note * 2 )
    waves = int(durée_note * freq_note)
    for i in range(waves):
        GPIO.output(BUZZER, True)
        GPIO.output(LED, GPIO.HIGH) 
        time.sleep(halveWaveTime)
        GPIO.output(BUZZER, False)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(halveWaveTime)
    GPIO.output(BUZZER, GPIO.LOW) #On l’éteint
    GPIO.output(LED, GPIO.LOW) #On l'allume
    time.sleep(1)
   
#pour faire une musique
def musique():
    t=0
    #notes=[262,262,392,392,440,440,392,349,349,330,330,294,294,262]
    notes=[DO_3,DO_3,DO_3,Re_3,MI_3,RE_3,Do_3,MI_3,RE_3,RE_3,DO_3]
    #notes=[131,131,196,196,220,220,196,175,175,165,165,147,147,131]
    #duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.25,0.5,0.5,0.5,0.5,0.5,0,5,0.25]
    durées=[N,N,N,N,B,B,N,N,N,N,R]
    for n in notes:
        buzz(n, durées[t])
        time.sleep(durées[t] *0.1)
        t+=1
#_______________FIN___________________FONCTIONS__________________________________________________



 
#_______________DEBUT___________________MAIN__________________________________________________
while(1) :                  #On boucle pour toujours tester si l'enfant est attentif ou non et donc savoir si on active l'alerte
    activation = 1          # mettre la condition qui montre que l'enfant est inatentif 0 si attentif 1 sinon
    if activation :         #si l'enfant est inatitif
        alerte(DO_3, P)     #declenchement de l'alerte

#_______________FIN______________________MAIN__________________________________________________