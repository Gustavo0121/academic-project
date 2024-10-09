"""Módulo principal."""

import logging
from pathlib import Path

from academic.project.controllers.entidades import Aluno, User

__title__ = '.'.join(Path(__file__).parent.parts[-2:])

confproject = Path(__file__).parents[2] / 'pyproject.toml'
versionfile = Path(__file__).parent / 'version.txt'

list_alunos: list[Aluno] = []
users = {
        1: ['1', 'professor', 'Almir'],
        2: ['10', 'professor', 'Edgar'],
        3: ['11', 'aluno', 'Gustavo dos Santos Ribeiro'],
        4: ['100', 'aluno', 'Letycia'],
        5: ['101', 'aluno', 'Lana'],
        6: ['110', 'aluno', 'Breno Esser'],
        7: ['111', 'aluno', 'Daniel'],
        8: ['1000', 'aluno', 'Eduardo'],
        9: ['1001', 'aluno', 'Eric'],
        10: ['1010', 'aluno', 'Kaio'],
    }
user_active: list[User] = []
DB = Path(__file__).parent.joinpath('model', 'sistema_notas.db')


if __name__ == '__main__':  # pragma: no cover
    logging.info('(%s)', __title__)
