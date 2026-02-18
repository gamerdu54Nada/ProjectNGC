# ⚙️ SETUP - Configuration ConnectScript

## 📋 Prérequis

### Système
- **OS**: Linux, macOS, ou Windows
- **Python**: 3.7 ou plus récent

### Vérifier Python
```bash
python3 --version
```

Vous devriez voir: `Python 3.x.x`

---

## 🚀 Installation

### Étape 1: Cloner/Télécharger
```bash
# Clone repository
git clone <repo-url>
cd codespaces-blank

# OU télécharger les fichiers
# et naviguer vers le répertoire
```

### Étape 2: Vérifier la Structure
```bash
ls -la
# Vous devriez voir:
# - index.html
# - app.js, styles.css, parser.js, runtime.js
# - compiler/ (répertoire)
```

### Étape 3: Tester le Compilateur
```bash
cd compiler
python3 __init__.py
# Ou essayez:
python3 -c "from . import compile_script; print('✓ OK')"
```

---

## 🎮 Lancer l'IDE Web

### Option A: Port 8000 (Défaut)
```bash
python3 -m http.server 8000
```

### Option B: Autre Port
```bash
python3 -m http.server 3000
```

### Ouvrir
- **Navigateur**: `http://localhost:8000`
- **Ou**: `http://localhost:3000` (si port 3000)

---

## 🌐 Lancer l'API HTTP

### Démarrer le Serveur
```bash
python3 compiler/api_server.py 5001
```

### Pour utiliser autre port:
```bash
python3 compiler/api_server.py 9000
```

### Tester l'API
```bash
curl -X GET http://localhost:5001/api/status
```

Vous devriez voir:
```json
{
  "status": "online",
  "service": "ConnectScript Compiler API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

## 🧪 Exécuter les Tests

### Tous les Tests
```bash
python3 compiler/tests.py
```

**Résultat attendu**: 10/10 tests passent (ou très proche)

### Tests Spécifiques
```bash
# Juste voir les exemples
python3 compiler/examples.py

# Test simple
python3 test_compiler.py

# Quick start
python3 QUICK_START.py
```

---

## 📚 Vérifier la Documentation

### Fichiers Importants
```bash
# Vue d'ensemble
cat GET_STARTED.md           # Vous êtes ici!

# Guides spécifiques
cat QUICK_REFERENCE.md       # Synthétique
cat IDE_USER_GUIDE.md        # Pour l'IDE
cat compiler/LANGUAGE_GUIDE.md # Syntaxe

# Navigation
cat INDEX.md                 # Où aller?
cat FILES.md                 # Tous les fichiers
```

---

## 💻 Utiliser le Compilateur en Python

### Importer
```python
from compiler import compile_script
```

### Compiler
```python
code = "page Home\n-button btn\n--text Click"
result = compile_script(code)
print(result['javascript'])
```

### Structure du Retour
```python
result = {
    'success': True/False,
    'javascript': "...",    # Code généré
    'ast': {...},          # Structure du code
    'errors': [...],       # Messages erreur
    'warnings': [...]      # Avertissements
}
```

---

## 🔌 Utiliser l'API HTTP

### Avec curl
```bash
curl -X POST http://localhost:5001/api/compile \
  -H "Content-Type: application/json" \
  -d '{
    "code": "page Home\n-button btn\n--text Click"
  }'
```

### Avec Python
```python
import http.client
import json

conn = http.client.HTTPConnection("localhost", 5001)

payload = json.dumps({"code": "page Home"})
headers = {"Content-Type": "application/json"}

conn.request("POST", "/api/compile", payload, headers)
response = conn.getresponse()
data = json.loads(response.read().decode())

