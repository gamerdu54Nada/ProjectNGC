"""
ConnectScript Event System
Système d'événements robuste et typé
"""
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Types d'événements disponibles"""
    CLICK = "click"
    START = "start"
    LOAD = "load"
    TICK = "tick"
    ON_VARIABLE_CHANGE = "onVariableChange"
    ON_PAGE_CHANGE = "onPageChange"


@dataclass
class Event:
    """Représente un événement"""
    type: EventType
    source: str  # Nom du composant
    timestamp: float
    data: Dict[str, Any] = None


class EventListener(ABC):
    """Interface pour un écouteur d'événement"""
    
    @abstractmethod
    def handle(self, event: Event) -> None:
        """Traite l'événement"""
        pass


class EventHandler(EventListener):
    """Gestionnaire d'événement basé sur une fonction"""
    
    def __init__(self, callback: Callable[[Event], None]):
        self.callback = callback
    
    def handle(self, event: Event) -> None:
        """Appelle la fonction de callback"""
        try:
            self.callback(event)
        except Exception as e:
            print(f"Error in event handler: {e}")


class EventBus:
    """Bus d'événements central"""
    
    def __init__(self):
        self.listeners: Dict[EventType, List[EventListener]] = {}
        self.history: List[Event] = []
    
    def subscribe(self, event_type: EventType, listener: EventListener) -> Callable:
        """S'abonne à un type d'événement"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        self.listeners[event_type].append(listener)
        
        # Retourner une fonction pour se désabonner
        def unsubscribe():
            if event_type in self.listeners:
                self.listeners[event_type].remove(listener)
        
        return unsubscribe
    
    def emit(self, event: Event) -> None:
        """Émet un événement"""
        self.history.append(event)
        
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                listener.handle(event)
    
    def on(self, event_type: EventType, callback: Callable[[Event], None]) -> Callable:
        """Syntaxe simplifiée pour s'abonner"""
        handler = EventHandler(callback)
        return self.subscribe(event_type, handler)
    
    def clear_history(self):
        """Efface l'historique"""
        self.history = []
    
    def get_events_of_type(self, event_type: EventType) -> List[Event]:
        """Obtient les événements d'un type"""
        return [e for e in self.history if e.type == event_type]


class EventContext:
    """Contexte d'exécution pour les événements"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.variables: Dict[str, Any] = {}
        self.current_page: str = None
    
    def set_variable(self, name: str, value: Any) -> None:
        """Définit une variable"""
        old_value = self.variables.get(name)
        self.variables[name] = value
        
        # Émettre un événement si la valeur a changé
        if old_value != value:
            self.event_bus.emit(Event(
                type=EventType.ON_VARIABLE_CHANGE,
                source=f"variable:{name}",
                timestamp=0,
                data={"name": name, "old": old_value, "new": value}
            ))
    
    def get_variable(self, name: str, default=None) -> Any:
        """Obtient une variable"""
        return self.variables.get(name, default)
    
    def navigate_to_page(self, page_name: str) -> None:
        """Navigue vers une page"""
        old_page = self.current_page
        self.current_page = page_name
        
        self.event_bus.emit(Event(
            type=EventType.ON_PAGE_CHANGE,
            source="app",
            timestamp=0,
            data={"from": old_page, "to": page_name}
        ))


# Convenience functions
def create_event(event_type: EventType, source: str, data: Dict[str, Any] = None) -> Event:
    """Factory pour créer un événement"""
    import time
    return Event(
        type=event_type,
        source=source,
        timestamp=time.time(),
        data=data or {}
    )


def create_event_bus() -> EventBus:
    """Crée un bus d'événements"""
    return EventBus()


def create_event_context(event_bus: EventBus) -> EventContext:
    """Crée un contexte d'exécution"""
    return EventContext(event_bus)
