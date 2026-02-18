# 🚀 ConnectScript - Guide de Référence Rapide

## 📋 Sommaire Rapide

| Tâche | Fichier | Commande |
|-------|---------|----------|
| Lancer l'IDE | `index.html` | `python3 -m http.server 8000` |
| Compiler du code | `compiler/__init__.py` | `from compiler import compile_script` |
| API HTTP | `compiler/api_server.py` | `python3 compiler/api_server.py 5001` |
| Exécuter tests | `compiler/tests.py` | `python3 compiler/tests.py` |
| Voir exemples | `compiler/examples.py` | `python3 compiler/examples.py` |
| Lire la langue | `compiler/LANGUAGE_GUIDE.md` | 📖 Documentation |
| Comprendre l'archi | `compiler/ARCHITECTURE.md` | 📖 Documentation |

## 🎮 Démarrage Rapide (3 Options)

### Option 1️⃣: IDE Web (Plus Facile pour Débutants)

```bash
# Démarrer
python3 -m http.server 8000

# Ouvrir http://localhost:8000 dans le navigateur
```

**Interface:**
- Créer/gérer Pages dans "Pages" expand
- Créer/gérer Scripts dans "Scripts"
- Écrire code au centre
- Voir résultat à droite

### Option 2️⃣: Python Code (Pour Intégrer)

```python
from compiler import compile_script

# Votre code ConnectScript
code = """
page HomePage
-background
--color blue

-button startBtn
--text "Start"
--color green
--position 100 200
--size 150 50

on start
 alert("Welcome!")
 set score 0
end

on click
 add score 10
 alert("Score: 10")
end
"""

# Compiler
result = compile_script(code)

# Utiliser
if result['success']:
    js = result['javascript']  # Code généré
    ast = result['ast']        # Arbre syntaxique
    print(js)
else:
    print("Erreurs:", result['errors'])
```

### Option 3️⃣: API HTTP (Pour Serveurs)

```bash
# Démarrer le serveur API
python3 compiler/api_server.py 5001
```

**Compile via POST:**
```bash
curl -X POST http://localhost:5001/api/compile \
  -H "Content-Type: application/json" \
  -d '{
    "code": "page Home\n-button btn\n--text Click"
  }'
```

**Réponse JSON:**
```json
{
  "success": true,
  "javascript": "const ConnectApp = {...}",
  "ast": {...},
  "errors": [],
  "warnings": []
}
```

## 🛠️ Syntaxe ConnectScript (Résumé)

### Pages
```connectscript
page PageName
-background
--color blue
```

### Éléments UI
```connectscript
-button myBtn
--text "Click"
--color green
--position 100 200
--size 150 50
--corner 8
--fontsize 16
--script scriptName

-text label
--value "Hello"
--color black
--position 50 50
--fontsize 24

-image img
--source "image.png"
--position 100 100
--size 200 200
```

### Événements & Actions
```connectscript
on start
 set variable 0
 alert("Message")
end

on click
 add variable 10
 subtract variable 5
 connect.goto(OtherPage)
 if condition
  alert("True!")
 end
end

on tick
 subtract timer 1
end

on load
 alert("Loaded")
end
```

## 📚 Documentation Disponible

### Pour Utilisateurs
| Document | Contenu | Durée Lecture |
|----------|---------|---------------|
| [IDE_USER_GUIDE.md](IDE_USER_GUIDE.md) | Guide complet IDE | 15 min |
| [compiler/LANGUAGE_GUIDE.md](compiler/LANGUAGE_GUIDE.md) | Langue complète | 30 min |
| [examples.py](compiler/examples.py) | 5 exemples | 20 min |

### Pour Développeurs
| Document | Contenu | Durée Lecture |
|----------|---------|---------------|
| [compiler/ARCHITECTURE.md](compiler/ARCHITECTURE.md) | Architecture | 30 min |
| [compiler/README.md](compiler/README.md) | Vue d'ensemble | 20 min |
| [compiler/INDEX.md](compiler/INDEX.md) | Référence API | 20 min |

### Récapitulatif
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - État complet
- [README_COMPLET.md](README_COMPLET.md) - Vue générale

## 🎯 Cas d'Usage Courants

### Créer un Simple Bouton
```python
code = """
page Home
-button btn
--text "Click me"
--color green

on click
 alert("Clicked!")
end
"""

result = compile_script(code)
js = result['javascript']
```

### Naviguer Entre Pages
```python
code = """
page Home
-button next
--text "Next Page"

page Page2
-button back
--text "Back"

on click
 connect.goto(Page2)
end

on click
 connect.goto(Home)
end
"""

result = compile_script(code)
```

### Gérer des Variables
```python
code = """
page Game
-text score
--value "Score: 0"

-button addBtn
--text "Add Points"

on start
 set points 0
end

on click
 add points 10
 alert("Points: 10")
end
"""

result = compile_script(code)
```

