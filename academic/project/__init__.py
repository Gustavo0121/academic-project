"""Módulo principal."""

import logging
from pathlib import Path

from academic.project.controllers.entidades import Aluno

__title__ = '.'.join(Path(__file__).parent.parts[-2:])

confproject = Path(__file__).parents[2] / 'pyproject.toml'
versionfile = Path(__file__).parent / 'version.txt'

list_alunos: list[Aluno] = []
users = {
        1: ['1', 'professor'],
        2: ['10', 'professor'],
        3: ['11', 'aluno'],
        4: ['100', 'aluno'],
        5: ['101', 'aluno'],
        6: ['110', 'aluno'],
        7: ['111', 'aluno'],
        8: ['1000', 'aluno'],
        9: ['1001', 'aluno'],
        10: ['1010', 'aluno'],
    }
DB = Path(__file__).parent.joinpath('model', 'sistema_notas.db')


if __name__ == '__main__':  # pragma: no cover
    logging.info('(%s)', __title__)
