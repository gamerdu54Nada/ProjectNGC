#!/usr/bin/env python3
"""
ConnectScript Compiler - Quick Start Guide
Guide de démarrage rapide du compilateur ConnectScript
"""

# ============================================================================
# OPTION 1: Usage simple depuis Python
# ============================================================================

from compiler import compile_script

code = """
page Home
-background
--color #1a1a2e

-text title
--value "Bienvenue"
--color #00ff00
--position 50 50
--fontsize 28

-button playBtn
--text "Jouer"
--color #00ff00
--position 100 200
--size 150 50
--corner 8
--fontsize 18

on start
 set score 0
 alert("Jeu commencé!")
end

on click
 add score 10
 alert("Score: 10 points!")
end
"""

result = compile_script(code)

if result['success']:
    print("✅ Compilation réussie!")
    print(f"\n📊 Code généré: {len(result['javascript'])} caractères")
    print(f"📄 Pages: {len(result['ast'].get('pages', {}))}")
    print(f"🔧 Scripts: {len(result['ast'].get('scripts', {}))}")
    
    # Utiliser le code généré
    print("\n💾 Code JavaScript généré:")
    print(result['javascript'][:500] + "...")
else:
    print("❌ Erreurs:")
    for error in result['errors']:
        print(f"  - {error}")


# ============================================================================
# OPTION 2: Usage via serveur API HTTP
# ============================================================================

import json
import http.client

def compile_via_api(code):
    """Compiler via l'API HTTP"""
    try:
        conn = http.client.HTTPConnection("localhost", 5001)
        
        payload = json.dumps({"code": code})
        headers = {"Content-Type": "application/json"}
        
        conn.request("POST", "/api/compile", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))
        
        conn.close()
        return data
    except ConnectionRefusedError:
        print("⚠️  Le serveur API n'est pas en cours d'exécution")
        print("   Lancez: python3 compiler/api_server.py")
        return None


# ============================================================================
# OPTION 3: Utilisation avancée avec composants individuels
# ============================================================================

from compiler import (
    Tokenizer, Parser, CodeGenerator,
    CompileErrorManager, compile_project
)

def compile_advanced(code):
    """Compilation avancée avec contrôle fin"""
    
    # Étape 1: Tokenization
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    print(f"📝 {len(tokens)} tokens générés")
    
    # Étape 2: Parsing
    error_manager = CompileErrorManager()
    parser = Parser(tokens, code)
    project = parser.parse()
    
    # Étape 3: Vérification des erreurs
    if parser.error_manager.has_errors():
        print("❌ Erreurs trouvées:")
        for error in parser.error_manager.get_errors():
            print(f"  {error}")
        return None
    
    # Étape 4: Génération de code
    javascript = compile_project(project, parser.error_manager)
    
    return {
        'ast': project,
        'javascript': javascript,
        'tokens': tokens
    }


# ============================================================================
# EXEMPLES DE TOUT UTILISER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎨 ConnectScript Compiler - Usage Examples")
    print("="*70 + "\n")
    
    # Exemple 1: Simple
    print("📌 Exemple 1: Utilisation Simple")
    print("-" * 70)
    simple_code = """
page Test
-button btn
--text "Click"
"""
    result = compile_script(simple_code)
    print(f"✓ Success: {result['success']}")
    
    # Exemple 2: Via API (si le serveur démarré)
    print("\n📌 Exemple 2: Via API HTTP")
    print("-" * 70)
    print("Pour utiliser l'API:")
    print("  1. Lancez le serveur: python3 compiler/api_server.py 5001")
    print("  2. Compilez le code:")
    print("  curl -X POST http://localhost:5001/api/compile \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"code\":\"page Home\"}'")
    
    # Exemple 3: Voir la documentation
    print("\n📌 Exemple 3: Documentation")
    print("-" * 70)
    print("Fichiers disponibles à consulter:")
    print("  • compiler/README.md - Vue d'ensemble")
    print("  • compiler/LANGUAGE_GUIDE.md - Guide du langage")
    print("  • compiler/ARCHITECTURE.md - Architecture technique")
    print("  • compiler/INDEX.md - Index et références")
    print("  • compiler/RECAP.md - Récapitulatif complet")
    
    print("\n" + "="*70 + "\n")
