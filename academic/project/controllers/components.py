"""Componentes."""

import logging
from typing import NoReturn

import flet as ft
from academic.project import MEDIA, list_alunos, user_active
from academic.project.controllers.entidades import Aluno, User
from academic.project.model.db import execute, query

users = query('SELECT * from users')
alunos = query("SELECT nome from users WHERE status = 'aluno'")


class Login(ft.View):
    """Classe para tela de login."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init for Login class."""
        super().__init__()
        self.events = events
        self.appbar = AppBar(
            events,
            'Sistema de notas',
            actions=[
                ft.IconButton(
                    icon=ft.icons.EXIT_TO_APP,
                    icon_color='#A40000',
                    on_click=self.close_app,
                    icon_size=40,
                ),
            ],
        )
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
            width=320,
        )
        self.senha = ft.TextField(
            label='Senha',
            password=True,
            can_reveal_password=True,
            width=320,
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
                                'SIA - Sistema de Informações Acadêmicas',
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                            padding=ft.padding.only(bottom=85, top=20),
                        ),
                        self.btn_email,
                        ft.Text(
                            '------------------- ou -------------------',
                            weight=ft.FontWeight.BOLD,
                        ),
                        self.matricula,
                        self.senha,
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    self.captcha,
                                    ft.Icon(ft.icons.RECYCLING),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor='#ebedeb',
                            border=ft.border.all(1, '#0a0a0a'),
                            width=320,
                            padding=ft.padding.only(right=8),
                        ),
                        ft.Container(
                            content=self.entrar,
                            padding=ft.padding.only(top=65),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    width=350,
                ),
                width=450,
                height=740,
                padding=30,
                border=ft.border.all(3, 'black'),
            ),
        ]

    def to_enter(self, event: ft.ControlEvent) -> NoReturn:
        """To enter."""
        prof_valid = (
            int(self.matricula.value),
            str(self.senha.value),
            'professor',
        )
        aluno_valid = (
            int(self.matricula.value),
            str(self.senha.value),
            'aluno',
        )

        if any(user[: len(prof_valid)] == prof_valid for user in users):
            user_act = query(
                r'SELECT * from users WHERE matricula == ? and senha == ?',
                (self.matricula.value, self.senha.value),
            )
            user_active.append(
                User(
                    matricula=user_act[0][0],
                    senha=user_act[0][1],
                    status=user_act[0][2],
                    nome=user_act[0][3],
                ),
            )
            logging.info(users)
            event.page.go('/')
        elif any(user[: len(aluno_valid)] == aluno_valid for user in users):
            user_act = query(
                r'SELECT * from users WHERE matricula == ? and senha == ?',
                (self.matricula.value, self.senha.value),
            )
            user_active.append(
                User(
                    matricula=user_act[0][0],
                    senha=user_act[0][1],
                    status=user_act[0][2],
                    nome=user_act[0][3],
                ),
            )
            logging.info(users)
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

    def close_app(self, event: ft.ControlEvent) -> None:
        """Close app."""
        event.page.window_close()


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
                width=700,
                height=550,
                padding=30,
                border=ft.border.all(3, 'black'),
            ),
        ]

        self.turma = ft.Dropdown(
            label='Matéria',
            options=[
                ft.dropdown.Option(
                    'Aplic. de Cloud, Iot e Indústria 4.0 em Python',
                ),
                ft.dropdown.Option('Programação Orientada a Objetos em Java'),
                ft.dropdown.Option(
                    'Desenvolvimento Rápido de Aplicações em Python',
                ),
                ft.dropdown.Option('Programação de Microcontroladores'),
            ],
            width=700,
        )
        self.controls[0].content.controls.append(self.turma)

        self.name = ft.Dropdown(
            label='Nome do aluno',
            options=[ft.dropdown.Option(*aluno) for aluno in alunos],
        )
        self.controls[0].content.controls.append(self.name)

        self.simulado1 = ft.TextField(
            label='Simulado 1',
            input_filter=ft.InputFilter(
                regex_string=r'^(0(\.\d{0,9})?|1(\.0{0,9})?)$',
            ),
        )
        self.controls[0].content.controls.append(self.simulado1)

        self.simulado2 = ft.TextField(
            label='Simulado 2',
            input_filter=ft.InputFilter(
                regex_string=r'^(0(\.\d{0,9})?|1(\.0{0,9})?)$',
            ),
        )
        self.controls[0].content.controls.append(self.simulado2)

        self.nota_av = ft.TextField(
            label='Nota AV',
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.controls[0].content.controls.append(self.nota_av)

        self.nota_nc = ft.TextField(
            label='Nota Nova chance',
            value=0,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.controls[0].content.controls.append(self.nota_nc)

        self.nota_avs = ft.TextField(
            label='Nota AVS',
            value=0,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.controls[0].content.controls.append(self.nota_avs)

        self.btn_confirm = ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Text('Confirmar'),
                    ft.Icon(name=ft.icons.CHECK_BOX_ROUNDED),
                ],
            ),
            on_click=self.confirm,
            on_hover=self.hover_confirm,
            width=130,
            height=50,
            style=ft.ButtonStyle(
                color='#ffffff',
                bgcolor='#8c8c8c',
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
        )
        self.controls[0].content.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.btn_confirm,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.only(top=20),
            ),
        )

    def hover_confirm(self, event: ft.ControlEvent) -> NoReturn:
        """On hover enter button."""
        self.btn_confirm.style.bgcolor = (
            '#1d7d1d' if event.data == 'true' else '#8c8c8c'
        )
        event.page.update()

    def confirm(self, event: ft.ControlEvent) -> NoReturn:
        """Confirmar."""
        nota_final = (
            float(self.simulado1.value)
            + float(self.simulado2.value)
            + float(self.nota_av.value)
            + float(self.nota_nc.value)
            + float(self.nota_avs.value)
        )
        execute(
            [
                f"""INSERT INTO notas(
                nome, turma, nota_simulado1, nota_simulado2, nota_av, nota_nc,
                nota_avs, nota_final, status) VALUES
                ('{self.name.value}', '{self.turma.value}',
                {self.simulado1.value}, {self.simulado2.value},
                {self.nota_av.value}, {self.nota_nc.value},
                {self.nota_avs.value}, {nota_final},
                {1 if nota_final >= MEDIA else 0})""",
            ],
        )
        result = Aluno(
            nome=self.name.value,
            turma=self.turma.value,
            notas=[
                self.simulado1.value,
                self.simulado2.value,
                self.nota_av.value,
                self.nota_nc.value,
                self.nota_avs.value,
            ],
        )
        list_alunos.append(result)
        logging.info(result)
        for campos in self.controls[0].content.controls[1:-1]:
            campos.value = (
                0 if campos.label in ('Nota Nova chance', 'Nota AVS') else ''
            )
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
        self.notas = query('SELECT * from notas')
        self.dlg_modal = ft.AlertDialog()

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text('Nome'),
                ),
                ft.DataColumn(
                    ft.Text('Turma'),
                ),
                ft.DataColumn(
                    ft.Text('Simulado 1'),
                ),
                ft.DataColumn(
                    ft.Text('Simulado 2'),
                ),
                ft.DataColumn(
                    ft.Text('Nota AV'),
                ),
                ft.DataColumn(
                    ft.Text('Nota NC'),
                ),
                ft.DataColumn(
                    ft.Text('Nota AVS'),
                ),
                ft.DataColumn(
                    ft.Text('Nota final'),
                ),
                ft.DataColumn(
                    ft.Text('Status'),
                ),
            ],
            rows=[],
        )

        self.tabela_prof = ft.DataTable(
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
                    ft.Text('Simulado 1'),
                ),
                ft.DataColumn(
                    ft.Text('Simulado 2'),
                ),
                ft.DataColumn(
                    ft.Text('Nota AV'),
                ),
                ft.DataColumn(
                    ft.Text('Nota NC'),
                ),
                ft.DataColumn(
                    ft.Text('Nota AVS'),
                ),
                ft.DataColumn(
                    ft.Text('Nota final'),
                ),
                ft.DataColumn(
                    ft.Text('Status'),
                ),
                ft.DataColumn(ft.Text('')),
                ft.DataColumn(ft.Text('')),
            ],
            rows=[],
        )

        for idx, nota in enumerate(self.notas):
            line = self.create_row(idx, nota)
            if line and user_active[-1].status == 'aluno':
                self.tabela.rows.append(line)
            elif line and user_active[-1].status == 'professor':
                self.tabela_prof.rows.append(line)

        self.msg = ft.Text(
            value='Sem dados para exibir.',
            color=ft.colors.RED_800,
            weight=ft.FontWeight.BOLD,
            size=40,
        )

        self.controls = [
            ft.Container(
                content=self.tabela
                if user_active[-1].status == 'aluno'
                else self.tabela_prof,
            ),
        ]

    def create_row(self, idx: int, item: tuple) -> ft.DataRow | None:
        """Add row."""
        if item[1] == user_active[-1].nome:
            return ft.DataRow(
                data=idx,
                cells=[
                    ft.DataCell(ft.Text(f'{item[1]}')),
                    ft.DataCell(ft.Text(f'{item[2]}')),
                    ft.DataCell(ft.Text(f'{item[3]}')),
                    ft.DataCell(ft.Text(f'{item[4]}')),
                    ft.DataCell(ft.Text(f'{item[5]}')),
                    ft.DataCell(ft.Text(f'{item[6]}')),
                    ft.DataCell(ft.Text(f'{item[7]}')),
                    ft.DataCell(ft.Text(f'{item[8]}')),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                'Aprovado' if bool(item[9]) else 'Reprovado',
                                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            bgcolor=ft.colors.with_opacity(0.8, '#03fc03')
                            if bool(item[9])
                            else ft.colors.with_opacity(0.8, '#bf0a0a'),
                            width=150,
                            alignment=ft.alignment.center,
                        ),
                    ),
                ],
            )
        if user_active[-1].status == 'professor':
            return ft.DataRow(
                data=idx,
                cells=[
                    ft.DataCell(ft.Text(f'{item[0]}')),
                    ft.DataCell(ft.Text(f'{item[1]}')),
                    ft.DataCell(ft.Text(f'{item[2]}')),
                    ft.DataCell(ft.Text(f'{item[3]}')),
                    ft.DataCell(ft.Text(f'{item[4]}')),
                    ft.DataCell(ft.Text(f'{item[5]}')),
                    ft.DataCell(ft.Text(f'{item[6]}')),
                    ft.DataCell(ft.Text(f'{item[7]}')),
                    ft.DataCell(ft.Text(f'{item[8]}')),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                'Aprovado' if bool(item[9]) else 'Reprovado',
                                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            bgcolor=ft.colors.with_opacity(0.8, '#03fc03')
                            if bool(item[9])
                            else ft.colors.with_opacity(0.8, '#bf0a0a'),
                            width=150,
                            alignment=ft.alignment.center,
                        ),
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            ft.icons.EDIT_DOCUMENT,
                            data=[idx, item[0]],
                            on_click=self.dlgmodal,
                        ),
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            ft.icons.DELETE,
                            data=[idx, item[0]],
                            icon_color='#A40000',
                            on_click=self.delete,
                        ),
                    ),
                ],
            )
        return None

    def delete(self, event: ft.ControlEvent) -> None:
        """Delete a row of DataTable."""
        logging.info(idx := event.control.data)
        del self.tabela_prof.rows[idx[0]]
        execute([f'DELETE FROM notas WHERE id = {idx[1]}'])  #noqa: S608
        event.page.update()

    def dlgmodal(self, event: ft.ControlEvent) -> None:
        """Edit a row of DataTable."""
        self.notas = query('SELECT * from notas')
        logging.info(idx := event.control.data)
        item = self.notas[idx[0]]
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text('Confirme atualização'),
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label='Índice',
                        value=item[0],
                        read_only=True,
                    ),
                    ft.TextField(
                        label='Nome',
                        value=item[1],
                        read_only=True,
                    ),
                    ft.TextField(
                        label='Turma',
                        value=item[2],
                        read_only=True,
                    ),
                    ft.TextField(
                        label='Nota Simulado 1',
                        value=item[3],
                    ),
                    ft.TextField(
                        label='Nota Simulado 2',
                        value=item[4],
                    ),
                    ft.TextField(
                        label='Nota AV',
                        value=item[5],
                    ),
                    ft.TextField(
                        label='Nota NC',
                        value=item[6],
                    ),
                    ft.TextField(
                        label='Nota AVS',
                        value=item[7],
                    ),
                    ft.TextField(
                        label='Nota final',
                        value=item[8],
                        read_only=True,
                    ),
                    ft.TextField(
                        label='Status',
                        value='Aprovado' if bool(item[9]) else 'Reprovado',
                        read_only=True,
                    ),
                ],
            ),
            actions=[
                ft.TextButton(
                    'Cancelar',
                    on_click=lambda e: e.page.close(self.dlg_modal),
                ),
                ft.TextButton(
                    'Atualizar',
                    on_click=lambda e: (
                        logging.info('%s', idx),
                        self.edit(
                            event=e,
                            idx=idx,
                            item=(
                                self.dlg_modal.content.controls[0].value,
                                self.dlg_modal.content.controls[1].value,
                                self.dlg_modal.content.controls[2].value,
                                self.dlg_modal.content.controls[3].value,
                                self.dlg_modal.content.controls[4].value,
                                self.dlg_modal.content.controls[5].value,
                                self.dlg_modal.content.controls[6].value,
                                self.dlg_modal.content.controls[7].value,
                                (
                                    float(
                                        self.dlg_modal.content.controls[
                                            3
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            4
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            5
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            6
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            7
                                        ].value,
                                    )
                                ),
                                1
                                if (
                                    float(
                                        self.dlg_modal.content.controls[
                                            3
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            4
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            5
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            6
                                        ].value,
                                    )
                                    + float(
                                        self.dlg_modal.content.controls[
                                            7
                                        ].value,
                                    )
                                )
                                >= MEDIA
                                else 0,
                            ),
                        ),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: e.page.add(
                ft.Text('Modal dialog dismissed'),
            ),
        )
        event.page.open(self.dlg_modal)

    def edit(
        self,
        event: ft.ControlEvent,
        idx: int,
        item: tuple,
    ) -> NoReturn:
        """Edit form data."""
        execute(
            [
                r"""UPDATE notas SET nota_simulado1 = ?,
            nota_simulado2 = ?, nota_av = ?,
            nota_nc = ?, nota_avs = ?, nota_final = ?,
            status = ? WHERE id = ?""",
            ],
            (
                item[3],
                item[4],
                item[5],
                item[6],
                item[7],
                item[8],
                item[9],
                idx[1],
            ),
        )
        self.tabela_prof.rows[idx[0]] = self.create_row(idx[0], item)
        event.page.close(self.dlg_modal)
        self.tabela_prof.update()


class AppBar(ft.AppBar):
    """Appbar component."""

    def __init__(
        self,
        events: ft.ControlEvent,
        titulo: str = '',
        actions: list | None = None,
    ):
        """Init for Appbar class."""
        super().__init__()
        self.events = events
        self.title = ft.Text(
            titulo,
            selectable=True,
            weight=ft.FontWeight.BOLD,
            size=30,
        )
        self.center_title = True
        self.toolbar_height = 70

        self.alert = ft.AlertDialog(
            title='Não há dados para visualizar.',
        )

        self.leading = ft.Icon(ft.icons.MENU_BOOK, size=40)

        self.actions = (
            actions
            if actions
            else [
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
                        ft.PopupMenuItem(
                            text='Exit',
                            on_click=self.close_app,
                        ),
                    ]
                    if user_active[-1].status == 'professor'
                    else [
                        ft.PopupMenuItem(
                            text='Visualizar notas',
                            on_click=lambda _: events.page.go('/notas'),
                        ),
                        ft.PopupMenuItem(
                            text='Logoff',
                            on_click=lambda _: events.page.go('/login'),
                        ),
                        ft.PopupMenuItem(
                            text='Exit',
                            on_click=self.close_app,
                        ),
                    ],
                ),
            ]
        )

    def close_app(self, event: ft.ControlEvent) -> None:
        """Close app."""
        event.page.window_close()


if __name__ == '__main__':
    logging.info(users)
