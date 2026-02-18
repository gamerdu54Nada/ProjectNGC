"""
ConnectScript Compiler - Main Entry Point
"""
from tokenizer import Tokenizer
from parser import Parser
from codegen import compile_project
from event_system import create_event_bus, create_event_context
from errors import CompileErrorManager
import json


class ConnectScriptCompiler:
    """Compilateur principal ConnectScript"""
    
    def __init__(self):
        self.error_manager = None
    
    def compile(self, source_code: str) -> dict:
        """
        Compile le code ConnectScript
        
        Returns:
            {
                'success': bool,
                'code': str,          # Code JavaScript généré
                'ast': dict,         # Arbre de syntaxe
                'errors': [str],     # Erreurs trouvées
                'warnings': [str]    # Avertissements
            }
        """
        result = {
            'success': False,
            'code': '',
            'ast': {},
            'errors': [],
            'warnings': []
        }
        
        try:
            # Étape 1: Tokenization
            print("📝 Tokenizing...")
            tokenizer = Tokenizer(source_code)
            tokens = tokenizer.tokenize()
            print(f"   → {len(tokens)} tokens générés")
            
            # Étape 2: Parsing
            print("🔍 Parsing...")
            parser = Parser(tokens, source_code)
            project = parser.parse()
            self.error_manager = parser.error_manager
            
            if parser.error_manager.has_errors():
                result['errors'] = [str(e) for e in parser.error_manager.get_errors()]
                result['warnings'] = [str(e) for e in parser.error_manager.get_warnings()]
                print(f"   ✗ {len(result['errors'])} erreur(s) trouvée(s)")
                print(f"   ⚠ {len(result['warnings'])} avertissement(s)")
                return result
            
            print(f"   ✓ {len(project.pages)} page(s), {len(project.scripts)} script(s)")
            
            # Étape 3: Code Generation
            print("⚙️  Generating JavaScript...")
            js_code = compile_project(project, self.error_manager)
            print(f"   ✓ {len(js_code)} caractères générés")
            
            # Étape 4: AST Export
            ast_data = {
                'pages': {
                    name: {
                        'name': page.name,
                        'backgroundColor': page.background_color,
                        'elements': [
                            {
                                'type': elem.element_type,
                                'name': elem.name,
                                'properties': elem.properties
                            }
                            for elem in page.elements
                        ]
                    }
                    for name, page in project.pages.items()
                },
                'scripts': {
                    name: {
                        'name': script.name,
                        'eventHandlers': [
                            {
                                'event': handler.event_type.value,
                                'actions': [
                                    {
                                        'type': action.action_type,
                                        'params': action.params
                                    }
                                    for action in handler.actions
                                ]
                            }
                            for handler in script.event_handlers
                        ]
                    }
                    for name, script in project.scripts.items()
                }
            }
            
            result['success'] = True
            result['code'] = js_code
            result['ast'] = ast_data
            result['warnings'] = [str(e) for e in self.error_manager.get_warnings()]
            
            print("\n✅ Compilation réussie!\n")
            return result
        
        except Exception as e:
            result['errors'] = [str(e)]
            print(f"❌ Erreur: {e}\n")
            return result
    
    def get_error_report(self) -> str:
        """Obtient un rapport détaillé des erreurs"""
        if self.error_manager:
            return self.error_manager.report()
        return "Pas d'erreur trouvée"


# Exemple d'utilisation
if __name__ == "__main__":
    
    # Exemple simple
    example_code = """
# ===== Pages =====
page Home
-background
--color lightblue

-text greeting
--value "Hello ConnectScript!"
--color darkblue
--position 50 50
--fontsize 28

-button playBtn
--text "Play"
--color green
--position 100 150
--size 150 50
--script playHandler

page GameOver
-background
--color lightcoral

-text gameOverMsg
--value "Game Over!"
--color white
--position 50 50
--fontsize 32

-button retryBtn
--text "Retry"
--color blue
--position 100 150
--size 150 50
--script retryHandler


# ===== Scripts =====

on click
 set score 0
 alert("Game Started!")
 connect.goto(GameOver)
end

on click
 alert("Restarting...")
 connect.goto(Home)
end

on start
 set playerName "Hero"
 alert("Welcome Player!")
end
"""
    
    compiler = ConnectScriptCompiler()
    result = compiler.compile(example_code)
    
    print("="*60)
    if result['success']:
        print("🎉 Succès!")
        print("\nAST:")
        print(json.dumps(result['ast'], indent=2, ensure_ascii=False))
        print("\nCode généré (premiers 500 chars):")
        print(result['code'][:500] + "...")
    else:
        print("❌ Erreurs trouvées:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['warnings']:
        print("\n⚠️  Avertissements:")
        for warning in result['warnings']:
            print(f"  - {warning}")
