import sqlite3
from sqlite3 import Error

#? pour cree un nouvelle bd avec sql
def create_connection():
    conn = None;
    #s'il y a un problem il va afficher un mesasage d'erreur
    try:
        conn = sqlite3.connect('banque.db') 
        print(sqlite3.version)

    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    conn.close()

#? class base de donnees pour gerer bd

class DatabaseManager:
    def fetch_all_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );""")
        self.conn.commit()

    def insert_admin(self, admin):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO admins(nom, prenom, email, password) VALUES(?,?,?,?)""", 
        (admin.nom, admin.prenom, admin.email, admin.password))
        self.conn.commit()

    def insert_client(self, client):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT INTO clients(nom, prenom, email, password) VALUES(?,?,?,?)""", 
            (client.nom, client.prenom, client.email, client.password))
            self.conn.commit()
            banque.add_client(client)
        except Error as e:
            print(f"il y a un error")

    def delete_client(self, client):
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM clients WHERE nom = ? AND prenom = ? AND email = ?""", (client.nom, client.prenom, client.email))
        self.conn.commit()
        for c in banque.clients:
            if c.nom == client.nom and c.prenom == client.prenom and c.email == client.email:
                banque.delete_client(c)
                break

    
    def close(self):
        self.conn.close()


#? class client

class Client:
    def __init__(self, nom, prenom, email, password ):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        self.patrimoine = 0

    def depot_argent(self, quantite):
        self.patrimoine += quantite

    def retrait_argent(self, quantite):
        if self.patrimoine >= quantite:
            self.patrimoine -= quantite
        else:
            return "solde insuffisant!"
        
    def transfert_argent(self, autre_client, quantite):
        if self.patrimoine >= quantite:
            self.patrimoine -= quantite
            autre_client.patrimoine += quantite
        else:
            return "solde insuffisant!"
        
    def login(self, email, password):
        if email == self.email and password == self.password:
            return True
        else:
            return False
              
    def change_password(self, new_password):
        self.password = new_password

#? class admin

class Admin:
    def __init__(self, nom, prenom, email, password, db_manager):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        self.db_manager = db_manager

    def login(self, email, password):
        if email == self.email and password == self.password:
            return True
        else:
            return False
    
    def add_client(self, client):
        self.db_manager.insert_client(client)
        

    def delete_client(self, client):
        self.db_manager.delete_client(client)
        

#? class banque

class Banque:
    def __init__(self):
        self.clients = []
    
    def add_client(self, client):
        self.clients.append(client)
    
    def delete_client(self,client):
        self.clients.remove(client)
    
    def list_client(self):
        for client in self.clients:
            print(client.nom)

    def check_solde(self,client):
        return client.patrimoine



banque = Banque()
db_manager = DatabaseManager('banque.db')
candas = Admin("candas", "kuran", "candas@mail", "12345", db_manager)

while True:
    print("Bienvenue dans le menu principal de mon banque !")
    etape = input("Pour l'interface client appuyez '1', pour l'interface admin appuyez '2', pour quitter appuyez '3': ")

    if etape == '1':
        #? Customer menu...
        email = input("Entrez votre email : ")
        password = input("Entrez votre mot de passe : ")
        current_client = None
        
        #? on va verifier l'adresse email et password
        for client in banque.clients:
            if client.login(email, password):
                current_client = client
                break

        #? si le client est deja exist dans le clinet on va continuer avec cette menu       
        if current_client is not None:
           while True:
            print("Bienvenue dans le menu de l'utilisateur !")
            user_action = input("Que souhaitez-vous faire? 'change_nom', 'change_prenom', 'change_email', 'change_password', 'quit'")
            if user_action == 'change_nom':
                new_nom = input("Entrez le nouveau nom : ")
                current_client.nom = new_nom
                print("Votre nom a été changé avec succès !")
            elif user_action == 'change_prenom':
                new_prenom = input("Entrez le nouveau prenom : ")
                current_client.prenom = new_prenom
                print("Votre prenom a été changé avec succès !")
            elif user_action == 'change_email':
                new_email = input("Entrez le nouveau email : ")
                current_client.email = new_email
                print("Votre email a été changé avec succès !")
            elif user_action == 'change_password':
                new_password = input("Entrez le nouveau mot de passe : ")
                current_client.change_password(new_password)
                print("Votre mot de passe a été changé avec succès !")
            elif user_action == 'quit':
                break
            else:
                print("Action non valide !")
        else:
            print("Email ou mot de passe incorrect.")

    elif etape == '2':
        #? mene ADMIN
        email = input("Admin email: ")
        password = input("Admin password: ")
        if candas.login(email, password):
            while True:
                print("Bienvenue dans le menu admin de mon banque !")
                user_action = input("Sélectionnez l'opération que vous souhaitez effectuer - 'add_client' ,'delete_client','quit'")
                 #? pour ajouter nouvelle client dans le class client
                if user_action == "add_client":
                    nom = input("Entrez le nom du client : ")
                    prenom = input("Entrez le prenom du client : ")
                    email = input("Entrez l'email du client : ")
                    password = input("Entrez le mot de passe du client : ")
                    client = Client(nom, prenom, email, password)
                    db_manager.insert_client(client)
                    print(f"le client a été ajouter avec succes => {prenom} {nom}")
                    db_manager.fetch_all_clients() 

                #?  pour supprimer un client dans le class client ssil est existe
                
                elif user_action == "delete_client":
                    nom = input("Entrez le nom du client : ")
                    prenom = input("Entrez le prenom du client : ")
                    email = input("Entrez l'email du client : ")

                    client_a_supprimer = None
                    for client in banque.clients:
                        if client.nom == nom and client.prenom == prenom and client.email == email:
                            client_a_supprimer = client
                            break

                    if client_a_supprimer is not None:
                        db_manager.delete_client(client_a_supprimer)
                        print(f"Le client {prenom} {nom} a été supprimé avec succès.")
                    else:
                        print("Aucun client avec ces informations n'a été trouvé.")

                        #--
                else:
                    user_action = "quit"
                    break
        
        else:
            print("Email ou mot de passe incorrect.")
   

    elif etape == '3':
        break

    else:
        print("Opération non valide !")

db_manager.close()

#!------------------------------------------------------------------------------


