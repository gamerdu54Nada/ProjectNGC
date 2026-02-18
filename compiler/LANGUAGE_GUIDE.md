# ConnectScript Language Guide

## Guide Professionnel - Moteur de Compilation DSL

Ceci est un guide complet pour le langage **ConnectScript**, un DSL (Domain Specific Language) pour créer des applications visuelles interactives.

---

## 📚 Table des matières

1. [Architecture du Compilateur](#architecture)
2. [Syntaxe du Langage](#syntaxe)
3. [Système d'Événements](#événements)
4. [Bonnes Pratiques](#bonnes-pratiques)
5. [Exemples Complets](#exemples)
6. [Guide de Dépannage](#dépannage)

---

## Architecture du Compilateur {#architecture}

### Étapes de Compilation

```
Code Source (.psx, .psc)
         ↓
    [TOKENIZER] → List[Token]
         ↓
    [PARSER] → AST (Abstract Syntax Tree)
         ↓
    [VALIDATOR] → Vérification des erreurs
         ↓
    [CODE GENERATOR] → JavaScript
         ↓
    Exécution sûre (sans eval())
```

### Composants

| Composant | Rôle | Fichier |
|-----------|------|---------|
| **Tokenizer** | Découpe le code en tokens | `tokenizer.py` |
| **Parser** | Crée l'AST | `parser.py` |
| **Error Manager** | Gestion des erreurs | `errors.py` |
| **Code Generator** | Génère le JS | `codegen.py` |
| **Event System** | Système d'événements | `event_system.py` |
| **AST Nodes** | Structure de données | `ast_nodes.py` |

---

## Syntaxe du Langage {#syntaxe}

### 1. Déclaration de Pages (.psx)

```connectscript
page NomDeLaPage
-background
--color lightblue

-text labelName
--value "Texte visible"
--color darkblue
--position 50 50
--fontsize 24

-button buttonName
--text "Click me"
--color green
--position 100 150
--size 150 50
--corner 8
--fontsize 16
--script scriptName
```

**Propriétés des éléments:**
- `position <x> <y>` - Coordonnées en pixels (toujours deux nombres)
- `size <width> <height>` - Largeur et hauteur en pixels
- `color <couleur>` - CSS color ou hex (#FF0000)
- `fontsize <taille>` - Taille en pixels
- `corner <radius>` - Bordures arrondies (pixels)

### 2. Déclaration de Scripts (.psc)

```connectscript
# Script déclenché au clic
on click
 alert("Vous avez cliqué!")
 set score 0
 add lives 1
 connect.goto(NextPage)
end

# Script exécuté au démarrage
on start
 set playerName "Hero"
 alert("Bienvenue!")
end

# Script exécuté à chaque frame (tick)
on tick
 subtract timer 1
 if timer == 0
  alert("Temps écoulé!")
 end
end
```

### 3. Actions Disponibles

#### Alert
```connectscript
alert("Message à afficher")
```

#### Navigation
```connectscript
connect.goto(PageName)
```

#### Variables
```connectscript
set myVar 42                    # Assigner une valeur
set playerName "Alice"          # Assigner une string
add score 10                    # Ajouter à une variable
subtract health 5               # Soustraire d'une variable
```

#### Temporisation
```connectscript
wait(2)  # Attendre 2 secondes
```

#### Son (futur)
```connectscript
play("sounds/beep.mp3")
```

---

## Système d'Événements {#événements}

### Types d'Événements

| Événement | Déclencheur | Usage |
|-----------|------------|-------|
| `click` | Clic sur un button | Interactions utilisateur |
| `start` | Chargement de l'app | Initialisation |
| `load` | Affichage d'une page | Logique de page |
| `tick` | Frame (30/s) | Animations, timers |

### Architecture du Système

```python
# Event Bus Pattern
event_bus = EventBus()

# Abonnement
def on_click(event):
    print(f"Clicked: {event.source}")

unsubscribe = event_bus.on(EventType.CLICK, on_click)

# Émission
event = Event(
    type=EventType.CLICK,
    source="button_play",
    data={"x": 100, "y": 50}
)
event_bus.emit(event)
```

### Avantages

✅ **Type-safe** - Types définis à la compilation  
✅ **Sans eval()** - Code généré statiquement  
✅ **Traçable** - Historique des événements  
✅ **Découplé** - Composants indépendants  

---

## Bonnes Pratiques {#bonnes-pratiques}

### 1. Nommage

```connectscript
# ✅ BON
page GameOver
-button retryBtn
--script retryHandler

-text gameOverMsg
--value "Game Over"

# ❌ MAUVAIS
page p1
-button btn1
--script s1
```

### 2. Commentaires

```connectscript
# Ceci est un commentaire
# Explique le but de chaque section

page MainMenu
-background
--color lightblue

# Bouton pour démarrer
-button startButton
--text "Start"
--position 50 100
```

### 3. Sécurité

```connectscript
# ✅ BON - Pas d'accès direct au DOM
alert("Safe message")
set health 100

# ❌ MAUVAIS - Serait bloquer/transpilé
# Pas de variables globales polluantes
# Pas de refs au JavaScript
```

### 4. Modularité

```connectscript
# Créer des scripts réutilisables
on click
 add score 10
 alert("Points +10")
end

# Au lieu de répéter la logique dans chaque button
```

### 5. Performance

```connectscript
# ✅ BON
on start
 set timer 0
end

# ❌ MAUVAIS (à éviter)
on tick
 # Ne pas faire d'opérations lourdes chaque frame
 # Vérifier les conditions avant d'agir
end
```

---

## Exemples Complets {#exemples}

### Exemple 1: Application Simple
```connectscript
# pages.psx
page Home
-background
--color #667eea

-text title
--value "Welcome to ConnectScript"
--color white
--position 50 50
--fontsize 32

-button startBtn
--text "Start Game"
--color white
--position 100 150
--size 200 50
--corner 8
--fontsize 18
--script startGameScript

page GameView
-background
--color #764ba2

-text scoreText
--value "Score: 0"
--color white
--position 50 50
--fontsize 24

-button menuBtn
--text "Back to Menu"
--color red
--position 50 500
--size 150 50
--script backToMenuScript
```

```connectscript
# scripts.psc
on click
 set score 0
 connect.goto(GameView)
 alert("Game Started!")
end

on click
 connect.goto(Home)
end
```

### Exemple 2: Jeu de Points

```connectscript
page Game
-background
--color lightblue

-text pointsDisplay
--value "Points: 0"
--color darkblue
--position 50 50
--fontsize 28

-button addPointsBtn
--text "+10 Points"
--color green
--position 50 150
--size 200 50
--corner 8
--fontsize 16
--script addPointsScript

-text timerDisplay
--value "Time: 30"
--color red
--position 50 250
--fontsize 24
```

```connectscript
# Game Logic
on start
 set points 0
 set timer 30
end

on click
 add points 10
 alert("Points +10")
end

on tick
 subtract timer 1
 if timer == 0
  alert("Game Over!")
 end
end
```

---

## Guide de Dépannage {#dépannage}

### Erreur: "Token inattendu"

```connectscript
# ❌ MAUVAIS
page MyPage  # Pas assez d'indentation
-button btn
--text Click  # Pas de guillemets
```

```connectscript
# ✅ BON
page MyPage
-button btn
--text "Click"
```

### Erreur: "Page non trouvée"

```connectscript
# ❌ MAUVAIS
on click
 connect.goto(NextPage)  # N'existe pas
end

# ✅ BON
page NextPage
-background
--color white

on click
 connect.goto(NextPage)  # Défini avant
end
```

### Erreur: "Variable non définie"

```connectscript
# ❌ MAUVAIS
on click
 set score 100
 
on click
 add score 10  # Ne sait pas si 'score' existe
end

# ✅ BON
on start
 set score 0  # Initialiser d'abord
end

on click
 add score 10  # Maintenant c'est safe
end
```

---

## Conseils Niveau Pro

### 1. Architecture du Projet

Séparez clairement pages et scripts:
```
project/
├── pages/
│   ├── mainMenu.psx
│   ├── gameScreen.psx
│   └── gameOver.psx
└── scripts/
    ├── gameLogic.psc
    ├── menuHandler.psc
    └── playerEvents.psc
```

### 2. Versionning

```connectscript
# Version: 1.0.0
# Author: Votre Nom
# Last Update: 2026-02-18

page GameLevel1
# ...
```

### 3. Optimisation

```connectscript
# ✅ BON - Logique efficace
on tick
 if timer > 0
  subtract timer 1
 end
end

# ❌ MAUVAIS - Trop d'alertes
on tick
 alert("Frame")  # Spam!
end
```

### 4. Validation des Données

Le compilateur valide automatiquement:
- ✅ Noms de variables
- ✅ Existence des pages
- ✅ Syntaxe correcte
- ✅ Types de données

---

## API JavaScript Générée

Le compilateur génère une API sûre:

```javascript
// Objet global accessible
ConnectApp.variables    // Variables du projet
ConnectApp.pages       // Pages disponibles
ConnectApp.events      // Événements enregistrés
ConnectApp.currentPage // Page actuelle

// Méthodes
ConnectApp.init()              // Initialiser
ConnectApp.showPage(name)      // Afficher page
ConnectApp.executeAction(name) // Exécuter action
ConnectApp.registerEvent()     // Enregistrer event
```

---

## Conclusion

ConnectScript est conçu pour:
- 🎯 **Simplicité** - Syntaxe claire et lisible
- 🔒 **Sécurité** - Pas d'eval(), validation stricte
- ⚡ **Performance** - Code généré optimisé
- 🛠️ **Maintenabilité** - Structure propre et modulaire

Pour des questions ou améliorations, consultez la documentation du compilateur!
