"""Componentes."""

import logging
from typing import NoReturn

import flet as ft
from academic.project import list_alunos
from academic.project.model.entidades import Aluno


class FormAluno(ft.View):
    """Classe dos formulários de aluno."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init for FormAluno class."""
        super().__init__()
        self.events = events
        self.appbar = AppBar(events, 'Sistema de notas')
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

        self.media = ft.TextField(label='Média', value=6.0)
        self.controls[0].content.controls.append(self.media)

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

    def add_nota(self, event: ft.ControlEvent) -> NoReturn:
        """Adiciona campo de nota no formulário."""
        self.controls[0].content.controls.insert(
            -1,
            ft.TextField(label='Nota'),
        )
        event.page.update()

    def confirm(self, event: ft.ControlEvent) -> NoReturn:
        """Confirmar."""
        notas_alunos = [
            float(nota.value)
            for nota in self.controls[0].content.controls[3:-1]
        ]
        result = Aluno(
            nome=self.name.value,
            turma=self.turma.value,
            media=float(self.media.value),
            notas=notas_alunos,
        )
        list_alunos.append(result)
        logging.info(result)
        for campos in self.controls[0].content.controls[1:]:
            campos.value = ''
        event.page.update()


class TableView(ft.View):
    """Classe para visualizar as notas dos alunos."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init for TableView class."""
        super().__init__()
        self.events = events
        self.appbar = AppBar(events, 'Sistema de notas')
        self.route: str | None = kwargs.get('route')
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.padding = 0

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(''),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text('Nome'),
                ),
                ft.DataColumn(
                    ft.Text('Turma'),
                ),
                ft.DataColumn(
                    ft.Text('Notas'),
                ),
                ft.DataColumn(
                    ft.Text('Status'),
                ),
            ],
            rows=[],
        )
        for idx in range(len(list_alunos)):
            line = self.create_row(idx)
            self.tabela.rows.append(line)

        self.msg = ft.Text(
            value='Sem dados para exibir.',
            color=ft.colors.RED_800,
            weight=ft.FontWeight.BOLD,
            size=40,
        )

        self.controls = [
            ft.Container(
                content=self.tabela if list_alunos else self.msg,
            ),
        ]

    def create_row(self, idx: int) -> ft.DataRow:
        """Add row."""
        item = list_alunos[idx]
        return ft.DataRow(
            data=idx,
            cells=[
                ft.DataCell(ft.Text(str(idx + 1))),
                ft.DataCell(ft.Text(f'{item.nome}')),
                ft.DataCell(ft.Text(f'{item.turma}')),
                ft.DataCell(ft.Text(''.join(str(item.notas)))),
                ft.DataCell(ft.Text('Aprovado' if sum(item.notas) / len(item.notas) >= float(item.media) else 'Reprovado')),
            ],
        )


class AppBar(ft.AppBar):
    """Appbar component."""

    def __init__(self, events: ft.ControlEvent, titulo: str = ''):
        """Init for Appbar class."""
        super().__init__()
        self.events = events
        self.title = ft.Text(titulo, selectable=True)
        self.center_title = True

        self.alert = ft.AlertDialog(
            title='Não há dados para visualizar.',
        )

        self.leading = ft.Icon(ft.icons.MENU_BOOK)

        self.actions = [
            ft.PopupMenuButton(
                visible=True,
                icon=ft.icons.MENU,
                items=[
                    ft.PopupMenuItem(
                        text='Formulário',
                        on_click=lambda _: events.page.go('/'),
                    ),
                    ft.PopupMenuItem(
                        text='Visualizar notas',
                        on_click=lambda _: events.page.go('/notas'),
                    ),
                ],
            ),
        ]
