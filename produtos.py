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
    produtos_filtrados = produtos.copy()
    cadastro = tk.Toplevel(master)
    cadastro.title("Cadastro de Produtos")
    cadastro.geometry("600x400")

    frame_pesquisa = tk.Frame(cadastro)
    frame_pesquisa.pack(pady=5)
    tk.Label(frame_pesquisa, text="Pesquisar:").pack(side=tk.LEFT)
    entrada_pesquisa = tk.Entry(frame_pesquisa, width=40)
    entrada_pesquisa.pack(side=tk.LEFT, padx=5)

    cols = ("Nome", "Preço", "Observação")
    tree = ttk.Treeview(cadastro, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill='both', expand=True, pady=10)

    def atualizar_lista(filtro=""):
        filtro_normalizado = filtro.lower().replace(',', '.')
        tree.delete(*tree.get_children())
        produtos_filtrados.clear()
        for p in produtos:
            nome = p['nome']
            preco = f"{p['preco']:.2f}".replace('.', ',')  # Para exibição
            preco_pesquisavel = f"{p['preco']:.2f}".replace(',', '.')  # Para comparação
            obs = p.get('obs', '')

            dados_pesquisaveis = f"{nome} {preco_pesquisavel} {obs}".lower()
            if filtro_normalizado in dados_pesquisaveis:
                produtos_filtrados.append(p)
                tree.insert("", tk.END, values=(nome, f"R${preco}", obs))
        btn_editar.config(state=tk.DISABLED)

    def ao_digitar(event):
        termo = entrada_pesquisa.get().strip()
        atualizar_lista(termo)

    entrada_pesquisa.bind("<KeyRelease>", ao_digitar)

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
        produto = produtos_filtrados[index]
        nome_original = produto['nome']
        preco_original = f"{produto['preco']:.2f}".replace('.', ',')
        obs_original = produto.get('obs', '')

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Produto")
        janela_editar.geometry("400x300")

        tk.Label(janela_editar, text="Nome:").pack()
        entry_nome = tk.Entry(janela_editar)
        entry_nome.insert(0, nome_original)
        entry_nome.pack()

        tk.Label(janela_editar, text="Preço (ex: 12,50):").pack()
        entry_preco = tk.Entry(janela_editar)
        entry_preco.insert(0, preco_original)
        entry_preco.pack()

        tk.Label(janela_editar, text="Observações:").pack()
        entry_obs = tk.Text(janela_editar, height=4)
        entry_obs.insert("1.0", obs_original)
        entry_obs.pack()

        btn_salvar = ttk.Button(janela_editar, text="Salvar", state=tk.DISABLED)
        btn_cancelar = ttk.Button(janela_editar, text="Cancelar", command=janela_editar.destroy)

        def verificar_alteracoes(event=None):
            nome = entry_nome.get().strip()
            preco = entry_preco.get().strip()
            obs = entry_obs.get("1.0", "end").strip()

            alguma_alteracao = (
                nome != nome_original or
                preco != preco_original or
                obs != obs_original
            )

            if alguma_alteracao:
                btn_salvar.config(state=tk.NORMAL)
            else:
                btn_salvar.config(state=tk.DISABLED)

        entry_nome.bind("<KeyRelease>", verificar_alteracoes)
        entry_preco.bind("<KeyRelease>", verificar_alteracoes)
        entry_obs.bind("<KeyRelease>", verificar_alteracoes)

        def salvar_edicao():
            nome = entry_nome.get().strip()
            preco_str = entry_preco.get().strip().replace(',', '.')
            obs = entry_obs.get("1.0", "end").strip()

            try:
                preco = float(preco_str)
            except:
                messagebox.showerror("Erro", "Preço inválido.")
                return

            for i, p in enumerate(produtos):
                if p == produto:
                    produtos[i] = {"nome": nome, "preco": preco, "obs": obs}
                    break

            salvar_produtos(produtos)
            atualizar_lista(entrada_pesquisa.get().strip())
            janela_editar.destroy()

        btn_salvar.config(command=salvar_edicao)

        frame_botoes = tk.Frame(janela_editar)
        frame_botoes.pack(pady=15)

        btn_salvar.pack(side=tk.LEFT, padx=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        frame_botoes.pack(anchor="center")

    def editar_produto_selecionado():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            editar(index)

    def remover():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            produto = produtos_filtrados[index]
            produtos.remove(produto)
            salvar_produtos(produtos)
            atualizar_lista(entrada_pesquisa.get().strip())

    def ao_duplo_clique(event):
        item = tree.identify_row(event.y)
        if item:
            index = tree.index(item)
            editar(index)

    def ao_selecionar(event):
        selecionado = tree.selection()
        if selecionado:
            btn_editar.config(state=tk.NORMAL)
        else:
            btn_editar.config(state=tk.DISABLED)

    tree.bind("<Double-1>", ao_duplo_clique)
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    frame_botoes = tk.Frame(cadastro)
    frame_botoes.pack(pady=5)
    ttk.Button(frame_botoes, text="Adicionar", command=adicionar).pack(side=tk.LEFT, padx=10)
    btn_editar = ttk.Button(frame_botoes, text="Editar Produto", command=editar_produto_selecionado, state=tk.DISABLED)
    btn_editar.pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Remover Selecionado", command=remover).pack(side=tk.LEFT, padx=10)

    atualizar_lista()