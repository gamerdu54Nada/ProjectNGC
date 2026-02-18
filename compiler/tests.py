"""
ConnectScript Compiler - Tests
Exemples et tests pour le compilateur
"""
from compile import ConnectScriptCompiler


def test_simple_page():
    """Test: Créer une page simple"""
    code = """
page Home
-background
--color lightblue
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success'], f"Erreurs: {result['errors']}"
    assert 'Home' in result['ast']['pages']
    assert result['ast']['pages']['Home']['backgroundColor'] == 'lightblue'
    print("✓ test_simple_page passed")


def test_page_with_elements():
    """Test: Page avec plusieurs éléments"""
    code = """
page GameScreen
-background
--color white

-text title
--value "Game Title"
--color darkblue
--position 50 50
--fontsize 32

-button playBtn
--text "Play"
--color green
--position 100 200
--size 150 50
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    page = result['ast']['pages']['GameScreen']
    assert len(page['elements']) == 2
    assert page['elements'][0]['type'] == 'text'
    assert page['elements'][1]['type'] == 'button'
    print("✓ test_page_with_elements passed")


def test_simple_event():
    """Test: Événement simple"""
    code = """
page Home
-button btn
--text "Click"

on click
 alert("Clicked!")
end
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    # Vérifie que le script a été créé
    scripts = result['ast']['scripts']
    assert len(scripts) > 0
    print("✓ test_simple_event passed")


def test_variables():
    """Test: Gestion des variables"""
    code = """
page Game
-button startBtn
--text "Start"

on start
 set score 0
 set lives 3
 alert("Game initialized!")
end

on click
 add score 10
 subtract lives 1
end
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    # Vérifie les actions
    js_code = result['code']
    assert "this.variables['score']" in js_code
    assert "this.variables['lives']" in js_code
    print("✓ test_variables passed")


def test_navigation():
    """Test: Navigation entre pages"""
    code = """
page Home
-button nextBtn
--text "Next"
--script goToGame

page GameScreen
-button backBtn
--text "Back"
--script goHome

on click
 connect.goto(GameScreen)
end

on click
 connect.goto(Home)
end
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    assert 'Home' in result['ast']['pages']
    assert 'GameScreen' in result['ast']['pages']
    js_code = result['code']
    assert "await this.showPage('GameScreen')" in js_code
    print("✓ test_navigation passed")


def test_multiple_events():
    """Test: Plusieurs événements"""
    code = """
on start
 set counter 0
 alert("App started!")
end

on click
 add counter 1
 alert("Clicked!")
end

on tick
 subtract timer 1
end
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    print("✓ test_multiple_events passed")


def test_error_handling():
    """Test: Détection d'erreurs"""
    code = """
page Home
-button btn
--text Click  # ERREUR: pas de guillemets
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    # Doit détecter l'erreur
    assert not result['success']
    assert len(result['errors']) > 0
    print("✓ test_error_handling passed")


def test_color_property():
    """Test: Propriété couleur"""
    code = """
page Home
-background
--color #FF0000

-text msg
--value "Red text"
--color red

-button btn
--text "Click"
--color #00FF00
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    page = result['ast']['pages']['Home']
    assert page['backgroundColor'] == '#FF0000'
    assert page['elements'][0]['properties']['color'] == 'red'
    assert page['elements'][1]['properties']['color'] == '#00FF00'
    print("✓ test_color_property passed")


def test_positions_and_sizes():
    """Test: Positions et tailles"""
    code = """
page Layout
-button btn1
--position 10 20
--size 100 50

-text txt1
--position 200 300
--fontsize 24

-image img1
--position 50 50
--size 200 150
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success']
    page = result['ast']['pages']['Layout']
    
    # Vérifie les positions
    assert page['elements'][0]['properties']['position'] == [10, 20]
    assert page['elements'][0]['properties']['size'] == [100, 50]
    assert page['elements'][1]['properties']['position'] == [200, 300]
    assert page['elements'][2]['properties']['position'] == [50, 50]
    assert page['elements'][2]['properties']['size'] == [200, 150]
    print("✓ test_positions_and_sizes passed")


def test_complex_game():
    """Test: Jeu complet"""
    code = """
# Game Pages
page MainMenu
-background
--color #2c3e50

-text gameTitle
--value "My Game"
--color white
--position 50 50
--fontsize 36

-button playBtn
--text "Play"
--color green
--position 100 200
--size 150 50
--corner 8
--fontsize 18
--script startGameScript

page GameLevel
-background
--color #3498db

-text scoreLabel
--value "Score: 0"
--color white
--position 20 20
--fontsize 24

-text timerLabel
--value "Time: 30"
--color yellow
--position 300 20
--fontsize 24

-button collectBtn
--text "Collect"
--color darkgreen
--position 200 300
--size 150 50
--script collectItemScript

page GameOver
-background
--color #e74c3c

-text endMsg
--value "Game Over!"
--color white
--position 50 50
--fontsize 32

-button retryBtn
--text "Retry"
--color green
--position 100 200
--size 150 50
--script startGameScript

# Game Logic
on start
 set score 0
 set timer 30
 set level 1
 alert("Welcome to My Game!")
end

on click
 add score 10
 subtract timer 1
 if timer == 0
  alert("Times up!")
 end
end

on tick
 subtract timer 1
end
"""
    compiler = ConnectScriptCompiler()
    result = compiler.compile(code)
    
    assert result['success'], f"Erreurs: {result['errors']}"
    
    # Vérifications
    ast = result['ast']
    assert len(ast['pages']) == 3  # 3 pages
    assert 'MainMenu' in ast['pages']
    assert 'GameLevel' in ast['pages']
    assert 'GameOver' in ast['pages']
    
    # Vérifie les éléments
    menu_page = ast['pages']['MainMenu']
    assert len(menu_page['elements']) == 2  # title + button
    
    game_page = ast['pages']['GameLevel']
    assert len(game_page['elements']) == 3  # 2 texts + 1 button
    
    print("✓ test_complex_game passed")


def run_all_tests():
    """Lance tous les tests"""
    print("\n" + "="*60)
    print("🧪 Exécution des tests ConnectScript Compiler")
    print("="*60 + "\n")
    
    tests = [
        test_simple_page,
        test_page_with_elements,
        test_simple_event,
        test_variables,
        test_navigation,
        test_multiple_events,
        test_error_handling,
        test_color_property,
        test_positions_and_sizes,
        test_complex_game,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 Résultats: {passed}/{len(tests)} tests réussis")
    
    if failed == 0:
        print("✅ Tous les tests sont passés!")
    else:
        print(f"❌ {failed} test(s) échoué(s)")
    
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
