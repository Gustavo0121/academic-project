"""DataBase manipulation."""

import sqlite3

from academic.project import DB, users


def execute(comandos: list[str]) -> bool:
    """Função para executar comandos SQL no banco de dados."""
    conn = sqlite3.connect(DB.as_posix())

    cursor = conn.cursor()

    for comando in comandos:
        cursor.execute(comando)
        conn.commit()

    conn.close()
    return True


def query(comando: str) -> list:
    """Função para fazer uma query no banco."""
    conn = sqlite3.connect(DB.as_posix())

    cursor = conn.cursor()

    cursor.execute(comando)
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
        nome text not null,
        turma text not null,
        nota_av integer not null,
        nota_trabalho integer not null,
        status numeric not null)
"""
    ])

if __name__ == '__main__':
    for user in users.items():
        execute(
            [
                f"""INSERT INTO users VALUES
                ({user[0]}, '{user[1][0]}', '{user[1][1]}', '{user[1][2]}')""",
            ],
        )
