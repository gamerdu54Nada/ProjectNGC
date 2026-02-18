"""
ConnectScript Parser
Convertit tokens en AST
"""
from typing import List, Optional, Dict, Any
from tokenizer import Token, TokenType, Tokenizer
from ast_nodes import (
    Project, Page, UIElement, Script, EventHandler, EventType,
    Action, Condition, IfStatement
)
from errors import ParseError, CompileErrorManager, ErrorLevel


class Parser:
    """Parse les tokens pour créer l'AST"""
    
    def __init__(self, tokens: List[Token], source_code: str):
        self.tokens = tokens
        self.position = 0
        self.project = Project()
        self.error_manager = CompileErrorManager(source_code)
        self.current_script_name = None
    
    def parse(self) -> Project:
        """Parse le code complet"""
        while not self._is_at_end():
            self._skip_newlines()
            
            if self._is_at_end():
                break
            
            if self._check(TokenType.PAGE):
                self._parse_page()
            elif self._check(TokenType.ON):
                self._parse_event_handler()
            else:
                token = self._current()
                self.error_manager.add_error(
                    f"Token inattendu: {token.type.name}",
                    token.line,
                    token.column,
                    suggestion="Esperait 'page' ou 'on'"
                )
                self._advance()
        
        return self.project
    
    def _parse_page(self):
        """Parse une déclaration de page"""
        page_token = self._consume(TokenType.PAGE)
        if not page_token:
            return
        
        name_token = self._consume(TokenType.IDENTIFIER)
        if not name_token:
            self.error_manager.add_error(
                "Nom de page manquant",
                self._current().line,
                self._current().column,
                suggestion="Utilisez: page <nom>"
            )
            return
        
        page_name = name_token.value
        page = Page(name=page_name, line=page_token.line)
        
        self._skip_newlines()
        
        # Parser les éléments de la page
        while not self._is_at_end() and not self._check(TokenType.PAGE) and not self._check(TokenType.ON):
            if self._check(TokenType.MINUS):
                self._parse_page_element(page)
            else:
                self._skip_newlines()
                if self._is_at_end() or self._check(TokenType.PAGE) or self._check(TokenType.ON):
                    break
        
        self.project.add_page(page)
    
    def _parse_page_element(self, page: Page):
        """Parse un élément de page (background, button, text, image)"""
        minus_token = self._consume(TokenType.MINUS)
        if not minus_token:
            return
        
        element_type_token = self._current()
        
        if element_type_token.type == TokenType.IDENTIFIER:
            if element_type_token.value == "background":
                self._advance()
                self._parse_background(page)
            elif element_type_token.value in ("button", "text", "image"):
                self._parse_ui_element(page)
            else:
                self.error_manager.add_error(
                    f"Type d'élément inconnu: {element_type_token.value}",
                    element_type_token.line,
                    element_type_token.column
                )
                self._advance()
        else:
            self.error_manager.add_error(
                "Type d'élément attendu",
                element_type_token.line,
                element_type_token.column
            )
            self._advance()
        
        self._skip_newlines()
    
    def _parse_background(self, page: Page):
        """Parse les propriétés du background"""
        self._skip_newlines()
        
        while not self._is_at_end() and self._check(TokenType.DOUBLE_MINUS):
            self._advance()  # Consume --
            
            prop_token = self._consume(TokenType.IDENTIFIER)
            if not prop_token:
                break
            
            prop_name = prop_token.value
            
            if prop_name == "color":
                color_token = self._consume(TokenType.COLOR)
                if color_token:
                    page.background_color = color_token.value
            
            self._skip_newlines()
    
    def _parse_ui_element(self, page: Page):
        """Parse un élément UI (button, text, image)"""
        element_type_token = self._consume(TokenType.IDENTIFIER)
        if not element_type_token:
            return
        
        element_type = element_type_token.value
        
        name_token = self._consume(TokenType.IDENTIFIER)
        if not name_token:
            self.error_manager.add_error(
                f"Nom d'{element_type} manquant",
                element_type_token.line,
                element_type_token.column
            )
            return
        
        element = UIElement(
            element_type=element_type,
            name=name_token.value,
            line=element_type_token.line
        )
        
        self._skip_newlines()
        
        # Parser les propriétés
        while not self._is_at_end() and self._check(TokenType.DOUBLE_MINUS):
            self._advance()  # Consume --
            
            prop_token = self._consume(TokenType.IDENTIFIER)
            if not prop_token:
                break
            
            prop_name = prop_token.value
            value = None
            
            if prop_name in ("text", "value"):
                value_token = self._consume(TokenType.STRING)
                if value_token:
                    value = value_token.value
            elif prop_name == "color":
                color_token = self._consume(TokenType.COLOR)
                if color_token:
                    value = color_token.value
            elif prop_name == "position":
                x_token = self._consume(TokenType.NUMBER)
                y_token = self._consume(TokenType.NUMBER)
                if x_token and y_token:
                    value = [x_token.value, y_token.value]
            elif prop_name == "size":
                w_token = self._consume(TokenType.NUMBER)
                h_token = self._consume(TokenType.NUMBER)
                if w_token and h_token:
                    value = [w_token.value, h_token.value]
            elif prop_name in ("fontsize", "corner"):
                num_token = self._consume(TokenType.NUMBER)
                if num_token:
                    value = num_token.value
            elif prop_name == "script":
                script_token = self._consume(TokenType.IDENTIFIER)
                if script_token:
                    value = script_token.value
            elif prop_name == "source":
                src_token = self._consume(TokenType.STRING)
                if src_token:
                    value = src_token.value
            
            if value is not None:
                element.properties[prop_name] = value
            
            self._skip_newlines()
        
        page.elements.append(element)
    
    def _parse_event_handler(self):
        """Parse un gestionnaire d'événement"""
        on_token = self._consume(TokenType.ON)
        if not on_token:
            return
        
        event_token = self._consume(TokenType.IDENTIFIER)
        if not event_token:
            self.error_manager.add_error(
                "Type d'événement manquant",
                on_token.line,
                on_token.column,
                suggestion="Utilisez: on <event>"
            )
            return
        
        event_name = event_token.value
        if event_name == "click":
            event_type = EventType.CLICK
        elif event_name == "start":
            event_type = EventType.START
        elif event_name == "load":
            event_type = EventType.LOAD
        elif event_name == "tick":
            event_type = EventType.TICK
        else:
            self.error_manager.add_warning(
                f"Type d'événement inconnu: {event_name}",
                event_token.line,
                event_token.column
            )
            event_type = EventType.CLICK  # Default
        
        self._skip_newlines()
        
        handler = EventHandler(event_type=event_type, line=on_token.line)
        actions = []
        
        # Parser les actions
        while not self._is_at_end() and not self._check(TokenType.END):
            if self._check(TokenType.ON):
                # Nouvelle déclaration d'événement
                handlers = self._extract_handlers_from_actions(actions)
                for h in handlers:
                    script = Script(name=self.current_script_name or "main", event_handlers=[h])
                    self.project.add_script(script)
                
                self._parse_event_handler()
                return
            
            action = self._parse_action()
            if action:
                actions.append(action)
            
            self._skip_newlines()
        
        self._consume(TokenType.END)
        handler.actions = actions
        
        # Créer un script pour cet handler
        script_name = self.current_script_name or f"script_{event_type.value}"
        script = Script(name=script_name, event_handlers=[handler], line=on_token.line)
        
        # Vérifier si le script existe
        if script_name not in self.project.scripts:
            self.project.scripts[script_name] = script
        else:
            self.project.scripts[script_name].event_handlers.append(handler)
    
    def _parse_action(self) -> Optional[Action]:
        """Parse une action"""
        token = self._current()
        
        if token.type == TokenType.ALERT:
            return self._parse_alert()
        elif token.type == TokenType.SET:
            return self._parse_set()
        elif token.type == TokenType.ADD:
            return self._parse_add()
        elif token.type == TokenType.SUBTRACT:
            return self._parse_subtract()
        elif token.type == TokenType.IDENTIFIER and token.value.startswith("connect"):
            return self._parse_goto()
        elif token.type == TokenType.IF:
            return self._parse_if()
        elif token.type == TokenType.NEWLINE:
            self._advance()
            return None
        else:
            self.error_manager.add_error(
                f"Action inconnue: {token.type.name}",
                token.line,
                token.column
            )
            self._advance()
            return None
    
    def _parse_alert(self) -> Optional[Action]:
        """Parse: alert("message")"""
        alert_token = self._consume(TokenType.ALERT)
        self._consume(TokenType.LPAREN)
        
        msg_token = self._consume(TokenType.STRING)
        if not msg_token:
            self.error_manager.add_error(
                "Message d'alerte manquant",
                alert_token.line,
                alert_token.column
            )
            return None
        
        self._consume(TokenType.RPAREN)
        
        return Action(
            action_type="alert",
            params={"message": msg_token.value},
            line=alert_token.line
        )
    
    def _parse_set(self) -> Optional[Action]:
        """Parse: set <var> <value>"""
        set_token = self._consume(TokenType.SET)
        
        var_token = self._consume(TokenType.IDENTIFIER)
        if not var_token:
            self.error_manager.add_error(
                "Nom de variable manquant",
                set_token.line,
                set_token.column
            )
            return None
        
        # Value peut être un nombre ou un identifiant
        value_token = self._current()
        value = None
        
        if value_token.type == TokenType.STRING:
            value = self._advance().value
        elif value_token.type == TokenType.NUMBER:
            value = self._advance().value
        elif value_token.type == TokenType.IDENTIFIER:
            value = self._advance().value
        else:
            self.error_manager.add_error(
                "Valeur manquante",
                set_token.line,
                set_token.column
            )
        
        return Action(
            action_type="set",
            params={"variable": var_token.value, "value": value},
            line=set_token.line
        )
    
    def _parse_add(self) -> Optional[Action]:
        """Parse: add <var> <number>"""
        add_token = self._consume(TokenType.ADD)
        
        var_token = self._consume(TokenType.IDENTIFIER)
        if not var_token:
            return None
        
        value_token = self._consume(TokenType.NUMBER)
        if not value_token:
            self.error_manager.add_error(
                "Valeur numérique manquante",
                add_token.line,
                add_token.column
            )
            return None
        
        return Action(
            action_type="add",
            params={"variable": var_token.value, "value": value_token.value},
            line=add_token.line
        )
    
    def _parse_subtract(self) -> Optional[Action]:
        """Parse: subtract <var> <number>"""
        sub_token = self._consume(TokenType.SUBTRACT)
        
        var_token = self._consume(TokenType.IDENTIFIER)
        if not var_token:
            return None
        
        value_token = self._consume(TokenType.NUMBER)
        if not value_token:
            self.error_manager.add_error(
                "Valeur numérique manquante",
                sub_token.line,
                sub_token.column
            )
            return None
        
        return Action(
            action_type="subtract",
            params={"variable": var_token.value, "value": value_token.value},
            line=sub_token.line
        )
    
    def _parse_goto(self) -> Optional[Action]:
        """Parse: connect.goto(page)"""
        # Token "connect.goto"
        goto_token = self._consume(TokenType.IDENTIFIER)
        if not goto_token or not goto_token.value.startswith("connect"):
            return None
        
        self._consume(TokenType.LPAREN)
        
        page_token = self._consume(TokenType.IDENTIFIER)
        if not page_token:
            self.error_manager.add_error(
                "Nom de page manquant",
                goto_token.line,
                goto_token.column
            )
            return None
        
        self._consume(TokenType.RPAREN)
        
        return Action(
            action_type="goto",
            params={"page": page_token.value},
            line=goto_token.line
        )
    
    def _parse_if(self) -> Optional[Action]:
        """Parse: if <condition> ... end"""
        if_token = self._consume(TokenType.IF)
        
        # Pour simplifier, on va stocker la condition comme string
        condition_str = ""
        while not self._is_at_end() and not self._check(TokenType.NEWLINE):
            condition_str += self._current().value or ""
            self._advance()
        
        return Action(
            action_type="if",
            params={"condition": condition_str},
            line=if_token.line
        )
    
    def _extract_handlers_from_actions(self, actions: List[Action]) -> List[EventHandler]:
        """Extrait les handlers des actions"""
        return []
    
    # Utility methods
    def _current(self) -> Token:
        """Token courant"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]  # EOF
    
    def _check(self, token_type: TokenType) -> bool:
        """Vérifie le type du token courant"""
        return self._current().type == token_type
    
    def _advance(self) -> Token:
        """Avance au prochain token"""
        token = self._current()
        if not self._is_at_end():
            self.position += 1
        return token
    
    def _consume(self, token_type: TokenType) -> Optional[Token]:
        """Consomme un token d'un type spécifique"""
        if self._check(token_type):
            return self._advance()
        return None
    
    def _skip_newlines(self):
        """Saute les newlines"""
        while self._check(TokenType.NEWLINE):
            self._advance()
    
    def _is_at_end(self) -> bool:
        """Vérifie si on est à la fin"""
        return self._current().type == TokenType.EOF


def parse_connect_script(code: str) -> tuple[Project, CompileErrorManager]:
    """Fonction pour tokenizer et parser le code"""
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    
    parser = Parser(tokens, code)
    project = parser.parse()
    
    return project, parser.error_manager
