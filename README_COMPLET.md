# 🎨 ConnectScript IDE & Compiler

Un environnement intégré complet pour créer et compiler votre propre langage de programmation visuelle: **ConnectScript**

## 🎯 Qu'est-ce que c'est?

ConnectScript est une plateforme qui vous permet de:

1. **Concevoir** une interface utilisateur visuelle (pages, boutons, textes, images)
2. **Programmer** des événements et des actions sans code traditionnel
3. **Exécuter** vos créations dans un environnement runtime sécurisé
4. **Compiler** vers du JavaScript standard pour une portabilité maximale

## 📁 Structure du Projet

```
codespaces-blank/
├── 🖥️  Frontend (IDE Web)
│   ├── index.html          # Interface utilisateur (Roblox Studio-like)
│   ├── app.js              # Logique Vue.js
│   ├── styles.css          # Styles CSS
│   ├── parser.js           # Parser JavaScript simple
│   └── runtime.js          # Runtime JavaScript simple
│
├── 🔧 Compilateur (Backend Python)
│   ├── compiler/
│   │   ├── tokenizer.py    # Analyse lexicale (tokenization)
│   │   ├── parser.py       # Analyse syntaxique (parsing)
│   │   ├── ast_nodes.py    # Structures de données AST
│   │   ├── codegen.py      # Génération de code JavaScript
│   │   ├── errors.py       # Gestion des erreurs avancée
│   │   ├── event_system.py # Système d'événements robuste
│   │   ├── compile.py      # Orchestration de la compilation
│   │   ├── tests.py        # Suite de tests (10 tests)
│   │   ├── examples.py     # 5 exemples complets
│   │   ├── api_server.py   # Serveur API HTTP
│   │   ├── __init__.py     # Package initialization
│   │   │
│   │   └── 📚 Documentation
│   │       ├── README.md           # Vue d'ensemble du compilateur
│   │       ├── LANGUAGE_GUIDE.md   # Guide complet du langage
│   │       ├── ARCHITECTURE.md     # Documentation technique
│   │       ├── INDEX.md            # Index et références
│   │       └── RECAP.md            # Récapitulatif complet
│   │
│   ├── 🚀 Utilisation
│   ├── QUICK_START.py      # Exemples de démarrage rapide
│   └── test_compiler.py    # Test simple du compilateur
│
└── 📖 Documentation
    └── README_COMPLET.md (ce fichier)
```

## 🚀 Démarrage Rapide

### Option 1: Utiliser l'IDE Web

1. **Démarrez le serveur web:**
```bash
python3 -m http.server 8000
```

2. **Ouvrez dans votre navigateur:**
```
http://localhost:8000
```

3. **Créez votre première application:**
   - Cliquez sur "➕ New Page" pour créer une page
   - Ajoutez des éléments (boutons, textes)
   - Créez un script pour gérer les événements
   - Le code est compilé en temps réel

### Option 2: Compiler depuis Python

```python
from compiler import compile_script

code = """
page Home
-button btn
--text "Click me"
--color green

on click
 alert("Vous avez cliqué!")
end
"""

result = compile_script(code)
if result['success']:
    print(result['javascript'])  # Code JavaScript généré
    print(result['ast'])         # Structure de l'arbre syntaxique
else:
    print(result['errors'])      # Messages d'erreur
```

### Option 3: API HTTP

1. **Démarrez le serveur API:**
```bash
python3 compiler/api_server.py 5001
```

2. **Compilez via POST:**
```bash
curl -X POST http://localhost:5001/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code":"page Home\n-button btn\n--text Click"}'
```

## 🎮 Exemple Simple

Créez un simple compteur cliquable:

```connectscript
page Counter
-background
--color #1a1a2e

-text display
--value "Compteur: 0"
--color #00ff00
--position 50 50
--fontsize 32

-button clickBtn
--text "Incrémenter"
--color #00ff00
--position 150 200
--size 200 60
--corner 8
--fontsize 20
--script increaseCounter

on start
 set count 0
 alert("Compteur démarré!")
end

on click
 add count 1
 alert("Appuis: " count)
end
```

## 📚 Documentation Complète

### Pour les Utilisateurs
- **[compiler/LANGUAGE_GUIDE.md](compiler/LANGUAGE_GUIDE.md)** - Apprenez la syntaxe ConnectScript
- **[QUICK_START.py](QUICK_START.py)** - 3 façons différentes d'utiliser le compilateur

### Pour les Développeurs
- **[compiler/README.md](compiler/README.md)** - Architecture du compilateur
- **[compiler/ARCHITECTURE.md](compiler/ARCHITECTURE.md)** - Détails techniques approfondis
- **[compiler/INDEX.md](compiler/INDEX.md)** - Référence complète des API
- **[compiler/RECAP.md](compiler/RECAP.md)** - Résumé du projet

