import json
import sqlite3
from datetime import date


def conectar(arquivo="cineflix.db"):
    conn = sqlite3.connect(arquivo)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS titulos (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            duracao_min INTEGER NOT NULL,
            classificacao INTEGER NOT NULL,
            nota REAL NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS visualizacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil TEXT NOT NULL,
            titulo_id INTEGER NOT NULL,
            minutos INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (titulo_id) REFERENCES titulos(id)
        )
    """)
    conn.commit()
    return conn


def importar_catalogo(conn, caminho_json="catalogo.json"):
    qtd_existente = conn.execute("SELECT COUNT(*) FROM titulos").fetchone()[0]
    if qtd_existente > 0:
        return 0

    with open(caminho_json, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    for item in catalogo:
        conn.execute(
            """
            INSERT INTO titulos (id, titulo, tipo, genero, ano, duracao_min, classificacao, nota)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["id"],
                item["titulo"],
                item["tipo"],
                item["genero"],
                item["ano"],
                item["duracao_min"],
                item["classificacao"],
                item["nota"],
            ),
        )
    conn.commit()
    return len(catalogo)


def listar_catalogo(conn):
    return conn.execute(
        "SELECT id, titulo, tipo, genero, ano, duracao_min, classificacao, nota FROM titulos ORDER BY id"
    ).fetchall()


def registrar_visualizacao(conn, perfil, titulo_id, minutos):
    hoje = date.today().isoformat()
    try:
        conn.execute(
            "INSERT INTO visualizacoes (perfil, titulo_id, minutos, data) VALUES (?, ?, ?, ?)",
            (perfil, titulo_id, minutos, hoje),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def historico_perfil(conn, perfil):
    return conn.execute(
        """
        SELECT v.data, t.titulo, v.minutos
        FROM visualizacoes v
        JOIN titulos t ON t.id = v.titulo_id
        WHERE v.perfil = ?
        ORDER BY v.data DESC, v.id DESC
        """,
        (perfil,),
    ).fetchall()


def mais_assistidos(conn, limite=5):
    return conn.execute(
        """
        SELECT t.titulo, COUNT(v.id) AS vezes
        FROM visualizacoes v
        JOIN titulos t ON t.id = v.titulo_id
        GROUP BY v.titulo_id
        ORDER BY vezes DESC, t.titulo ASC
        LIMIT ?
        """,
        (limite,),
    ).fetchall()


def tempo_por_perfil(conn):
    return conn.execute(
        """
        SELECT perfil, SUM(minutos) AS total
        FROM visualizacoes
        GROUP BY perfil
        ORDER BY total DESC
        """
    ).fetchall()
