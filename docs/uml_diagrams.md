# Diagrammes UML - Plateforme E-Learning

## 1. Diagramme de Cas d'Utilisation

```plantuml
@startuml
left to right direction

actor "Étudiant" as student
actor "Instructeur" as instructor
actor "Administrateur" as admin

rectangle "Plateforme E-Learning" {
  usecase "S'inscrire" as UC1
  usecase "Se connecter" as UC2
  usecase "Suivre des cours" as UC3
  usecase "Télécharger des ressources" as UC4
 
  usecase "Créer des cours" as UC6
  usecase "Gérer le contenu" as UC7
  usecase "Gérer les utilisateurs" as UC8
  usecase "Monitorer la plateforme" as UC9
}

student --> UC1
student --> UC2
student --> UC3
student --> UC4
student --> UC5

instructor --> UC2
instructor --> UC6
instructor --> UC7

admin --> UC2
admin --> UC8
admin --> UC9
@enduml
```

## 4. Diagramme de Séquence - Processus d'Inscription aux Cours

```plantuml
@startuml
actor "Étudiant" as student
participant "Interface Web" as web
participant "Système d'Authentification" as auth
participant "Gestionnaire de Cours" as course
database "Base de Données" as db

student -> web : Accède à la page d'inscription
web -> auth : Vérifie l'authentification
alt Utilisateur non connecté
    auth --> web : Demande de connexion
    student -> web : Se connecte
    web -> auth : Valide les identifiants
    auth -> db : Vérifie les credentials
    db --> auth : Confirme l'authentification
    auth --> web : Session authentifiée
end

student -> web : Sélectionne un cours
web -> course : Demande d'inscription
course -> db : Vérifie la disponibilité
db --> course : Confirme la disponibilité
course -> db : Enregistre l'inscription
db --> course : Confirme l'enregistrement
course --> web : Inscription réussie
web --> student : Affiche confirmation
@enduml
```

## 5. Diagramme de Déploiement

```plantuml
@startuml
node "Client" as client {
    component "Navigateur Web" as browser
}

node "Serveur Web" as webserver {
    component "Django Application" as django {
        component "Serveur WSGI" as wsgi
        component "Apps Django" as apps
    }
    component "Serveur ASGI" as asgi {
        component "Channels" as channels
    }
}

node "Serveur de Base de Données" as dbserver {
    database "SQLite" as db
}

node "Serveur de Médias" as mediaserver {
    folder "Fichiers Statiques" as static
    folder "Médias Uploadés" as media
}

client -- webserver : HTTP/HTTPS
browser -- asgi : WebSocket
django -- dbserver : SQL
django -- mediaserver : Fichiers
@enduml
```

## 2. Diagramme de Classes

```plantuml
@startuml
class User {
  -id: Integer
  -username: String
  -email: String
  -password: String
  -role: String
  +login()
  +logout()
}

class Admin {
  -admin_level: String
  +manage_users()
  +monitor_platform()
  +generate_reports()
}

class Instructor {
  -speciality: String
  -bio: String
  +create_course()
  +manage_content()
  +evaluate_students()
}

class Course {
  -id: Integer
  -title: String
  -overview: String
  -created: Date
  -status: String
  +enroll()
  +unenroll()
}

class Module {
  -id: Integer
  -title: String
  -description: String
  -order: Integer
}

class Content {
  -id: Integer
  -content_type: String
  -object_id: Integer
  -order: Integer
}

class Chat {
  -id: Integer
  -message: String
  -timestamp: DateTime
  +send_message()
}

User <|-- Admin
User <|-- Instructor

Instructor "1" -- "*" Course : creates >
User "*" -- "*" Course : enrolls >
Admin "1" -- "*" User : manages >
Course "1" -- "*" Module : contains >
Module "1" -- "*" Content : contains >
User "1" -- "*" Chat : sends >
@enduml
```

## 4. Diagramme de Séquence - Processus d'Inscription aux Cours

```plantuml
@startuml
actor "Étudiant" as student
participant "Interface Web" as web
participant "Système d'Authentification" as auth
participant "Gestionnaire de Cours" as course
database "Base de Données" as db

student -> web : Accède à la page d'inscription
web -> auth : Vérifie l'authentification
alt Utilisateur non connecté
    auth --> web : Demande de connexion
    student -> web : Se connecte
    web -> auth : Valide les identifiants
    auth -> db : Vérifie les credentials
    db --> auth : Confirme l'authentification
    auth --> web : Session authentifiée
end

student -> web : Sélectionne un cours
web -> course : Demande d'inscription
course -> db : Vérifie la disponibilité
db --> course : Confirme la disponibilité
course -> db : Enregistre l'inscription
db --> course : Confirme l'enregistrement
course --> web : Inscription réussie
web --> student : Affiche confirmation
@enduml
```

## 5. Diagramme de Déploiement

```plantuml
@startuml
node "Client" as client {
    component "Navigateur Web" as browser
}

node "Serveur Web" as webserver {
    component "Django Application" as django {
        component "Serveur WSGI" as wsgi
        component "Apps Django" as apps
    }
    component "Serveur ASGI" as asgi {0
        component "Channels" as channels
    }
}

node "Serveur de Base de Données" as dbserver {
    database "MySQL" as db
}

node "Serveur de Médias" as mediaserver {
    folder "Fichiers Statiques" as static
    folder "Médias Uploadés" as media
}

client -- webserver : HTTP/HTTPS
browser -- asgi : WebSocket
django -- dbserver : SQL
django -- mediaserver : Fichiers
@enduml
```

## 6. Diagramme d'État de Transition

```plantuml
@startuml
state "Non Connecté" as NC
state "Connecté" as C
state "En Cours" as EC
state "Terminé" as T
state "En Attente" as EA
state "Publié" as P

[*] --> NC
NC --> C : Authentification

state C {
  state "Étudiant" as E {
    state "Inscription Cours" as IC
    state "Suivi Cours" as SC
    [*] --> IC
    IC --> SC : Inscription validée
    SC --> T : Cours complété
  }
  
  state "Instructeur" as I {
    state "Création Cours" as CC
    state "Édition Cours" as EDC
    [*] --> CC
    CC --> EDC : Brouillon
    EDC --> EA : Soumission
    EA --> P : Validation
  }
}

C --> NC : Déconnexion
@enduml
```

## 3. Diagramme d'Activité

```plantuml
@startuml
start

if (Utilisateur connecté?) then (non)
  :S'authentifier;
else (oui)
endif

if (Role?) then (Instructeur)
  :Créer un cours;
  :Ajouter des modules;
  :Organiser le contenu;
  :Publier le cours;
else (Étudiant)
  :Parcourir les cours;
  :S'inscrire à un cours;
  while (Progression du cours) is (En cours)
    :Suivre le module;
    :Télécharger les ressources;
    :Participer au chat;
  endwhile (Terminé)
endif

stop
@enduml
```