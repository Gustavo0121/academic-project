"""Componentes."""

import logging
from typing import NoReturn

import flet as ft
from academic.project import list_alunos, user_active
from academic.project.controllers.entidades import Aluno, User
from academic.project.model.db import query

users = query('SELECT * from users')
alunos = query("SELECT nome from users WHERE status = 'aluno'")


class Login(ft.View):
    """Classe para tela de login."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init for Login class."""
        super().__init__()
        self.events = events
        self.route: str | None = kwargs.get('route')
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.padding = 0

        self.not_user = ft.Text(
            'Usuário ou senha incorretos',
            color='red',
            size=20,
        )
        self.btn_email = ft.TextButton(
            'Entrar com e-mail de estudante',
            icon=ft.icons.EMAIL,
            width=320,
            height=50,
            style=ft.ButtonStyle(
                color='#ffffff',
                bgcolor='#0072C6',
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
        )
        self.matricula = ft.TextField(
            label='Matrícula',
            input_filter=ft.NumbersOnlyInputFilter(),
            suffix_icon=ft.icons.PERM_IDENTITY,
        )
        self.senha = ft.TextField(
            label='Senha',
            password=True,
            can_reveal_password=True,
        )
        self.captcha = ft.Checkbox(
            'Não sou um robô',
            shape=ft.RoundedRectangleBorder(radius=3),
            width=250,
            height=60,
            on_change=self.enter_validation,
        )
        self.entrar = ft.TextButton(
            'Entrar',
            disabled=True,
            on_click=self.to_enter,
            on_hover=self.hover_enter,
            width=320,
            height=50,
            style=ft.ButtonStyle(
                color='#ffffff',
                bgcolor='#8c8c8c',
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                'SGA - Sistema de Gerenciamento Acadêmico',
                            ),
                            padding=ft.padding.only(bottom=85, top=20),
                        ),
                        self.btn_email,
                        ft.Text('---------- ou ----------'),
                        self.matricula,
                        self.senha,
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    self.captcha,
                                    ft.Icon(ft.icons.RECYCLING),
                                ],
                            ),
                            bgcolor='#ebedeb',
                            border=ft.border.all(1, '#0a0a0a'),
                        ),
                        ft.Container(
                            content=self.entrar,
                            padding=ft.padding.only(top=65),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                width=350,
                height=events.page.window.height - 50,
                padding=30,
            ),
        ]

    def to_enter(self, event: ft.ControlEvent) -> NoReturn:
        """To enter."""
        prof_valid = (int(self.matricula.value), str(self.senha.value), 'professor')
        aluno_valid = (int(self.matricula.value), str(self.senha.value), 'aluno')

        if any(user[:len(prof_valid)] == prof_valid for user in users):
            user_act = query(f"SELECT * from users WHERE matricula == {self.matricula.value} and senha == '{self.senha.value}'")
            user_active.append(User(matricula=user_act[0][0], senha=user_act[0][1], status=user_act[0][2], nome=user_act[0][3]))
            print(users)
            event.page.go('/')
        elif any(user[:len(aluno_valid)] == aluno_valid for user in users):
            event.page.go('/notas')
        else:
            self.controls[0].content.controls.append(self.not_user)
            event.page.update()

    def hover_enter(self, event: ft.ControlEvent) -> NoReturn:
        """On hover enter button."""
        self.entrar.style.bgcolor = (
            '#1d7d1d'
            if event.data == 'true'
            else ft.colors.with_opacity(0.7, '#1d7d1d')
        )
        event.page.update()

    def enter_validation(self, event: ft.ControlEvent) -> NoReturn:
        """Validation for button enter disabled or not."""
        self.entrar.style.bgcolor = (
            ft.colors.with_opacity(0.7, '#1d7d1d')
            if self.captcha.value
            else '#8c8c8c'
        )
        self.entrar.disabled = not self.captcha.value
        event.page.update()


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

        self.materia = ft.Dropdown(
            label='Matéria',
            options=[
                ft.dropdown.Option('Aplic. de Cloud, Iot e Indústria 4.0 em Python'),
                ft.dropdown.Option('Programação Orientada a Objetos em Java'),
                ft.dropdown.Option('Desenvolvimento Rápido de Aplicações em Python'),
                ft.dropdown.Option('Programação de Microcontroladores'),
            ],
            width=700,
        )

        self.controls = [
            self.materia,
            ft.Container(
                content=ft.Column(
                    controls=[],
                ),
                width=700,
            ),
        ]

        self.name = ft.Dropdown(
            label='Nome do aluno',
            options=[
                ft.dropdown.Option(*aluno) for aluno in alunos
            ],
        )
        self.controls[1].content.controls.append(self.name)

        self.nota_av = ft.TextField(label='Nota AV')
        self.controls[1].content.controls.append(self.nota_av)

        self.nota_trabalho = ft.TextField(label='Nota Trabalho')
        self.controls[1].content.controls.append(self.nota_trabalho)

        self.btn_linha = ft.Row(
            controls=[
                ft.TextButton('Adicionar nota', on_click=self.add_nota),
                ft.TextButton('Confirmar', on_click=self.confirm),
            ],
        )
        self.controls[1].content.controls.append(self.btn_linha)

    def add_nota(self, event: ft.ControlEvent) -> NoReturn:
        """Adiciona campo de nota no formulário."""
        self.controls[1].content.controls.insert(
            -1,
            ft.TextField(label='Nota'),
        )
        event.page.update()

    def confirm(self, event: ft.ControlEvent) -> NoReturn:
        """Confirmar."""
        notas_alunos = [
            float(nota.value)
            for nota in self.controls[1].content.controls[1:-1]
        ]
        result = Aluno(
            nome=self.name.value,
            turma=self.materia.value,
            notas=notas_alunos,
        )
        list_alunos.append(result)
        logging.info(result)
        for campos in self.controls[1].content.controls:
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
                ft.DataCell(
                    ft.Text(
                        'Aprovado'
                        if sum(item.notas) / len(item.notas)
                        >= 6
                        else 'Reprovado',
                    ),
                ),
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
                    ft.PopupMenuItem(
                        text='Logoff',
                        on_click=lambda _: events.page.go('/login'),
                    ),
                ],
            ),
        ]


if __name__ == '__main__':
    print(users)