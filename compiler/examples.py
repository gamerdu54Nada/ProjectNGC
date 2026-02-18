#!/usr/bin/env python3
"""
ConnectScript Compiler Usage Example
Exemple d'utilisation du compilateur
"""

from compiler import compile_script
import json


def example_1_simple():
    """Exemple 1: Application simple"""
    print("\n" + "="*70)
    print("📌 EXEMPLE 1: Application Simple")
    print("="*70 + "\n")
    
    code = """
page Home
-background
--color lightblue

-text greeting
--value "Bonjour ConnectScript!"
--color darkblue
--position 50 50
--fontsize 28

-button playBtn
--text "Commencer"
--color green
--position 100 200
--size 150 50
--corner 8
--fontsize 18
"""
    
    result = compile_script(code)
    
    print("✅ Compilation réussie!")
    print(f"\n📊 AST généré:")
    print(json.dumps(result['ast'], indent=2, ensure_ascii=False))
    
    print(f"\n💻 JavaScript généré (~{len(result['javascript'])} caractères):")
    print(result['javascript'][:300] + "...\n")


def example_2_events():
    """Exemple 2: Événements et variables"""
    print("\n" + "="*70)
    print("📌 EXEMPLE 2: Événements et Variables")
    print("="*70 + "\n")
    
    code = """
page Game
-text scoreDisplay
--value "Score: 0"
--color white
--position 20 20
--fontsize 24

-button collectBtn
--text "Collecter"
--color green
--position 100 200
--size 150 50
--script collectItem

on start
 set score 0
 set itemsCollected 0
 alert("Jeu commencé!")
end

on click
 add score 10
 add itemsCollected 1
 alert("Item collecté!")
end

on tick
 subtract timer 1
end
"""
    
    result = compile_script(code)
    
    if result['success']:
        print("✅ Compilation réussie!")
        
        scripts = result['ast'].get('scripts', {})
        print(f"\n📜 Scripts trouvés: {len(scripts)}")
        
        for script_name, script_data in scripts.items():
            print(f"\n  Script: {script_name}")
            handlers = script_data.get('eventHandlers', [])
            for handler in handlers:
                print(f"    - Événement: {handler['event']}")
                for action in handler['actions']:
                    print(f"      - Action: {action['type']} {action['params']}")
    else:
        print("❌ Erreurs trouvées:")
        for error in result['errors']:
            print(f"  - {error}")


def example_3_multiple_pages():
    """Exemple 3: Navigation entre pages"""
    print("\n" + "="*70)
    print("📌 EXEMPLE 3: Navigation entre Pages")
    print("="*70 + "\n")
    
    code = """
page MainMenu
-background
--color #2c3e50

-text title
--value "Mon Jeu"
--color white
--position 50 50
--fontsize 36

-button startBtn
--text "Jouer"
--color green
--position 100 200
--size 150 50
--script startGame

page GameScreen
-background
--color #3498db

-text levelDisplay
--value "Niveau 1"
--color white
--position 20 20
--fontsize 24

-button menuBtn
--text "Menu"
--color red
--position 20 500
--size 150 50
--script backToMenu

page GameOver
-background
--color #e74c3c

-text endMsg
--value "Game Over!"
--color white
--position 50 50
--fontsize 32

-button retryBtn
--text "Rejouer"
--color green
--position 100 200
--size 150 50
--script restartGame

on click
 set level 1
 connect.goto(GameScreen)
end

on click
 connect.goto(MainMenu)
end

on click
 connect.goto(MainMenu)
end
"""
    
    result = compile_script(code)
    
    if result['success']:
        print("✅ Compilation réussie!")
        
        pages = result['ast']['pages']
        print(f"\n📄 Pages trouvées: {len(pages)}")
        
        for page_name, page_data in pages.items():
            elements = page_data['elements']
            print(f"\n  Page: {page_name}")
            print(f"    - Background: {page_data['backgroundColor']}")
            print(f"    - Éléments: {len(elements)}")
            for elem in elements:
                props = elem['properties']
                print(f"      · {elem['type']}: {elem['name']} ({props.get('text', props.get('value', ''))})")


