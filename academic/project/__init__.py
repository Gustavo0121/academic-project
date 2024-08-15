"""Módulo principal."""

import logging
from pathlib import Path

__version__ = ''
__title__ = '.'.join(Path(__file__).parent.parts[-2:])

confproject = Path(__file__).parents[2] / 'pyproject.toml'
versionfile = Path(__file__).parent / 'version.txt'


try:
    __version__ = versionfile.read_text().strip()

except FileNotFoundError:
    pass

if __name__ == '__main__':  # pragma: no cover
    logging.info('(%s) %s by %s', __title__, __version__)
