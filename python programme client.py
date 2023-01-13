# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, time

HOST = '192.168.1.101'
PORT = 20000

# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) envoi d'une requête de connexion au serveur :
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print ("La connexion a échoué.")
    sys.exit()    
print ("Connexion établie avec le serveur.")    

# 3) Dialogue avec le serveur :
msgServeur = mySocket.recv(1024)

while 1:
    if msgServeur.upper() == "FIN" or msgServeur =="":
        break
    print ("S>", msgServeur)
    msgClient = input("C> ")
    if (msgClient == 'A'): #AVANCE
        mySocket.send(b'A')
        time.sleep(2)
        mySocket.send(b'S')
    elif (msgClient == 'R'): #RECULE
        mySocket.send(b'R')
        time.sleep(2)
        mySocket.send(b'S')
    elif (msgClient == "G"): #GAUCHE
        mySocket.send(b'G')
        time.sleep(2)
        mySocket.send(b'S')
    elif (msgClient == "D"): #DROITE
        mySocket.send (b'D')
        time.sleep(2)
        mySocket.send(b'S')
    elif (msgClient == "S"): #STOP
        mySocket.send (b'S')
         
    elif (msgClient == "F"): #FIN
        mySocket.send(b'Fin')
        
    
    
    #msgServeur = mySocket.recv(1024)

# 4) Fermeture de la connexion :
print ("Connexion interrompue.")
mySocket.close()