"""Entidades."""

from dataclasses import dataclass

@dataclass
class Aluno:
    """Classe modelo para aluno."""
    nome: str
    turma: str
    notas: list[float]