### Créer un Jeu Simple
```python
code = """
page Game
-text timer
--value "Temps: 30"

-button clickZone
--text "CLIQUEZ!"
--size 200 200

on start
 set time 30
 set score 0
end

on click
 add score 100
 subtract time 1
 if time == 0
  alert("Game Over! Score: 100")
  connect.goto(GamePage)
 end
end

on tick
 subtract time 1
end
"""

result = compile_script(code)
```

## 🔧 Propriétés Disponibles

### Positions et Tailles
```
--position X Y          # X: 0-600, Y: 0-800
--size WIDTH HEIGHT     # En pixels
--corner RADIUS         # Arrondi des coins (0-50)
```

### Couleurs
```
--color blue            # Nom standard
--color #3498db        # Hexadécimal
--color rgb(52,152,219) # RGB
```

### Texte
```
--value "Texte"        # Pour texte/image
--text "Bouton"        # Pour boutons
--fontsize 24          # Taille police
```

### Média
```
--source "image.png"   # URL d'image
```

## 🎬 Événements Disponibles

| Événement | Quand | Exemple |
|-----------|-------|---------|
| `on start` | Au démarrage | Initialiser variables |
| `on click` | Au clic bouton | Gérer interaction |
| `on tick` | Chaque frame | Mise à jour gameplay |
| `on load` | Au chargement page | Préparer page |

## ✏️ Actions Disponibles

| Action | Usage | Exemple |
|--------|-------|---------|
| `alert(msg)` | Afficher message | `alert("Hi!")` |
| `set var val` | Définir variable | `set score 0` |
| `add var val` | Ajouter valeur | `add score 10` |
| `subtract var val` | Retirer valeur | `subtract health 5` |
| `connect.goto(page)` | Naviguer | `connect.goto(Menu)` |
| `if condition` | Condition | `if score > 100` |

## 🐛 Dépannage

### Erreur: "Variable non définie"
```
❌ set foo 10       # foo n'existe pas
✅ set foo 0
   add foo 10       # Maintenant c'existe
```

### Erreur: "Guillemets manquants"
```
❌ --value Hello    # Pas de guillemets
✅ --value "Hello"  # Bon
```

### Erreur: "Page non trouvée"
```
❌ connect.goto(HomePage)      # Page n'existe pas
✅ page HomePage
   -background
   connect.goto(HomePage)     # Maintenant c'existe
```

## 📊 Ressources

| Ressource | URL |
|-----------|-----|
| Code source | `/compiler/*.py` |
| Tests | `python3 compiler/tests.py` |
| Exemples | `python3 compiler/examples.py` |
| Serveur web | `localhost:8000` |
| API HTTP | `localhost:5001` |

## ✅ Checklist pour Commencer

- [ ] Lire [README_COMPLET.md](README_COMPLET.md)
- [ ] Lancer IDE: `python3 -m http.server 8000`
- [ ] Créer une simple page
- [ ] Ajouter un bouton
- [ ] Ajouter un événement on click
- [ ] Voir le résultat
- [ ] Compiler du code Python
- [ ] Lire [compiler/LANGUAGE_GUIDE.md](compiler/LANGUAGE_GUIDE.md)
- [ ] Créer une app plus complexe

## 🚀 Commandes Utiles

```bash
# Lancer IDE
python3 -m http.server 8000

# Lancer API
python3 compiler/api_server.py 5001

# Exécuter tests
python3 compiler/tests.py

# Voir exemples
python3 compiler/examples.py

# Quick start
python3 QUICK_START.py

# Test simple
python3 test_compiler.py
```

## 💡 Trucs & Astuces

1. **Nombrez vos pages et boutons:**
   ```
   page HomePage
   -button startGame
   -button aboutBtn
   ```

2. **Utilisez des noms explicites:**
   ```
   set playerScore 0   # Bon
   set x 0            # Peu clair
   ```

3. **Testez chaque page:**
   - Testez navigation
   - Testez tous les clics
   - Vérifiez la console

4. **Utilisez les commentaires:**
   ```
   -- Ceci est un commentaire
   page Home
   -- Page d'accueil
   ```

5. **Organisez le code:**
   - Une page = une vue
   - Un script = une logique
   - Des variables = état

## 🎓 Exemples Avancés

Voir [compiler/examples.py](compiler/examples.py) pour:
- Application simple
- Événements avancés
- Navigation multi-pages
- Détection d'erreurs
- Jeu complet

## 📞 Besoin d'Aide?

1. **Erreur de compilation?** → Consultez LANGUAGE_GUIDE.md
2. **Comment utiliser?** → Consultez IDE_USER_GUIDE.md
3. **Code ne marche pas?** → Regardez console (errors)
4. **Architecture?** → Consultez ARCHITECTURE.md
5. **API?** → Consultez INDEX.md

---

**Prêt à créer? Lancez le serveur et commencez! 🚀**

```bash
python3 -m http.server 8000
```

**http://localhost:8000** 🎉
