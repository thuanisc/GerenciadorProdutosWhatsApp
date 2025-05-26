# orcamento.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import pyperclip
from datetime import datetime
import os
from produtos import carregar_produtos

PASTA_ORCAMENTOS = 'orcamentos'
os.makedirs(PASTA_ORCAMENTOS, exist_ok=True)

def abrir_orcamento(master):
    produtos = carregar_produtos()
    orc = tk.Toplevel(master)
    orc.title("Novo Orçamento")
    orc.geometry("1000x720")

    carrinho = []

    frame_top = tk.Frame(orc)
    frame_top.pack(fill='both', expand=True, pady=5)

    frame_esq = tk.Frame(frame_top)
    frame_esq.pack(side='left', fill='both', expand=True, padx=5)
    tk.Label(frame_esq, text="Produtos disponíveis:").pack()
    lista_prod = tk.Listbox(frame_esq)
    lista_prod.pack(fill='both', expand=True)
    for p in produtos:
        lista_prod.insert(tk.END, f"{p['nome']} - R${p['preco']:.2f}".replace('.', ','))

    tk.Label(frame_esq, text="Unidades:").pack(pady=(10, 0))
    entry_qtd = tk.Entry(frame_esq, width=5)
    entry_qtd.insert(0, "1")
    entry_qtd.pack()

    frame_dir = tk.Frame(frame_top)
    frame_dir.pack(side='right', fill='both', expand=True, padx=5)
    tk.Label(frame_dir, text="Itens no orçamento:").pack()
    tree_cols = ("Produto", "Qtd", "Preço Unit.", "Total")
    tree = ttk.Treeview(frame_dir, columns=tree_cols, show='headings')
    for col in tree_cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill='both', expand=True)

    preview_text = tk.Text(orc, height=16, font=("Courier", 10))
    preview_text.pack(fill='x', padx=10, pady=5)

    frame_inf = tk.Frame(orc)
    frame_inf.pack(pady=5)
    tk.Label(frame_inf, text="Desconto (R$ ou %):").pack(side=tk.LEFT)
    desconto_entry = tk.Entry(frame_inf, width=10)
    desconto_entry.insert(0, "0")
    desconto_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_inf, text="Tempo de serviço:").pack(side=tk.LEFT, padx=(20, 5))
    tempo_entry = tk.Entry(frame_inf, width=20)
    tempo_entry.insert(0, "1 à 2 dias úteis")
    tempo_entry.pack(side=tk.LEFT)

    def atualizar_preview():
        total = sum(item['total'] for item in carrinho)
        desc_texto = desconto_entry.get().replace(',', '.').strip()
        tempo = tempo_entry.get().strip()
        desconto = 0
        is_percentual = False

        if desc_texto.endswith('%'):
            try:
                perc = float(desc_texto.replace('%', ''))
                desconto = total * (perc / 100)
                is_percentual = True
            except:
                desconto = 0
        else:
            try:
                desconto = float(desc_texto)
            except:
                desconto = 0

        total_final = total - desconto
        msg = ""
        for item in carrinho:
            msg += f"*{item['nome']}*\n- {item['qtd']} un. X R${item['preco']:.2f} = *R${item['total']:.2f}*\n"
            if item.get('obs'):
                msg += f"> {item['obs']}\n"
        msg += "╠═══════════════════╣\n"
        if tempo != "0" and tempo:
            msg += f"🕒 *Tempo de serviço*: {tempo} (se ficar pronto antes, avisamos)\n"
        msg += f"🧾 *Subtotal*: R${total:.2f}\n"
        if is_percentual:
            msg += f"💖 *Desconto* ({int((desconto/total)*100)}%): -R${desconto:.2f}\n"
        elif desconto > 0:
            msg += f"💖 *Desconto* (-): -R${desconto:.2f}\n"
        msg += f"💰 *Total Final*: R${total_final:.2f}"

        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, msg.replace('.', ','))

    def adicionar_item():
        idx = lista_prod.curselection()
        if not idx:
            return
        index = idx[0]
        prod = produtos[index]
        try:
            qtd = int(entry_qtd.get())
        except:
            qtd = 1
        if qtd < 1:
            return
        total = prod['preco'] * qtd
        carrinho.append({"nome": prod['nome'], "qtd": qtd, "preco": prod['preco'], "total": total, "obs": prod.get('obs', '')})
        tree.insert("", tk.END, values=(prod['nome'], qtd, f"R${prod['preco']:.2f}".replace('.', ','), f"R${total:.2f}".replace('.', ',')))
        atualizar_preview()

    def remover_item():
        selecionado = tree.selection()
        if selecionado:
            index = tree.index(selecionado[0])
            tree.delete(selecionado[0])
            carrinho.pop(index)
            atualizar_preview()

    def editar_item(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        index = tree.index(item)
        item_data = carrinho[index]

        nova_qtd = simpledialog.askinteger("Editar Quantidade", f"Alterar quantidade de '{item_data['nome']}':",
                                           initialvalue=item_data['qtd'])
        if nova_qtd and nova_qtd > 0:
            item_data['qtd'] = nova_qtd
            item_data['total'] = nova_qtd * item_data['preco']
            tree.item(item, values=(
                item_data['nome'],
                nova_qtd,
                f"R${item_data['preco']:.2f}".replace('.', ','),
                f"R${item_data['total']:.2f}".replace('.', ',')
            ))
            atualizar_preview()

    def copiar_preview():
        pyperclip.copy(preview_text.get("1.0", tk.END))
        messagebox.showinfo("Copiado", "Texto copiado para WhatsApp!")

    def salvar():
        nome = simpledialog.askstring("Cliente", "Nome do cliente:")
        if not nome:
            return
        agora = datetime.now().strftime('%Y-%m-%d_%H-%M')
        caminho = os.path.join(PASTA_ORCAMENTOS, f"{nome}_{agora}.txt")
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(preview_text.get("1.0", tk.END))
        messagebox.showinfo("Orçamento Salvo", f"Salvo em {caminho}")

    def imprimir():
        preview_win = tk.Toplevel(orc)
        preview_win.title("Pré-visualização do Cupom")
        preview_win.geometry("500x600")
        texto = tk.Text(preview_win, font=("Courier", 10))
        texto.insert(tk.END, preview_text.get("1.0", tk.END))
        texto.pack(expand=True, fill='both')

    tree.bind("<Double-1>", editar_item)

    frame_botoes = tk.Frame(orc)
    frame_botoes.pack(pady=10)
    ttk.Button(frame_botoes, text="Adicionar ao Orçamento", command=adicionar_item).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Remover Selecionado", command=remover_item).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Atualizar Preview", command=atualizar_preview).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Copiar para WhatsApp", command=copiar_preview).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Salvar Orçamento", command=salvar).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botoes, text="Imprimir Cupom", command=imprimir).pack(side=tk.LEFT, padx=10)
