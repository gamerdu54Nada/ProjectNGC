# 🚀 ConnectScript - Compilateur Professionnel

Architecture de compilation complète pour le langage ConnectScript avec système d'événements robuste et génération de code sûr.

## 📋 Vue d'ensemble

ConnectScript est un **DSL (Domain Specific Language)** pour créer des applications visuelles interactives sans code dangereux (`eval()`).

### Architecture de Compilation

```
┌─────────────────────┐
│   Code Source       │  files: .psx (pages), .psc (scripts)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   TOKENIZER         │  Découpe en tokens
│ tokenizer.py        │  - Reconnaissance de patterns
└──────────┬──────────┘  - Gestion d'erreurs de caractères
           │
           ▼
┌─────────────────────┐
│   PARSER            │  Crée l'AST
│ parser.py           │  - Analyse syntaxique
└──────────┬──────────┘  - Validation structurelle
           │
           ▼
┌─────────────────────┐
│   VALIDATOR         │  Vérifie la sémantique
│ errors.py           │  - Références valides
└──────────┬──────────┘  - Types correctes
           │
           ▼
┌─────────────────────┐
│   CODE GENERATOR    │  Produit du JavaScript sûr
│ codegen.py          │  - Pas d'eval()
└──────────┬──────────┘  - Optimisé
           │
           ▼
┌─────────────────────┐
│   JavaScript Output │  Code exécutable
│   (typé, sûr)       │  - Pas de pollution globale
└─────────────────────┘  - 100% interprétable
```

## 📁 Structure des Fichiers

```
compiler/
├── tokenizer.py           # Tokenisation lexicale
├── ast_nodes.py          # Structure AST
├── parser.py             # Analyse syntaxique
├── errors.py             # Gestion d'erreurs
├── codegen.py            # Générateur de code
├── event_system.py       # Système d'événements
├── compile.py            # Point d'entrée
├── LANGUAGE_GUIDE.md     # Guide du langage
└── ARCHITECTURE.md       # Ce fichier
```

## 🔧 Composants Détaillés

### 1. Tokenizer (`tokenizer.py`)

**Responsabilité:** Convertir le texte en tokens

```python
from tokenizer import Tokenizer

code = "page Home\n-background\n--color blue"
tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()
# → [Token(PAGE, 'page', 1, 1), Token(IDENTIFIER, 'Home', 1, 6), ...]
```

**TokenTypes supportés:**
- Keywords: `PAGE`, `ON`, `END`, `IF`, etc.
- Délimiteurs: `MINUS`, `DOUBLE_MINUS`, `LPAREN`, `RPAREN`
- Littéraux: `STRING`, `NUMBER`, `COLOR`, `IDENTIFIER`
- Spéciaux: `NEWLINE`, `EOF`

### 2. AST Nodes (`ast_nodes.py`)

**Responsabilité:** Représenter le code sous forme d'arbre

```python
@dataclass
class Project:
    pages: Dict[str, Page]    # Pages définies
    scripts: Dict[str, Script]  # Scripts définis

@dataclass
class Page:
    name: str
    background_color: str
    elements: List[UIElement]  # Buttons, texts, images

@dataclass
class Script:
    name: str
    event_handlers: List[EventHandler]

@dataclass
class EventHandler:
    event_type: EventType  # click, start, load, tick
    actions: List[Action]
```

### 3. Parser (`parser.py`)

**Responsabilité:** Créer l'AST à partir des tokens

```python
from parser import parse_connect_script

code = "..."
project, error_manager = parse_connect_script(code)

if error_manager.has_errors():
    print(error_manager.report())  # Rapport détaillé
else:
    # Utiliser project
    for page in project.pages.values():
        print(f"Page: {page.name}")
```

**Récursion descendante (Recursive Descent Parser):**
```
parse() 
  ├── _parse_page()
  │   ├── _parse_background()
  │   └── _parse_ui_element()
  │       └── Propriétés
  └── _parse_event_handler()
      └── _parse_action()
          ├── _parse_alert()
          ├── _parse_set()
          ├── _parse_add()
          ├── _parse_subtract()
          ├── _parse_goto()
          └── _parse_if()
```

### 4. Error Management (`errors.py`)

**Responsabilité:** Collecter et rapporter les erreurs

```python
from errors import CompileErrorManager, ErrorLevel

error_manager = CompileErrorManager(source_code)

# Ajouter erreur
error_manager.add_error(
    message="Type d'événement inconnu",
    line=5,
    column=12,
    suggestion="Utilisez: click, start, load, tick"
)

# Rapport
print(error_manager.report())
```

**Exemple de rapport:**
```
ERROR] Ligne 5, Colonne 12: Type d'événement inconnu
  on unknown
     ^
  Suggestion: Utilisez: click, start, load, tick
```

### 5. Code Generator (`codegen.py`)

**Responsabilité:** Générer du JavaScript sûr

```python
from codegen import compile_project

# Compile l'AST en JavaScript
js_code = compile_project(project, error_manager)

# Résultat: JavaScript pur, sans eval()
# - Variables dans l'objet global ConnectApp
# - Pas de pollution du scope global
# - Facilement testable
```

**Sécurité:**
- ✅ Pas d'eval()
- ✅ Pas d'accès au DOM direct
- ✅ Variables locales
- ✅ Code traçable

### 6. Event System (`event_system.py`)

**Responsabilité:** Bus d'événements robuste

