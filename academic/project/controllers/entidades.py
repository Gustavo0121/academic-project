"""Entidades."""

from dataclasses import dataclass


@dataclass
class Aluno:
    """Classe modelo para aluno."""

    nome: str
    turma: str
    notas: list[float]


@dataclass
class User:
    """Classe modelo para usuário."""

    matricula: int
    senha: str
    status: str
    nome: str