import sqlite3


def conectar(arquivo="estoque.db"):
    conn = sqlite3.connect(arquivo)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            minimo INTEGER NOT NULL DEFAULT 5
        )
    """)
    conn.commit()
    return conn


def cadastrar(conn, nome, categoria, preco, quantidade=0, minimo=5):
    cursor = conn.execute(
        "INSERT INTO produtos (nome, categoria, preco, quantidade, minimo) VALUES (?, ?, ?, ?, ?)",
        (nome, categoria, preco, quantidade, minimo),
    )
    conn.commit()
    return cursor.lastrowid


def listar(conn):
    return conn.execute(
        "SELECT id, nome, categoria, preco, quantidade, minimo FROM produtos ORDER BY nome"
    ).fetchall()


def buscar(conn, texto):
    return conn.execute(
        "SELECT id, nome, categoria, preco, quantidade, minimo FROM produtos WHERE nome LIKE ? ORDER BY nome",
        (f"%{texto}%",),
    ).fetchall()


def entrada(conn, id, quantidade):
    cursor = conn.execute(
        "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
        (quantidade, id),
    )
    conn.commit()
    return cursor.rowcount > 0


def saida(conn, id, quantidade):
    linha = conn.execute(
        "SELECT nome, quantidade FROM produtos WHERE id = ?",
        (id,),
    ).fetchone()

    if linha is None:
        return "Produto não encontrado."

    nome, atual = linha
    if quantidade > atual:
        return f"Estoque insuficiente: há {atual} unidade(s) de {nome}."

    conn.execute(
        "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
        (quantidade, id),
    )
    conn.commit()
    return f"Saída registrada: {quantidade} x {nome}."


def estoque_baixo(conn):
    return conn.execute(
        "SELECT id, nome, categoria, preco, quantidade, minimo FROM produtos WHERE quantidade < minimo ORDER BY nome"
    ).fetchall()


def valor_total(conn):
    total = conn.execute("SELECT SUM(preco * quantidade) FROM produtos").fetchone()[0]
    return total if total is not None else 0.0
