"""
ConnectScript Compiler Package
Un compilateur professionnel pour le langage ConnectScript
"""

__version__ = "1.0.0"
__author__ = "ConnectScript Team"

from .tokenizer import Tokenizer, TokenType, Token
from .ast_nodes import Project, Page, Script, EventType, UIElement
from .parser import Parser, parse_connect_script
from .errors import CompileErrorManager, CompileException, ParseError, TokenizeError
from .codegen import CodeGenerator, compile_project
from .event_system import EventBus, EventType as EventEnum, Event, EventListener

__all__ = [
    # Tokenizer
    'Tokenizer',
    'TokenType', 
    'Token',
    
    # AST
    'Project',
    'Page',
    'Script',
    'UIElement',
    'EventType',
    
    # Parser
    'Parser',
    'parse_connect_script',
    
    # Errors
    'CompileErrorManager',
    'CompileException',
    'ParseError',
    'TokenizeError',
    
    # Code Gen
    'CodeGenerator',
    'compile_project',
    
    # Events
    'EventBus',
    'EventEnum',
    'Event',
    'EventListener',
]


def compile_script(code: str) -> dict:
    """
    Compile un script ConnectScript
    
    Args:
        code: Code source en ConnectScript
        
    Returns:
        {
            'success': bool,
            'javascript': str,
            'ast': dict,
            'errors': [str],
            'warnings': [str]
        }
    """
    try:
        # Tokenize
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        
        # Parse
        parser = Parser(tokens, code)
        project = parser.parse()
        
        # Check errors
        if parser.error_manager.has_errors():
            return {
                'success': False,
                'javascript': '',
                'ast': {},
                'errors': [str(e) for e in parser.error_manager.get_errors()],
                'warnings': [str(e) for e in parser.error_manager.get_warnings()]
            }
        
        # Generate code
        js_code = compile_project(project, parser.error_manager)
        
        # Convert AST
        ast_dict = project_to_dict(project)
        
        return {
            'success': True,
            'javascript': js_code,
            'ast': ast_dict,
            'errors': [],
            'warnings': [str(e) for e in parser.error_manager.get_warnings()]
        }
    
    except Exception as e:
        return {
            'success': False,
            'javascript': '',
            'ast': {},
            'errors': [str(e)],
            'warnings': []
        }


def project_to_dict(project: Project) -> dict:
    """Convertit un Project en dictionnaire"""
    return {
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
