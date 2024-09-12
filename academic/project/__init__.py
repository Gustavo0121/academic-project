"""Módulo principal."""

import logging
from pathlib import Path

from academic.project.controllers.entidades import Aluno

__title__ = '.'.join(Path(__file__).parent.parts[-2:])

confproject = Path(__file__).parents[2] / 'pyproject.toml'
versionfile = Path(__file__).parent / 'version.txt'

list_alunos: list[Aluno] = []

DB = Path(__file__).parent.joinpath('model', 'sistema_notas.db')


if __name__ == '__main__':  # pragma: no cover
    logging.info('(%s)', __title__)
