# Diagrammes de Séquence - Plateforme E-Learning

## 1. Inscription et Authentification

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant F as Frontend
    participant B as Backend
    participant DB as Base de données

    U->>F: Accède au formulaire d'inscription
    F->>B: Envoie les données du formulaire
    B->>B: Valide les données
    B->>DB: Vérifie si l'email existe
    DB-->>B: Retourne le résultat
    alt Email existe déjà
        B-->>F: Erreur: Email déjà utilisé
        F-->>U: Affiche message d'erreur
    else Email disponible
        B->>B: Hash du mot de passe
        B->>DB: Crée nouvel utilisateur
        DB-->>B: Confirme création
        B-->>F: Succès de l'inscription
        F-->>U: Redirige vers connexion
    end
```

## 2. Création et Publication d'un Cours

```mermaid
sequenceDiagram
    actor I as Instructeur
    participant F as Frontend
    participant B as Backend
    participant DB as Base de données
    participant S as Stockage

    I->>F: Accède à l'interface de création
    F->>B: Vérifie les droits d'accès
    B-->>F: Confirme les droits
    I->>F: Remplit les détails du cours
    I->>F: Upload contenu (vidéos, docs)
    F->>B: Envoie données du cours
    B->>S: Stocke les fichiers
    S-->>B: Confirme stockage
    B->>DB: Enregistre métadonnées
    DB-->>B: Confirme enregistrement
    B-->>F: Cours créé avec succès
    F-->>I: Affiche confirmation
```

## 3. Inscription à un Cours

```mermaid
sequenceDiagram
    actor E as Étudiant
    participant F as Frontend
    participant B as Backend
    participant DB as Base de données

    E->>F: Recherche un cours
    F->>B: Requête liste des cours
    B->>DB: Récupère les cours
    DB-->>B: Retourne les cours
    B-->>F: Affiche les cours
    E->>F: Sélectionne un cours
    F->>B: Demande d'inscription
    B->>DB: Vérifie inscription existante
    alt Déjà inscrit
        DB-->>B: Inscription existe
        B-->>F: Erreur: Déjà inscrit
        F-->>E: Affiche message
    else Pas encore inscrit
        B->>DB: Crée inscription
        DB-->>B: Confirme inscription
        B-->>F: Inscription réussie
        F-->>E: Accès au cours accordé
    end
```

## 4. Suivi de Progression

```mermaid
sequenceDiagram
    actor E as Étudiant
    participant F as Frontend
    participant B as Backend
    participant DB as Base de données

    E->>F: Accède au cours
    F->>B: Demande progression
    B->>DB: Récupère données progression
    DB-->>B: Retourne progression
    B-->>F: Affiche progression
    E->>F: Complète une leçon
    F->>B: Met à jour progression
    B->>DB: Enregistre progression
    DB-->>B: Confirme mise à jour
    B-->>F: Progression mise à jour
    F-->>E: Affiche nouvelle progression
```

## 5. Administration

```mermaid
sequenceDiagram
    actor A as Admin
    participant F as Frontend
    participant B as Backend
    participant DB as Base de données

    A->>F: Accède au panel admin
    F->>B: Vérifie droits admin
    B->>DB: Vérifie permissions
    DB-->>B: Confirme permissions
    B-->>F: Autorise accès
    A->>F: Gère utilisateurs/cours
    F->>B: Envoie modifications
    B->>DB: Applique modifications
    DB-->>B: Confirme changements
    B-->>F: Modifications appliquées
    F-->>A: Affiche confirmation
```