### Pour Tester
```bash
python3 compiler/tests.py        # Exécuter 10 tests
python3 compiler/examples.py     # Voir 5 exemples complets
python3 test_compiler.py         # Test simple
python3 QUICK_START.py           # Exemples d'utilisation
```

## 🔑 Caractéristiques Principales

### ✅ Compilateur Professionnel
- **Architecture propre**: Tokenizer → Parser → AST → CodeGenerator
- **Zéro eval()**: Sécurité maximale, code généré explicitement
- **Gestion d'erreurs avancée**: Contextuelle avec suggestions
- **Performance**: Complexity O(n) garantie
- **Sans dépendances externes**: Pur Python 3

### ✅ Système d'Événements Robuste
- **Événements supportés**: click, start, load, tick
- **Pattern Observer**: Découplage maximum
- **Histoire des événements**: Traçabilité complète
- **Contexte dynamique**: Gestion des variables par événement

### ✅ Interface IDE Professionnelle
- **Roblox Studio-like**: Layout familier et intuitif
- **Explorer multi-panels**: Pages et Scripts organisés
- **Éditeur multi-fichiers**: Travailler sur plusieurs fichiers
- **Prévisualisation en temps réel**: Voir les changements immédiatement
- **Console de débogage**: Voir les erreurs et logs

## 🛠️ Briques de Base

### Pages
```connectscript
page PageName
-background
--color blue
```

### Éléments UI
```connectscript
-button myButton
--text "Click me"
--color green
--position 100 200
--size 150 50
--corner 8
```

### Événements & Actions
```connectscript
on click
 alert("Message")
 set variable value
 add counter 5
 subtract counter 3
 connect.goto(OtherPage)
 if condition
  alert("Condition vraie")
 end
end
```

## 💻 Architecture Technique

Le compilateur fonctionne en 5 étapes:

1. **Tokenizer** (tokenizer.py)
   - Convertit le texte en tokens
   - Reconnaît: keywords, identifiers, strings, numbers, colors, comments

2. **Parser** (parser.py)
   - Construit une structure d'arbre (AST)
   - Valide la syntaxe
   - Intègre la gestion des erreurs

3. **AST** (ast_nodes.py)
   - Représentation structure du programme
   - Types sûrs (dataclasses)
   - Méthodes de validation

4. **Code Generator** (codegen.py)
   - Traduit AST en JavaScript
   - Génère objet ConnectApp
   - Zéro eval, code explicite

5. **Event System** (event_system.py)
   - Bus d'événements centralisé
   - Gestion des variables
   - Navigation entre pages

## 📊 Statistiques du Projet

- **Code Python**: ~2800 lignes
- **Documentation**: ~1500 lignes
- **Tests**: 10 cas complets
- **Exemples**: 5 applications démonstration
- **Fichiers compilateur**: 8 modules
- **API Endpoints**: 3 (compile, status, version)

## 🎓 Cas d'Usage

ConnectScript est parfait pour:

1. **Éducation**: Apprendre à créer des DSLs
2. **Prototypage rapide**: Développer rapidement des interfaces
3. **Jeux simples**: Créer des mini-jeux cliquables
4. **Applications interactives**: Prototypes d'UX
5. **Démonstrations**: Montrer des concepts rapidement

## 🔐 Sécurité

- **Pas de eval()**: Le code généré est du JavaScript standard
- **Tokens validés**: Chaque token est vérifiée
- **Parser strict**: Syntaxe rigoureusement validée
- **Error handling**: Messages d'erreur clairs et utiles
- **Sandboxisé**: L'exécution est isolée

## 🚀 Prochaines Étapes

1. **Exécuter les tests**:
   ```bash
   python3 compiler/tests.py
   ```

2. **Voir les exemples**:
   ```bash
   python3 compiler/examples.py
   ```

3. **Lire la documentation**:
   - Commencez par [compiler/LANGUAGE_GUIDE.md](compiler/LANGUAGE_GUIDE.md)
   - Explorez [compiler/ARCHITECTURE.md](compiler/ARCHITECTURE.md)

4. **Utiliser l'IDE**:
   - Lancez le serveur web
   - Créez vos premières applications

5. **Intégrer dans vos projets**:
   ```python
   from compiler import compile_script
   result = compile_script(your_code)
   ```

## 📝 Licence

Ce projet est fourni à titre d'exemple éducatif.

## 🤝 Support

Pour plus d'informations:
- Consultez la documentation du compilateur
- Voyez les exemples fournis
- Lisez le récapitulatif du projet

---

**Créé avec ❤️ pour les développeurs qui aiment créer des langages!**

Happy Coding! 🚀
