# 🚀 GET STARTED - ConnectScript en 2 Minutes

## ⚡ Option 1: IDE Web (Le Plus Facile!)

### Étape 1: Démarrer
```bash
python3 -m http.server 8000
```

### Étape 2: Ouvrir
```
Allez à: http://localhost:8000
```

### Étape 3: Créer
- Cliquez "➕ New Page"
- Écrivez votre code
- Voir le résultat à droite!

**Exemple:**
```
page Home
-button myBtn
--text "Click me!"
--color green
--position 100 200
--size 150 50

on click
 alert("Boum!")
end
```

---

## 💻 Option 2: Compiler en Python

### Étape 1: Importer
```python
from compiler import compile_script
```

### Étape 2: Compiler
```python
code = """
page Home
-button btn
--text "Start"

on click
 alert("Clicked!")
end
"""

result = compile_script(code)
```

### Étape 3: Utiliser
```python
if result['success']:
    print(result['javascript'])  # Code généré
else:
    print(result['errors'])      # Erreurs
```

---

## 🌐 Option 3: API HTTP

### Étape 1: Démarrer serveur
```bash
python3 compiler/api_server.py 5001
```

### Étape 2: Compiler via HTTP
```bash
curl -X POST http://localhost:5001/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code":"page Home\n-button btn\n--text Click"}'
```

---

## 📚 Documentation Complète

Vous voulez en savoir plus?

| Oh! | Fais ceci |
|-----|----------|
| Je suis débutant | Lis [README_COMPLET.md](README_COMPLET.md) |
| Je veux utiliser l'IDE | Lis [IDE_USER_GUIDE.md](IDE_USER_GUIDE.md) |
| Je veux apprendre la langue | Lis [compiler/LANGUAGE_GUIDE.md](compiler/LANGUAGE_GUIDE.md) |
| Je veux une syntaxe rapide | Lis [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Je veux voir des exemples | Lance `python3 compiler/examples.py` |
| Je veux tout | Lis [INDEX.md](INDEX.md) |

---

## 💡 Exemple Complet: Mini-Jeu

```connectscript
page Game
-background
--color #2c3e50

-text scoreDisplay
--value "Score: 0"
--color white
--position 20 20
--fontsize 32

-button clickZone
--text "CLIQUEZ!"
--color green
--position 200 300
--size 200 100

on start
 set score 0
 alert("Jeu commencé!")
end

on click
 add score 10
 alert("Score: 10!")
end
```

---

## 🎯 Prochaines Étapes

1. **Lancez une option ci-dessus**
2. **Créez une simple page**
3. **Ajoutez un bouton**
4. **Ajoutez un événement on click**
5. **Voilà! 🎉**

---

## ✅ Checklist Rapide

- [ ] J'ai lu GET_STARTED.md (ce fichier!)
- [ ] J'ai choisi: IDE / Python / API
- [ ] J'ai lancé le serveur/IDE approprié
- [ ] J'ai créé une première app
- [ ] Ça marche! 🚀

---

**C'est tout pour démarrer! Amusez-vous! 🎨**

**Questions? Consultez [INDEX.md](INDEX.md)**