conn.close()
```

### Avec JavaScript/Fetch
```javascript
fetch('http://localhost:5001/api/compile', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({code: 'page Home'})
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## ⚙️ Configuration Avancée

### Dossiers Importants

```
codespaces-blank/
├── compiler/               # Code compilateur
│   ├── *.py               # Modules Python
│   ├── *.md               # Docs compilateur
│   └── tests.py           # Suite tests
├── index.html             # IDE interface
├── *.js, *.css            # Frontend
└── *.md                   # Docs racine
```

### Fichiers Modifiables

**Ne modifiez PAS (ce sont les modules clés):**
- `compiler/tokenizer.py`
- `compiler/parser.py`
- `compiler/compile.py`

**Modifiables:**
- `index.html` - Personnaliser l'interface
- `styles.css` - Changer les couleurs
- Documentation - Corriger/améliorer

---

## 🔧 Dépannage

### "Port déjà en utilisation"
```bash
# Trouvez le processus
lsof -i :8000

# Utilisez autre port
python3 -m http.server 9000
```

### "Erreur d'importation: compiler"
```bash
# Vérifiez que vous êtes dans le bon répertoire
pwd                  # Devrait être .../codespaces-blank
ls compiler/         # Devrait afficher les fichiers .py

# Relancez
python3 -c "from compiler import compile_script"
```

### "Cannot compile: X"
```bash
# Vérifiez la syntaxe
# Consultez: QUICK_REFERENCE.md ou compiler/LANGUAGE_GUIDE.md
```

### "Syntaxe erreur: Unexpected character"
```bash
# C'est normal! Regardez dans la console
# Elle vous montre ligne et colonne exacte
# Consultez compiler/LANGUAGE_GUIDE.md#dépannage
```

---

## 📊 Vérifier l'Installation

### Checklist
```bash
# 1. Structure fichiers
ls -la | grep -E "index|app.js|compiler"

# 2. Python 3
python3 --version

# 3. Compilateur importable
python3 -c "from compiler import compile_script; print('✓')"

# 4. Tests exécutables
python3 compiler/tests.py 2>&1 | head -20

# 5. API démarrable
timeout 2 python3 compiler/api_server.py 5001 2>&1 | head -5

# 6. IDE accessible
curl http://localhost:8000 2>&1 | head -20
```

---

## 🎯 Configuration Par Cas d'Usage

### Pour le Développement Web (IDE)
```bash
# Démarrer IDE
python3 -m http.server 8000

# Ouvrir http://localhost:8000
# Cliquez "New Page" et commencez!
```

### Pour l'Intégration Python
```bash
# Dans votre code:
from compiler import compile_script
result = compile_script("""
page Home
-button btn
--text Click
""")
```

### Pour l'API REST
```bash
# Démarrer serveur
python3 compiler/api_server.py 5001

# POST http://localhost:5001/api/compile
```

### Pour les Tests
```bash
# Exécuter tous les tests
python3 compiler/tests.py

# Voir les exemples
python3 compiler/examples.py
```

---

## 📚 Ressources

| Besoin | Fichier |
|--------|---------|
| Guide rapide | GET_STARTED.md (ce fichier!) |
| Syntaxe | QUICK_REFERENCE.md |
| IDE | IDE_USER_GUIDE.md |
| Langage | compiler/LANGUAGE_GUIDE.md |
| Architecture | compiler/ARCHITECTURE.md |
| Navigation | INDEX.md |
| Tous fichiers | FILES.md |

---

## ✅ Configuration Rapide

```bash
# 1. Vérifier Python
python3 --version

# 2. Tester compilateur
python3 -c "from compiler import compile_script; print('✓')"

# 3. Lancer IDE
python3 -m http.server 8000

# 4. Ouvrir http://localhost:8000

# 5. Créer première page!
```

---

## 🎉 Bravo!

Vous êtes maintenant configuré pour utiliser ConnectScript! 🚀

**Prochaines étapes:**
1. Consultez [GET_STARTED.md](GET_STARTED.md)
2. Créez votre première application
3. Explorez la documentation
4. Amusez-vous! 🎨

---

**Questions? Voir [INDEX.md](INDEX.md)**
