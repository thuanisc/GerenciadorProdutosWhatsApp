import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CAMINHO_CLIENTES = "clientes.json"

def carregar_clientes():
    if os.path.exists(CAMINHO_CLIENTES):
        with open(CAMINHO_CLIENTES, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def salvar_clientes(lista):
    with open(CAMINHO_CLIENTES, "w", encoding="utf-8") as file:
        json.dump(lista, file, indent=4, ensure_ascii=False)

def abrir_cadastro_clientes(janela_pai):
    janela = tk.Toplevel(janela_pai)
    janela.title("Cadastro de Clientes")
    janela.geometry("700x400")

    clientes = carregar_clientes()
    clientes_filtrados = clientes.copy()

    # Frame do topo (barra de pesquisa)
    frame_topo = tk.Frame(janela)
    frame_topo.pack(pady=5)
    tk.Label(frame_topo, text="Pesquisar:").pack(side=tk.LEFT)
    campo_pesquisa = tk.Entry(frame_topo, width=40)
    campo_pesquisa.pack(side=tk.LEFT, padx=5)

    # Treeview (lista com colunas)
    colunas = ("telefone", "nome", "email", "observacoes")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    tree.heading("telefone", text="Telefone")
    tree.heading("nome", text="Nome")
    tree.heading("email", text="E-mail")
    tree.heading("observacoes", text="Observações")
    tree.pack(padx=10, pady=10, fill='both', expand=True)

    def atualizar_lista(filtro=""):
        tree.delete(*tree.get_children())
        clientes_filtrados.clear()
        for cliente in clientes:
            if filtro.lower() in json.dumps(cliente, ensure_ascii=False).lower():
                clientes_filtrados.append(cliente)
                tree.insert("", "end", values=(
                    cliente.get("telefone", ""),
                    cliente.get("nome", ""),
                    cliente.get("email", ""),
                    cliente.get("observacoes", "")
                ))

    def ao_digitar(event):
        termo = campo_pesquisa.get().strip()
        atualizar_lista(termo)

    campo_pesquisa.bind("<KeyRelease>", ao_digitar)

    def adicionar_cliente():
        def salvar():
            telefone = telefone_entry.get().strip()
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            obs = obs_entry.get("1.0", "end").strip()

            if not telefone:
                messagebox.showwarning("Atenção", "O telefone é obrigatório.")
                return

            novo = {
                "telefone": telefone,
                "nome": nome,
                "email": email,
                "observacoes": obs
            }
            clientes.append(novo)
            salvar_clientes(clientes)
            atualizar_lista(campo_pesquisa.get().strip())
            janela_nova.destroy()

        janela_nova = tk.Toplevel(janela)
        janela_nova.title("Novo Cliente")
        janela_nova.geometry("400x300")

        tk.Label(janela_nova, text="Telefone (obrigatório):").pack()
        telefone_entry = tk.Entry(janela_nova)
        telefone_entry.pack()

        tk.Label(janela_nova, text="Nome:").pack()
        nome_entry = tk.Entry(janela_nova)
        nome_entry.pack()

        tk.Label(janela_nova, text="E-mail:").pack()
        email_entry = tk.Entry(janela_nova)
        email_entry.pack()

        tk.Label(janela_nova, text="Observações:").pack()
        obs_entry = tk.Text(janela_nova, height=4)
        obs_entry.pack()

        tk.Button(janela_nova, text="Salvar", command=salvar).pack(pady=10)

    def remover_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um cliente para remover.")
            return
        valores = tree.item(item, "values")
        telefone = valores[0]
        cliente = next((c for c in clientes if c["telefone"] == telefone), None)
        if cliente and messagebox.askyesno("Confirmação", f"Remover cliente {cliente.get('nome', '')}?"):
            clientes.remove(cliente)
            salvar_clientes(clientes)
            atualizar_lista(campo_pesquisa.get().strip())

    # Botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Adicionar Cliente", command=adicionar_cliente).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Remover Selecionado", command=remover_cliente).pack(side=tk.LEFT, padx=10)

    atualizar_lista()