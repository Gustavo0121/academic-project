"""Router module."""

import logging
from typing import NoReturn

import flet as ft
from academic.project import user_active
from academic.project.views import pages

routes = {
    '/': pages.main_view,
    '/notas': pages.visualizar_view,
    '/notfound': pages.not_found_view,
    '/login': pages.login_view,
}


def view_pop(e: ft.ControlEvent) -> NoReturn:
    """View pop."""
    logging.info(e)
    e.page.views.pop()
    e.page.go(e.page.views[-1])


def route_change(e: ft.RouteChangeEvent) -> NoReturn:
    """Route change."""
    e.page.views.clear()
    for element in e.page.overlay:
        element.visible = False
    e.page.views.append(routes.get(e.page.route, pages.not_found_view)(e))
    logging.info(user_active)
    e.page.update()
