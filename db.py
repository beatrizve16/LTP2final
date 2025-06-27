import sqlite3

class Database:
    def __init__(self, db_name='biblioteca.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor_id INTEGER NOT NULL,
                ano INTEGER,
                FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def obter_autores(self):
        self.cursor.execute("SELECT id, nome FROM autores ORDER BY nome")
        return self.cursor.fetchall()

    def adicionar_autor(self, nome):
        self.cursor.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        self.conn.commit()
        return self.cursor.lastrowid

    def obter_autor_por_nome(self, nome):
        self.cursor.execute("SELECT id FROM autores WHERE nome = ?", (nome,))
        return self.cursor.fetchone()

    def adicionar_livro(self, titulo, autor_id, ano):
        self.cursor.execute("INSERT INTO livros (titulo, autor_id, ano) VALUES (?, ?, ?)",
                            (titulo, autor_id, ano))
        self.conn.commit()

    def listar_livros(self):
        self.cursor.execute('''
            SELECT livros.id, livros.titulo, autores.nome, livros.ano
            FROM livros
            JOIN autores ON livros.autor_id = autores.id
            ORDER BY livros.titulo
        ''')
        return self.cursor.fetchall()

    def atualizar_livro(self, livro_id, titulo, autor_id, ano):
        self.cursor.execute("UPDATE livros SET titulo = ?, autor_id = ?, ano = ? WHERE id = ?",
                            (titulo, autor_id, ano, livro_id))
        self.conn.commit()
        return self.cursor.rowcount

    def deletar_livro(self, livro_id):
        self.cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def fechar(self):
        self.conn.close()
