"""Pages."""

import flet as ft
import logging

def main_view(e: ft.ControlEvent) -> ft.Control:
    """Main view."""
    logging.debug(e)
    return ft.View(
        route='/',
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        vertical_alignment = ft.MainAxisAlignment.CENTER,
        padding=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.TextField(
                            label='Nome do aluno',
                        ),
                        ft.TextField(
                            label='Turma',
                        ),
                        ft.TextField(
                            label='Nota',
                        ),
                        ft.Row(
                            controls=[
                                ft.TextButton('Adicionar nota'),
                                ft.TextButton('Novo aluno'),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )


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