def example_4_error_detection():
    """Exemple 4: Détection d'erreurs"""
    print("\n" + "="*70)
    print("📌 EXEMPLE 4: Détection d'Erreurs")
    print("="*70 + "\n")
    
    code = """
page Home
-button btn
--text "Click"  # OK
--color green

page GamePage  # Existe
-text display

on click
 alert("Button clicked!")
 connect.goto(GamePage)  # Cette page existe
 add score 10
end
"""
    
    result = compile_script(code)
    
    if result['success']:
        print("✅ Aucune erreur trouvée!")
        print(f"   Pages: {list(result['ast']['pages'].keys())}")
        print(f"   Scripts: {list(result['ast']['scripts'].keys())}")
    else:
        print("❌ Erreurs:")
        for error in result['errors']:
            print(f"  {error}")
    
    # Exemple avec erreur
    print("\n" + "-"*70)
    print("Test avec erreur intentionnelle:\n")
    
    code_with_error = """
page Home
-button btn
--text Click  # ERREUR: Pas de guillemets!
"""
    
    result = compile_script(code_with_error)
    
    if result['success']:
        print("✅ OK")
    else:
        print("❌ Erreurs détectées:")
        for error in result['errors']:
            print(f"  {error}")


def example_5_full_game():
    """Exemple 5: Jeu complet"""
    print("\n" + "="*70)
    print("📌 EXEMPLE 5: Jeu Complet avec Score")
    print("="*70 + "\n")
    
    code = """
page MainMenu
-background
--color #1a1a2e

-text gameTitle
--value "CLICK CLICKER"
--color #00ff00
--position 100 50
--fontsize 48

-text description
--value "Cliquez autant que possible!"
--color #00ff00
--position 100 120
--fontsize 16

-button playBtn
--text "JOUER"
--color #00ff00
--position 150 250
--size 180 60
--corner 10
--fontsize 24
--script startGame

page GameLevel
-background
--color #16213e

-text scoreLabel
--value "Score: 0"
--color #00ff00
--position 20 20
--fontsize 32

-text timerLabel
--value "Temps: 30"
--color #ff0000
--position 400 20
--fontsize 32

-text clicksLabel
--value "Clics: 0"
--color #00ff00
--position 200 100
--fontsize 24

-button clickZone
--text "CLIQUEZ!"
--color #00ff00
--position 200 300
--size 200 100
--corner 5
--fontsize 32
--script playerClick

-button menuBtn
--text "Menu"
--color #666666
--position 20 500
--size 100 40
--corner 5
--fontsize 14
--script backToMenu

page HighScore
-background
--color #0f3460

-text finalScore
--value "Score Final: 0"
--color #ffd700
--position 150 50
--fontsize 36

-text rank
--value "Excellent!"
--color #00ff00
--position 150 150
--fontsize 28

-button playAgainBtn
--text "Rejouer"
--color #00ff00
--position 150 350
--size 150 60
--corner 8
--fontsize 20
--script playAgain

on start
 set score 0
 set timer 30
 set clicks 0
 alert("Jeu commencé! Vous avez 30 secondes!")
 connect.goto(MainMenu)
end

on click
 add score 100
 add clicks 1
 subtract timer 1
 if timer == 0
  alert("Temps écoulé!")
  connect.goto(HighScore)
 end
end
"""
    
    result = compile_script(code)
    
    if result['success']:
        print("✅ Compilation réussie!")
        
        ast = result['ast']
        print(f"\n📊 Statistiques:")
        print(f"  - Pages: {len(ast['pages'])}")
        print(f"  - Scripts: {len(ast['scripts'])}")
        
        total_elements = sum(len(p['elements']) for p in ast['pages'].values())
        print(f"  - Éléments UI: {total_elements}")
        
        print(f"\n💾 Taille du code généré: {len(result['javascript'])} caractères")
        
        print(f"\n⚙️  Actions trouvées:")
        for script_name, script_data in ast['scripts'].items():
            for handler in script_data['eventHandlers']:
                print(f"  - {handler['event']}: {len(handler['actions'])} action(s)")
    else:
        print("❌ Erreurs:")
        for error in result['errors']:
            print(f"  {error}")


def main():
    """Lance tous les exemples"""
    
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*15 + "🎨 CONNECTSCRIPT COMPILER EXAMPLES" + " "*19 + "║")
    print("╚" + "="*68 + "╝")
    
    examples = [
        example_1_simple,
        example_2_events,
        example_3_multiple_pages,
        example_4_error_detection,
        example_5_full_game,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Erreur dans {example_func.__name__}: {e}")
    
    print("\n" + "="*70)
    print("✅ Tous les exemples ont été exécutés!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