```python
from event_system import EventBus, EventType, create_event

# Créer le bus
event_bus = EventBus()

# S'abonner
def on_click(event):
    print(f"Clicked: {event.source}")

unsubscribe = event_bus.on(EventType.CLICK, on_click)

# Émettre
event = create_event(EventType.CLICK, "button1", {"x": 100})
event_bus.emit(event)

# Désabonner
unsubscribe()

# Historique
events = event_bus.get_events_of_type(EventType.CLICK)
```

**Pattern utilisé:** Event Bus pattern (Observer pattern)
- Découplage complet entre composants
- Historique d'événements
- Subscriptions/Unsubscriptions
- Type-safe

## 🎯 Workflow Complet

```python
from compile import ConnectScriptCompiler

# Initialiser
compiler = ConnectScriptCompiler()

# Compiler
result = compiler.compile(source_code)

# Vérifier résultat
if result['success']:
    print(result['code'])  # JavaScript généré
    print(result['ast'])   # Structure du projet
else:
    print(result['errors'])  # Erreurs trouvées
    print(result['warnings'])  # Avertissements
```

## 📊 Exemple de Pipeline

**Entrée:**
```connectscript
page Home
-button playBtn
--text "Play"
--script startGame

on click
 alert("Starting!")
 set score 0
 connect.goto(Home)
end
```

**Tokens générés:**
```
Token(PAGE, 'page', 1, 1)
Token(IDENTIFIER, 'Home', 1, 6)
Token(NEWLINE, '\n', 1, 10)
Token(MINUS, '-', 2, 1)
Token(IDENTIFIER, 'button', 2, 2)
...
```

**AST produit:**
```
Project(
  pages={
    'Home': Page(
      name='Home',
      elements=[
        UIElement(
          element_type='button',
          name='playBtn',
          properties={
            'text': 'Play',
            'script': 'startGame'
          }
        )
      ]
    )
  },
  scripts={
    'startGame': Script(
      event_handlers=[
        EventHandler(
          event_type=EventType.CLICK,
          actions=[...]
        )
      ]
    )
  }
)
```

**Code JavaScript généré:**
```javascript
const ConnectApp = {
  variables: {},
  pages: {
    'Home': {
      name: 'Home',
      elements: [
        {
          type: 'button',
          name: 'playBtn',
          properties: { text: 'Play', script: 'startGame' }
        }
      ]
    }
  },
  events: {
    'startGame': {
      onClick: async () => {
        window.alert('Starting!');
        this.variables['score'] = 0;
        await this.showPage('Home');
      }
    }
  },
  // ... autres méthodes
};
```

## 💡 Conseils Professionnels

### 1. Extensibilité

Pour ajouter une nouvelle fonctionnalité:

1. **Ajouter le TokenType** dans `tokenizer.py`
2. **Ajouter le parse method** dans `parser.py`
3. **Ajouter le code gen** dans `codegen.py`

```python
# Exemple: Ajouter un événement "onResize"
class EventType(Enum):
    RESIZE = "resize"  # Nouveau!
```

### 2. Performance

- **Tokenizer:** O(n) - Une seule passe
- **Parser:** O(n) - Recursive descent
- **Code Gen:** O(n) - Génération linéaire
- **Total:** O(n) - Complexité linéaire

### 3. Debugging

```python
# Activer les logs détaillés
parser = Parser(tokens, source_code, debug=True)

# Obtenir le rapport d'erreurs
report = error_manager.report()
print(report)
```

### 4. Testing

```python
# Test unitaire simple
def test_parse_page():
    code = "page Test\n-background\n--color blue"
    project, errors = parse_connect_script(code)
    
    assert len(project.pages) == 1
    assert project.pages['Test'].background_color == 'blue'
    assert not errors.has_errors()
```

### 5. Optimisations Futures

- [ ] Minification du code généré
- [ ] Tree-shaking (remove unused pages/scripts)
- [ ] Caching des tokens/AST
- [ ] Compilation incrémentale
- [ ] Source maps pour debugging
- [ ] Hot reload en dev

## 🚨 Gestion des Erreurs

### Format d'erreur

```
[ERROR] Ligne 5, Colonne 12: Message d'erreur
  on invalid_event
     ^
  Suggestion: Utilisez: click, start, load, tick
```

### Niveaux d'erreur

| Niveau | Impact | Exemple |
|--------|--------|---------|
| `ERROR` | Compilation échoue | Syntax error, Unknown page |
| `WARNING` | Avertissement | Unused variable, Typo détecté |
| `INFO` | Information | File compiled successfully |

## 📚 Ressources

- [LANGUAGE_GUIDE.md](./LANGUAGE_GUIDE.md) - Guide complet du langage
- [Code Source](.) - Tous les fichiers source
- Exemples dans `compile.py`

## 🎓 Concepts de Compilation

Ce compilateur démontre:
- ✅ **Analyse lexicale** (Tokenizer)
- ✅ **Analyse syntaxique** (Parser - Recursive Descent)
- ✅ **Analyse sémantique** (Validator)
- ✅ **Génération de code** (Code Generator)
- ✅ **Gestion d'erreurs** (Error Manager)
- ✅ **Système d'événements** (Event Bus)

**Inspiré par:**
- TypeScript
- Rust
- Go
- Python AST

---

**Niveau:** Avancé  
**Audience:** Développeurs intéressés par la compilation  
**Difficulté:** Intermédiaire à Avancé
