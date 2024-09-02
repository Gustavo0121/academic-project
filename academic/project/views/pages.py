"""Pages."""

import flet as ft
import logging

def main_view(e: ft.ControlEvent) -> ft.Control:
    """Main view."""
    logging.debug(e)
    return ft.View(
        route='/',
        controls=[
            ft.Text('Página principal'),
        ],
    )


def not_found_view(e: ft.ControlEvent) -> ft.Control:
    """Notfount view."""
    logging.debug(e)
    return ft.View(
        route='/notfound',
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        value='Recurso não encontrado...',
                        color='red',
                        weight='bold',
                    ),
                ],
            ),
        ],
    )
