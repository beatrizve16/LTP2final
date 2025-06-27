import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Biblioteca OOP")
        self.root.geometry("700x450")
        self.root.resizable(False, False)

        self.setup_interface()
        self.carregar_autores()
        self.listar_livros()

    def setup_interface(self):
        tk.Label(self.root, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(self.root, state='readonly')
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Título").grid(row=1, column=0, padx=5, pady=5)
        self.entry_titulo = tk.Entry(self.root, width=40)
        self.entry_titulo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Autor").grid(row=2, column=0, padx=5, pady=5)
        self.combo_autor = ttk.Combobox(self.root, width=37)
        self.combo_autor.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Ano").grid(row=3, column=0, padx=5, pady=5)
        self.entry_ano = tk.Entry(self.root)
        self.entry_ano.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Adicionar", command=self.adicionar_livro).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Atualizar", command=self.atualizar_livro).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Deletar", command=self.deletar_livro).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Limpar", command=self.limpar_campos).grid(row=3, column=2, padx=5, pady=5)

        colunas = ('ID', 'Título', 'Autor', 'Ano')
        self.tree = ttk.Treeview(self.root, columns=colunas, show='headings', height=15)
        for col in colunas:
            self.tree.heading(col, text=col)
        self.tree.column('ID', width=40, anchor='center')
        self.tree.column('Título', width=300)
        self.tree.column('Autor', width=150)
        self.tree.column('Ano', width=60, anchor='center')
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_livro)

    def carregar_autores(self):
        autores = self.db.obter_autores()
        self.combo_autor['values'] = [a[1] for a in autores]
        self.combo_autor.ids = [a[0] for a in autores]

    def listar_livros(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.listar_livros():
            self.tree.insert('', tk.END, values=row)

    def adicionar_livro(self):
        
        titulo = self.entry_titulo.get().strip()
        autor_nome = self.combo_autor.get().strip()
        ano = self.entry_ano.get().strip()

        if not titulo or not autor_nome:
            messagebox.showwarning("Aviso", "Preencha título e autor.")
            return

        try:
            ano = int(ano) if ano else None
        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser numérico.")
            return 

        autor = self.db.obter_autor_por_nome(autor_nome)
        autor_id = autor[0] if autor else self.db.adicionar_autor(autor_nome)

        self.db.adicionar_livro(titulo, autor_id, ano)
        messagebox.showinfo("Sucesso", "Livro adicionado!")
        self.limpar_campos()
        self.listar_livros()
        self.carregar_autores()

    def selecionar_livro(self, event):
        selecionado = self.tree.focus()
        if selecionado:
            valores = self.tree.item(selecionado, 'values')
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, tk.END)
            self.entry_titulo.delete(0, tk.END)
            self.combo_autor.set('')
            self.entry_ano.delete(0, tk.END)

            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state='readonly')
            self.entry_titulo.insert(0, valores[1])
            self.combo_autor.set(valores[2])
            self.entry_ano.insert(0, valores[3])

    def atualizar_livro(self):
        livro_id = self.entry_id.get()
        titulo = self.entry_titulo.get().strip()
        autor_nome = self.combo_autor.get().strip()
        ano = self.entry_ano.get().strip()

        if not livro_id or not titulo or not autor_nome:
            messagebox.showwarning("Aviso", "Selecione e preencha os dados.")
            return

        try:
            ano = int(ano) if ano else None
        except ValueError:
            messagebox.showerror("Erro", "Ano inválido.")
            return

        autor = self.db.obter_autor_por_nome(autor_nome)
        autor_id = autor[0] if autor else self.db.adicionar_autor(autor_nome)

        rows = self.db.atualizar_livro(livro_id, titulo, autor_id, ano)
        if rows == 0:
            messagebox.showerror("Erro", "Livro não encontrado.")
        else:
            messagebox.showinfo("Sucesso", "Livro atualizado.")
            self.limpar_campos()
            self.listar_livros()
            self.carregar_autores()

    def deletar_livro(self):
        livro_id = self.entry_id.get()
        if not livro_id:
            messagebox.showwarning("Aviso", "Selecione um livro para deletar.")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este livro?")
        if confirm:
            deletado = self.db.deletar_livro(livro_id)
            if deletado == 0:
                messagebox.showerror("Erro", "Livro não encontrado.")
            else:
                messagebox.showinfo("Sucesso", "Livro deletado com sucesso!")
                self.limpar_campos()
                self.listar_livros()
                self.carregar_autores()

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_titulo.delete(0, tk.END)
        self.combo_autor.set('')
        self.entry_ano.delete(0, tk.END)
