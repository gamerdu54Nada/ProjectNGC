"""
ConnectScript AST (Abstract Syntax Tree)
Structure pour représenter le code analysé
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class EventType(Enum):
    """Types d'événements supportés"""
    CLICK = "click"
    START = "start"
    LOAD = "load"
    TICK = "tick"


@dataclass
class Position:
    """Position d'un élément UI"""
    x: int
    y: int


@dataclass
class Size:
    """Taille d'un élément UI"""
    width: int
    height: int


@dataclass
class UIProperty:
    """Propriété d'un élément UI"""
    name: str
    value: Any
    line: int


@dataclass
class UIElement:
    """Représente un élément d'interface (Button, Text, Image)"""
    element_type: str  # button, text, image
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    line: int = 0
    
    def get_property(self, key: str, default=None):
        """Obtient une propriété avec valeur par défaut"""
        return self.properties.get(key, default)


@dataclass
class Page:
    """Représente une page"""
    name: str
    background_color: str = "white"
    elements: List[UIElement] = field(default_factory=list)
    line: int = 0


@dataclass
class Action:
    """Représente une action (alert, goto, etc.)"""
    action_type: str
    params: Dict[str, Any] = field(default_factory=dict)
    line: int = 0
    
    def __repr__(self):
        return f"{self.action_type}({self.params})"


@dataclass
class Condition:
    """Représente une condition"""
    operator: str  # ==, !=, <, >
    left: str  # variable name
    right: Any  # value
    line: int = 0


@dataclass
class IfStatement:
    """Représente une instruction if"""
    condition: Condition
    actions: List[Action] = field(default_factory=list)
    line: int = 0


@dataclass
class EventHandler:
    """Représente un gestionnaire d'événement"""
    event_type: EventType
    actions: List[Action] = field(default_factory=list)
    line: int = 0


@dataclass
class Script:
    """Représente un script (.psc)"""
    name: str
    event_handlers: List[EventHandler] = field(default_factory=list)
    line: int = 0


@dataclass
class Project:
    """Représente le projet complet"""
    pages: Dict[str, Page] = field(default_factory=dict)
    scripts: Dict[str, Script] = field(default_factory=dict)
    
    def add_page(self, page: Page):
        """Ajoute une page au projet"""
        if page.name in self.pages:
            raise ValueError(f"Page '{page.name}' existe déjà")
        self.pages[page.name] = page
    
    def add_script(self, script: Script):
        """Ajoute un script au projet"""
        if script.name in self.scripts:
            raise ValueError(f"Script '{script.name}' existe déjà")
        self.scripts[script.name] = script
    
    def get_page(self, name: str) -> Optional[Page]:
        """Obtient une page par nom"""
        return self.pages.get(name)
    
    def get_script(self, name: str) -> Optional[Script]:
        """Obtient un script par nom"""
        return self.scripts.get(name)


# Types de données
class DataType(Enum):
    """Types de données supportés"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    COLOR = "color"


@dataclass 
class Variable:
    """Représente une variable"""
    name: str
    data_type: DataType
    value: Any = None
