"""Main module."""

import logging
import os

import flet as ft
from academic.project.views.router import route_change, view_pop

if os.getenv('DEBUG_MODE'):
    logging.basicConfig(level=logging.INFO)


def main(page: ft.Page) -> None:
    """Main process."""
    page.title = 'Gerenciamento de notas'
    page.window.min_width = 1000
    page.window.min_height = 790
    page.padding = 0
    page.window.width = page.window.min_width
    page.window.height = page.window.min_height
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/login')


def app():
    """Run app."""
    ft.app(target=main, assets_dir='assets')


if __name__ == '__main__':
    app()
