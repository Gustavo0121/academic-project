"""DataBase manipulation."""

import sys
from pathlib import Path

sys.path.append(
    Path(__file__).parents[2].resolve().as_posix(),
)

import sqlite3

from academic.project import DB, users


def execute(comandos: list[str], parametros: tuple = ()) -> bool:
    """Função para executar comandos SQL no banco de dados."""
    conn = sqlite3.connect(DB.as_posix())

    cursor = conn.cursor()

    for comando in comandos:
        cursor.execute(comando, parametros)
        conn.commit()

    conn.close()
    return True


def query(comando: str, parametros: tuple = ()) -> list:
    """Função para fazer uma query no banco."""
    conn = sqlite3.connect(DB.as_posix())

    cursor = conn.cursor()

    cursor.execute(comando, parametros)
    query_list = cursor.fetchall()
    conn.commit()

    conn.close()
    return query_list


if not DB.is_file():
    execute([
        """CREATE TABLE
        users(
        matricula integer not null,
        senha text not null,
        status text not null,
        nome text not null)""",
        """CREATE TABLE
        notas(
        id integer primary key autoincrement,
        nome text not null,
        turma text not null,
        nota_simulado1 integer not null,
        nota_simulado2 integer not null,
        nota_av integer not null,
        nota_nc integer not null,
        nota_avs integer not null,
        nota_final integer not null,
        status numeric not null)
""",
    ])

if __name__ == '__main__':
    for user in users.items():
        execute(
            [
                f"""INSERT INTO users VALUES
                ({user[0]}, '{user[1][0]}', '{user[1][1]}', '{user[1][2]}')""",
            ],
        )
