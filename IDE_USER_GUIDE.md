# 💻 Guide d'Utilisation de l'IDE ConnectScript

## 🚀 Démarrage de l'IDE

1. **Lancer le serveur web:**
```bash
python3 -m http.server 8000
```

2. **Ouvrir dans le navigateur:**
```
http://localhost:8000
```

Vous verrez une interface divisée en 3 panneaux:
- **À gauche**: Explorer (Pages et Scripts)
- **Au centre**: Éditeur de code
- **À droite**: Aperçu/Prévisualisation

## 📌 Interface Utilisateur

### Panneau Explorateur (Gauche)

**Pages:**
- Affiche toutes les pages créées
- Cliquez sur une page pour l'éditer
- Bouton "➕" pour ajouter une page
- Bouton "🗑️" pour supprimer une page

**Scripts:**
- Affiche tous les scripts (gestionnaires d'événements)
- Cliquez sur un script pour l'éditer
- Bouton "➕" pour ajouter un script

### Panneau Éditeur (Centre)

- **Syntaxe**: Écrire du code ConnectScript
- **Auto-save**: Votre code est sauvegardé automatiquement
- **Validation**: Les erreurs s'affichent en bas après compilation

### Panneau Prévisualisation (Droite)

- **Canvas**: Visualisation de votre application
- **Console**: Affiche les logs et erreurs d'exécution
- **Bouton "Run"**: Relancer la compilation

## 🎮 Créer Votre Première App

### Étape 1: Créer une Page

1. Cliquez sur "➕ New Page" dans le panneau Pages
2. Nommez votre page (ex: "Home")
3. L'éditeur affiche maintenant:

```
page Home
-background
--color lightblue
```

### Étape 2: Ajouter des Éléments

Modifiez le code pour ajouter des boutons et textes:

```
page Home
-background
--color lightblue

-text title
--value "Mon Application"
--color darkblue
--position 50 50
--fontsize 24

-button playBtn
--text "Start Game"
--color green
--position 150 250
--size 150 50
--corner 8
--fontsize 16
```

### Étape 3: Ajouter un Script

1. Cliquez sur "➕ New Script" dans le panneau Scripts
2. Nommez votre script (ex: "gameController")
3. Écrivez les événements:

```
on start
 set score 0
 alert("Game Started!")
end

on click
 add score 10
 alert("You earned 10 points!")
end

on tick
 subtract timer 1
end
```

### Étape 4: Visualiser

- Cliquez sur "Run" dans le panneau droit
- Votre application s'affiche dans le canvas
- Cliquez sur les boutons pour déclencher les événements
- Regardez la console pour les messages

## 🎨 Propriétés des Éléments

### Texte (text)
```
-text myText
--value "Texte affiché"
--color blue
--position 100 200
--fontsize 24
```

### Bouton (button)
```
-button myBtn
--text "Click me"
--color green
--position 100 200
--size 150 50
--corner 8
--fontsize 16
--script myScript
```

### Image (image)
```
-image myImage
--source "url_of_image"
--position 100 200
--size 200 200
```

### Fond (background)
```
-background
--color #3498db
```

## ⚙️ Propriétés Disponibles

| Propriété | Type | Exemple |
|-----------|------|---------|
| `color` | hex ou nom | `#3498db` ou `green` |
| `value` | texte | `"Hello"` |
| `text` | texte | `"Click me"` |
| `position` | x y | `100 200` |
| `size` | width height | `150 50` |
| `fontsize` | nombre | `24` |
| `corner` | nombre | `8` |
| `source` | url | `"image.png"` |

## 🎬 Événements Disponibles

### on start
Déclenché au démarrage de l'application
```
on start
 set level 1
 alert("Welcome!")
end
```

### on click
Déclenché quand un bouton est cliqué
```
on click
 add score 10
end
```

### on tick
Déclenché chaque frame (périodiquement)
```
on tick
 subtract timer 1
 alert("Tick!")
end
```

### on load
Déclenché au chargement d'une page
```
on load
 alert("Page loaded")
end
```

## 🔧 Actions Disponibles

### alert
Affiche un message
```
alert("Message")
```

### set
Définit une variable
```
set playerScore 0
set playerName "Alice"
```

### add
Ajoute une valeur
```
add score 10
add lives 1
```

### subtract
Soustrait une valeur
```
subtract lives 1
subtract timer 5
```

### connect.goto
Navigue vers une page
```
connect.goto(HomePage)
connect.goto(GamePage)
```

### if
Condition
```
if score > 100
 alert("High score!")
end
```

## 💾 Sauvegarder et Charger

### Sauvegarder
- Votre code est **auto-sauvegardé** dans le localStorage du navigateur
- À chaque modification, le code est sauvegardé automatiquement

### Charger
- Quand vous revenez, votre code est automatiquement restauré
- Aucune action supplémentaire nécessaire

## 🐛 Déboguer

### Console
Regardez le panneau "Console" à droite pour:
- Les messages `alert()`
- Les erreurs de compilation
- Les réactions aux clics
- Les logs de débogage

### Messages d'Erreur

Si vous avez une erreur:
```
Erreur: Identifiant inconnu 'foo'
Ligne: 5
Message: La variable 'foo' n'est pas définie
```

**Solutions:**
- Vérifiez l'orthographe
- Vérifiez les guillemets autour des textes
- Vérifiez l'indentation

## 📱 Exemple Complet: Mini-Jeu

Voici un exemple d'un simple jeu cliquable:

**Page homePage:**
```
page HomePage
-background
--color #1a1a2e

-text title
--value "CLICK CLICKER"
--color #00ff00
--position 100 50
--fontsize 48

-button startBtn
--text "JOUER"
--color #00ff00
--position 150 250
--size 180 60
--corner 10
--fontsize 24
```

**Page gamePage:**
```
page GamePage
-background
--color #16213e

-text scoreDisplay
--value "Score: 0"
--color #00ff00
--position 20 20
--fontsize 32

-text timerDisplay
--value "Temps: 30"
--color #ff0000
--position 400 20
--fontsize 32

-button clickZone
--text "CLIQUEZ!"
--color #00ff00
--position 200 300
--size 200 100
--corner 5
--fontsize 32
```

**Script gameLogic:**
```
on start
 set score 0
 set timer 30
 alert("Jeu commencé! Vous avez 30 secondes!")
 connect.goto(GamePage)
end

on click
 add score 100
 subtract timer 1
 if timer == 0
  alert("Temps écoulé! Score final: " score)
  connect.goto(HomePage)
 end
end
```

## 🎓 Conseils et Bonnes Pratiques

1. **Commencez simple**: Une page, quelques boutons
2. **Testez progressivement**: Ajoutez une fonctionnalité à la fois
3. **Utilisez des noms explicites**: `nextPageBtn` plutôt que `btn`
4. **Organisez vos scripts**: Un script par fonctionnalité
5. **Vérifiez la console**: Elle montre tous les erreurs
6. **Commentez votre code**: Les `--` créent des commentaires
7. **Testez la navigation**: Assurez-vous que `connect.goto()` fonctionne

## ❓ FAQ

**Q: Comment j'ajoute plusieurs pages?**
A: Cliquez "➕ New Page" autant de fois que needed. Utilisez `connect.goto(PageName)` pour naviguer.

**Q: Peux-je avoir plusieurs boutons?**
A: Oui! Ajoutez plusieurs `-button` éléments dans votre page.

**Q: Quand utiliser `on click` vs `on click`?**
A: Mettez un '--script' sur le bouton pour spécifier quel script gère ses clics.

**Q: Comment déboguer?**
A: Regardez la console (panneau droit) pour tous les messages et erreurs.

**Q: Mon code ne fonctionne pas!**
A: 
1. Vérifiez la console pour les erreurs
2. Vérifiez l'orthographe des noms
3. Vérifiez les guillemets autour des textes
4. Cliquez "Run" pour récompiler

---

**Amusez-vous à créer avec ConnectScript! 🎨**
