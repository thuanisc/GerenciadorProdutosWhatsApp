# produtos.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

ARQUIVO_PRODUTOS = 'produtos.json'

def carregar_produtos():
    if os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_produtos(produtos):
    with open(ARQUIVO_PRODUTOS, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

def abrir_cadastro(master):
    produtos = carregar_produtos()
    cadastro = tk.Toplevel(master)
    cadastro.title("Cadastro de Produtos")
    cadastro.geometry("600x400")

    cols = ("Nome", "Preço", "Observação")
    tree = ttk.Treeview(cadastro, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill='both', expand=True, pady=10)

    def atualizar_lista():
        tree.delete(*tree.get_children())
        for p in produtos:
            tree.insert("", tk.END, values=(p['nome'], f"R${p['preco']:.2f}".replace('.', ','), p.get('obs', '')))

    def adicionar():
        nome = simpledialog.askstring("Nome", "Nome do produto:")
        preco_str = simpledialog.askstring("Preço", "Preço unitário (ex: 12,50):")
        try:
            preco = float(preco_str.replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Preço inválido.")
            return
        obs = simpledialog.askstring("Observação", "Observações (opcional):")
        if nome:
            produtos.append({"nome": nome, "preco": preco, "obs": obs})
            salvar_produtos(produtos)
            atualizar_lista()

    def editar(index):
        produto = produtos[index]
        nome = simpledialog.askstring("Nome", "Nome do produto:", initialvalue=produto['nome'])
        preco_str = simpledialog.askstring("Preço", "Preço unitário (ex: 12,50):", initialvalue=str(produto['preco']).replace('.', ','))
        try:
            preco = float(preco_str.replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Preço inválido.")
            return
        obs = simpledialog.askstring("Observação", "Observações (opcional):", initialvalue=produto.get('obs', ''))
        produtos[index] = {"nome": nome, "preco": preco, "obs": obs}
        salvar_produtos(produtos)
        atualizar_lista()

    def remover():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            produtos.pop(index)
            salvar_produtos(produtos)
            atualizar_lista()

    def ao_duplo_clique(event):
        item = tree.identify_row(event.y)
        if item:
            index = tree.index(item)
            editar(index)

    tree.bind("<Double-1>", ao_duplo_clique)

    frame_botoes = tk.Frame(cadastro)
    frame_botoes.pack(pady=5)
    ttk.Button(frame_botoes, text="Adicionar", command=adicionar).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Remover Selecionado", command=remover).pack(side=tk.LEFT, padx=10)

    atualizar_lista()