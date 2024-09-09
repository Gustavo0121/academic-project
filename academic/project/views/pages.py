"""Pages."""

import logging

import flet as ft
from academic.project.model.components import FormAluno


def main_view(e: ft.ControlEvent) -> ft.Control:
    """Main view."""
    logging.debug(e)
    return FormAluno(e, route='/')


def visualizar_view(e: ft.ControlEvent) -> ft.ControlEvent:
    """Visualizar view."""
    logging.debug(e)
    return ft.View(
        route='/visualizar',
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
