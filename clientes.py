import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import re

ARQUIVO_CLIENTES = 'clientes.json'

def telefone_valido(numero):
    return bool(re.fullmatch(r'[\d\-\(\) ]{8,}', numero.strip()))

def email_valido(email):
    if not email.strip():
        return True  # Campo opcional
    return bool(re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", email.strip()))

def carregar_clientes():
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, 'w', encoding='utf-8') as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)

def abrir_cadastro_clientes(master):
    clientes = carregar_clientes()
    clientes_filtrados = clientes.copy()

    cadastro = tk.Toplevel(master)
    cadastro.title("Cadastro de Clientes")
    cadastro.geometry("700x450")

    frame_pesquisa = tk.Frame(cadastro)
    frame_pesquisa.pack(pady=5)
    tk.Label(frame_pesquisa, text="Pesquisar:").pack(side=tk.LEFT)
    entrada_pesquisa = tk.Entry(frame_pesquisa, width=40)
    entrada_pesquisa.pack(side=tk.LEFT, padx=5)

    cols = ("Telefone", "Nome", "E-mail", "Observações")
    tree = ttk.Treeview(cadastro, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=160)
    tree.pack(fill='both', expand=True, pady=10)

    def atualizar_lista(filtro=""):
        tree.delete(*tree.get_children())
        clientes_filtrados.clear()
        for c in clientes:
            dados = f"{c['telefone']} {c.get('nome','')} {c.get('email','')} {c.get('obs','')}".lower()
            if filtro.lower() in dados:
                clientes_filtrados.append(c)
                tree.insert("", tk.END, values=(
                    c['telefone'],
                    c.get('nome', ''),
                    c.get('email', ''),
                    c.get('obs', '')
                ))
        btn_editar.config(state=tk.DISABLED)

    def ao_digitar(event):
        termo = entrada_pesquisa.get().strip()
        atualizar_lista(termo)

    entrada_pesquisa.bind("<KeyRelease>", ao_digitar)

    def adicionar():
        telefone = simpledialog.askstring("Telefone", "Telefone do cliente (obrigatório):")
        if not telefone or not telefone_valido(telefone):
            messagebox.showerror("Erro", "Telefone inválido.")
            return

        nome = simpledialog.askstring("Nome", "Nome do cliente (opcional):")
        email = simpledialog.askstring("E-mail", "E-mail do cliente (opcional):")
        if email and not email_valido(email):
            messagebox.showerror("Erro", "E-mail inválido.")
            return

        obs = simpledialog.askstring("Observações", "Observações (opcional):")
        clientes.append({
            "telefone": telefone.strip(),
            "nome": nome.strip() if nome else "",
            "email": email.strip() if email else "",
            "obs": obs.strip() if obs else ""
        })
        salvar_clientes(clientes)
        atualizar_lista(entrada_pesquisa.get().strip())

    def editar(index):
        cliente = clientes_filtrados[index]
        original = cliente.copy()

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Cliente")
        janela_editar.geometry("400x350")

        campos = {}

        def criar_entrada(label, chave, valor_inicial):
            tk.Label(janela_editar, text=label).pack()
            entrada = tk.Entry(janela_editar)
            entrada.insert(0, valor_inicial or "")
            entrada.pack()
            campos[chave] = entrada

        criar_entrada("Telefone (obrigatório):", "telefone", cliente['telefone'])
        criar_entrada("Nome:", "nome", cliente.get("nome", ""))
        criar_entrada("E-mail:", "email", cliente.get("email", ""))
        tk.Label(janela_editar, text="Observações:").pack()
        campo_obs = tk.Text(janela_editar, height=4)
        campo_obs.insert("1.0", cliente.get("obs", ""))
        campo_obs.pack()

        btn_salvar = ttk.Button(janela_editar, text="Salvar", state=tk.DISABLED)
        btn_cancelar = ttk.Button(janela_editar, text="Cancelar", command=janela_editar.destroy)

        def verificar_alteracoes(event=None):
            alterado = False
            for chave in ["telefone", "nome", "email"]:
                if campos[chave].get().strip() != original.get(chave, ""):
                    alterado = True
            if campo_obs.get("1.0", "end").strip() != original.get("obs", ""):
                alterado = True
            btn_salvar.config(state=tk.NORMAL if alterado else tk.DISABLED)

        for entrada in campos.values():
            entrada.bind("<KeyRelease>", verificar_alteracoes)
        campo_obs.bind("<KeyRelease>", verificar_alteracoes)

        def salvar_edicao():
            novo = {
                "telefone": campos["telefone"].get().strip(),
                "nome": campos["nome"].get().strip(),
                "email": campos["email"].get().strip(),
                "obs": campo_obs.get("1.0", "end").strip()
            }

            if not novo["telefone"] or not telefone_valido(novo["telefone"]):
                messagebox.showerror("Erro", "Telefone inválido.")
                return

            if novo["email"] and not email_valido(novo["email"]):
                messagebox.showerror("Erro", "E-mail inválido.")
                return

            for i, c in enumerate(clientes):
                if c == cliente:
                    clientes[i] = novo
                    break
            salvar_clientes(clientes)
            atualizar_lista(entrada_pesquisa.get().strip())
            janela_editar.destroy()

        btn_salvar.config(command=salvar_edicao)

        frame_inferior = tk.Frame(janela_editar)
        frame_inferior.pack(side=tk.BOTTOM, fill='x', pady=20)
        frame_botoes = tk.Frame(frame_inferior)
        frame_botoes.place(relx=0.5, rely=0.5, anchor='center')
        btn_salvar.pack(side=tk.LEFT, padx=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

    def editar_cliente_selecionado():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            editar(index)

    def remover():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            cliente = clientes_filtrados[index]
            clientes.remove(cliente)
            salvar_clientes(clientes)
            atualizar_lista(entrada_pesquisa.get().strip())

    def ao_selecionar(event):
        selecionado = tree.selection()
        btn_editar.config(state=tk.NORMAL if selecionado else tk.DISABLED)

    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    frame_botoes = tk.Frame(cadastro)
    frame_botoes.pack(pady=5)
    ttk.Button(frame_botoes, text="Adicionar", command=adicionar).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Remover Selecionado", command=remover).pack(side=tk.LEFT, padx=10)
    btn_editar = ttk.Button(frame_botoes, text="Editar Cliente", command=editar_cliente_selecionado, state=tk.DISABLED)
    btn_editar.pack(side=tk.LEFT, padx=10)

    atualizar_lista()
