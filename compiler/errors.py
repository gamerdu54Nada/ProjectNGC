"""
ConnectScript Error Handling
Système de gestion d'erreurs avec numéros de ligne
"""
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ErrorLevel(Enum):
    """Niveaux d'erreur"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CompileError:
    """Représente une erreur de compilation"""
    level: ErrorLevel
    message: str
    line: int
    column: int
    code_context: Optional[str] = None
    suggestion: Optional[str] = None
    
    def __str__(self):
        """Format lisible"""
        result = f"[{self.level.value.upper()}] Ligne {self.line}, Colonne {self.column}: {self.message}"
        
        if self.code_context:
            result += f"\n  {self.code_context}"
            result += f"\n  {' ' * (self.column - 1)}^"
        
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        
        return result


class CompileErrorManager:
    """Gère les erreurs de compilation"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.split('\n')
        self.errors: List[CompileError] = []
    
    def add_error(
        self,
        message: str,
        line: int,
        column: int = 0,
        suggestion: Optional[str] = None,
        level: ErrorLevel = ErrorLevel.ERROR
    ) -> CompileError:
        """Ajoute une erreur"""
        code_context = self._get_line_context(line)
        
        error = CompileError(
            level=level,
            message=message,
            line=line,
            column=column,
            code_context=code_context,
            suggestion=suggestion
        )
        
        self.errors.append(error)
        return error
    
    def add_warning(
        self,
        message: str,
        line: int,
        column: int = 0,
        suggestion: Optional[str] = None
    ):
        """Ajoute un avertissement"""
        self.add_error(message, line, column, suggestion, ErrorLevel.WARNING)
    
    def _get_line_context(self, line: int) -> Optional[str]:
        """Obtient le contexte de la ligne"""
        if 1 <= line <= len(self.lines):
            return self.lines[line - 1]
        return None
    
    def has_errors(self) -> bool:
        """Vérifie s'il y a des erreurs"""
        return any(e.level == ErrorLevel.ERROR for e in self.errors)
    
    def get_errors(self) -> List[CompileError]:
        """Retourne les erreurs"""
        return [e for e in self.errors if e.level == ErrorLevel.ERROR]
    
    def get_warnings(self) -> List[CompileError]:
        """Retourne les avertissements"""
        return [e for e in self.errors if e.level == ErrorLevel.WARNING]
    
    def report(self) -> str:
        """Génère un rapport d'erreurs"""
        if not self.errors:
            return "✓ Aucune erreur"
        
        report = f"\n{'='*60}\n"
        report += f"Rapport de Compilation ({len(self.errors)} problème(s))\n"
        report += f"{'='*60}\n\n"
        
        for error in sorted(self.errors, key=lambda e: e.line):
            report += str(error) + "\n\n"
        
        error_count = len(self.get_errors())
        warning_count = len(self.get_warnings())
        
        report += f"Résumé: {error_count} erreur(s), {warning_count} avertissement(s)\n"
        
        return report


# Exceptions personnalisées
class ConnectScriptError(Exception):
    """Erreur base pour ConnectScript"""
    pass


class TokenizeError(ConnectScriptError):
    """Erreur de tokenization"""
    pass


class ParseError(ConnectScriptError):
    """Erreur de parsing"""
    pass


class CompileException(ConnectScriptError):
    """Erreur de compilation"""
    pass


class RuntimeException(ConnectScriptError):
    """Erreur à l'exécution"""
    pass
