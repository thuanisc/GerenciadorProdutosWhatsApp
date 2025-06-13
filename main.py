# main.py
import tkinter as tk
from produtos import abrir_cadastro
from orcamento import abrir_orcamento

class GerenciadorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EMPRESA")
        self.master.geometry("400x300")
        self.criar_interface()

    def criar_interface(self):
        tk.Label(self.master, text="Bem-vindo ao Sistema MqC", font=("Helvetica", 14, "bold")).pack(pady=20)
        tk.Button(self.master, text="Cadastro de Produtos", command=lambda: abrir_cadastro(self.master)).pack(pady=5, fill='x', padx=50)
        tk.Button(self.master, text="Novo Orçamento / Impressão", command=lambda: abrir_orcamento(self.master)).pack(pady=5, fill='x', padx=50)
        tk.Button(self.master, text="Sair", command=self.master.quit).pack(pady=20, fill='x', padx=50)

if __name__ == '__main__':
    root = tk.Tk()
    app = GerenciadorApp(root)
    root.mainloop()