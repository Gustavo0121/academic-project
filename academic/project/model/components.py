"""Componentes."""

import logging

import flet as ft
from academic.project import list_alunos
from academic.project.model.entidades import Aluno


class FormAluno(ft.View):
    """Classe dos formulários de aluno."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        super().__init__()
        self.events = events
        self.route: str | None = kwargs.get('route')
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.padding = 0

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[],
                ),
            ),
        ]

        self.name = ft.TextField(label='Nome do aluno')
        self.controls[0].content.controls.append(self.name)

        self.turma = ft.TextField(label='Turma')
        self.controls[0].content.controls.append(self.turma)

        self.nota = ft.TextField(label='Nota')
        self.controls[0].content.controls.append(self.nota)

        self.btn_linha = ft.Row(
            controls=[
                ft.TextButton('Adicionar nota', on_click=self.add_nota),
                ft.TextButton('Confirmar', on_click=self.confirm),
            ],
        )
        self.controls[0].content.controls.append(self.btn_linha)

    def add_nota(self, event: ft.ControlEvent):
        """Adiciona campo de nota no formulário."""
        self.controls[0].content.controls.insert(
            -1, ft.TextField(label='Nota')
        )
        event.page.update()

    def confirm(self, event: ft.ControlEvent):
        """Confirmar."""
        notas_alunos = [float(nota.value) for nota in self.controls[0].content.controls[2:-1]]
        result = Aluno(
            nome=self.name.value,
            turma=self.turma.value,
            notas=notas_alunos,
        )
        list_alunos.append(result)
        logging.info(result)
        for campos in self.controls[0].content.controls:
            campos.value = ''
        event.page.update()
