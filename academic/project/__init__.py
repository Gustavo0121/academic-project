"""Módulo principal."""

import logging
from pathlib import Path

from academic.project.model.entidades import Aluno

__title__ = '.'.join(Path(__file__).parent.parts[-2:])

confproject = Path(__file__).parents[2] / 'pyproject.toml'
versionfile = Path(__file__).parent / 'version.txt'

list_alunos: list[Aluno] = []


if __name__ == '__main__':  # pragma: no cover
    logging.info('(%s)', __title__)
