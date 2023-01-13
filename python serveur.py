HOST = '192.168.1.101'
PORT = 20000

import socket, sys, threading
import RPi.GPIO as GPIO


  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

duty0= 50
duty1= 50
    
moteurdroit= 32
moteurgauche=33

GPIO.setup(moteurdroit,GPIO.OUT)
GPIO.setup(moteurgauche,GPIO.OUT)

pi_pwm0 =GPIO.PWM(moteurdroit,530)
pi_pwm1 =GPIO.PWM(moteurgauche,530)

pi_pwm0.start(0)
pi_pwm1.start(0)
    

 
class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    
  
    
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
    
    
        
    def run(self):
        # Dialogue avec le client :
        nom = self.getName()        # Chaque thread possède un nom
        while 1:
            msgClient = self.connexion.recv(1024)
            message = "%s> %s" %(nom, msgClient)
            print (message)
            
            if (msgClient == b'A'):
                #PWM pour avancer
                pi_pwm0.ChangeDutyCycle(85)
                pi_pwm1.ChangeDutyCycle(85)
                
                
            if (msgClient == b'R'):
                #PWM pour reculer

                pi_pwm0.ChangeDutyCycle(65)
                pi_pwm1.ChangeDutyCycle(65)
                
            if (msgClient == b'S'):
                #PWM pour stoper
                pi_pwm0.ChangeDutyCycle(75)
                pi_pwm1.ChangeDutyCycle(75)

                
            if (msgClient == b'D'):
                #PWM pour droite
                pi_pwm0.ChangeDutyCycle(85)
                pi_pwm1.ChangeDutyCycle(65)

                
            if (msgClient == b'G'):
                #PWM pour gauche
                pi_pwm0.ChangeDutyCycle(65)
                pi_pwm1.ChangeDutyCycle(85)
                
            if msgClient.upper() == b'FIN' or msgClient ==b'':
                
                pi_pwm0.ChangeDutyCycle(0)
                pi_pwm1.ChangeDutyCycle(0)
                break
            
        message = "%s> %s" %(nom, msgClient)
        print ("message")
            # Faire suivre le message à tous les autres clients :
        for cle in conn_client:
                if cle != nom:      # ne pas le renvoyer à l'émetteur
                    conn_client[cle].send(b'message')
                    
        # Fermeture de la connexion :
        self.connexion.close()      # couper la connexion côté serveur
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print ("Client %s déconnecté." %nom)
        return duty0,duty1
        # Le thread se termine ici    



        


# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print ("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
print  ("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients
while 1:    
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    th.start()
    # Mémoriser la connexion dans le dictionnaire : 
    it = th.getName()        # identifiant du thread
    conn_client[it] = connexion
    print ("Client %s connecté, adresse IP %s, port %s." %(it, adresse[0], adresse[1]))
    # Dialogue avec le client :
    connexion.send(b'Vous etes connecte. Envoyez vos messages')
    