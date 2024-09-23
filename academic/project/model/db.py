"""DataBase manipulation."""

import sqlite3

from academic.project import DB


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
        users(matricula integer not null, senha text not null)""",
        """CREATE TABLE
        professor(matricula integer not null, senha text not null)""",
        """CREATE TABLE
        aluno(matricula integer not null, senha text not null)""",
    ])

if __name__ == '__main__':
    query("""SELECT * from users""")
