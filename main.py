import tkinter as tk
from tkinter import messagebox
from produtos import abrir_cadastro
from orcamento import abrir_orcamento

class GerenciadorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EMPRESA")
        self.master.geometry("400x300")
        self.criar_interface()

    def criar_interface(self):
        tk.Label(self.master, text="Bem-vindo ao Sistema MQ", font=("Helvetica", 14, "bold")).pack(pady=20)
        tk.Button(self.master, text="Cadastro de Produtos", command=lambda: abrir_cadastro(self.master)).pack(pady=5, fill='x', padx=50)
        tk.Button(self.master, text="Novo Orçamento / Impressão", command=lambda: abrir_orcamento(self.master)).pack(pady=5, fill='x', padx=50)
        tk.Button(self.master, text="Sair", command=self.master.quit).pack(pady=20, fill='x', padx=50)

entry_usuario = None
entry_senha = None
login = None  # Janela de login

def tela_login(ao_logar):
    global entry_usuario, entry_senha, login
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x180")

    tk.Label(login, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(login)
    entry_usuario.pack()

    tk.Label(login, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(login, show="*")
    entry_senha.pack()

    tk.Button(login, text="Entrar", command=lambda: verificar_login(ao_logar)).pack(pady=10)

    login.mainloop()

def verificar_login(ao_logar):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "1234":
        login.destroy()
        ao_logar()
    else:
        messagebox.showerror(title="Erro", message="Usuário ou senha incorretos!")

def iniciar_sistema():
    root = tk.Tk()
    app = GerenciadorApp(root)
    root.mainloop()

# Início do programa
if __name__ == "__main__":
    tela_login(iniciar_sistema)